"""Local, incremental CJE full-text search. Python standard library only; no network."""
from pathlib import Path
import argparse
import json
import re
import sqlite3

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--corpus-root', type=Path, required=True)
parser.add_argument('--build', action='store_true')
parser.add_argument('--query')
parser.add_argument('--limit', type=int, default=5)
parser.add_argument('--per-paper', type=int, default=2)
args = parser.parse_args()
root = args.corpus_root.resolve()
audit = json.loads((root / 'catalog/download_audit.json').read_text())
directory = root / 'index'
directory.mkdir(exist_ok=True)
db = sqlite3.connect(directory / 'cje.sqlite')
db.row_factory = sqlite3.Row
db.executescript('''
CREATE TABLE IF NOT EXISTS documents (
 doi TEXT PRIMARY KEY, title TEXT, authors TEXT, year INTEGER, volume TEXT,
 issue TEXT, printed_pages TEXT, pdf_file TEXT, status TEXT,
 fingerprint TEXT, indexed_chunks INTEGER DEFAULT 0
);
CREATE VIRTUAL TABLE IF NOT EXISTS passages USING fts5(
 doi UNINDEXED, pdf_page UNINDEXED, body, tokenize='porter unicode61'
);
''')
changed = 0
if args.build:
    for item in audit['articles']:
        doi = item['doi']
        old = db.execute('SELECT fingerprint,indexed_chunks FROM documents WHERE doi=?', (doi,)).fetchone()
        textpath = Path(item.get('text_file', '/nonexistent'))
        usable = item['status'] == 'pdf_validated' and textpath.is_file() and item.get('text_chars', 0) > 0
        fingerprint = f'{item.get("sha256")}:{textpath.stat().st_mtime_ns}' if usable else None
        status = item['status'] if usable else 'text_not_available_or_identity_unverified'
        count = old['indexed_chunks'] if old else 0
        if usable and (not old or old['fingerprint'] != fingerprint):
            db.execute('DELETE FROM passages WHERE doi=?', (doi,))
            count = 0
            for number, page in enumerate(textpath.read_text().split('\f'), 1):
                page = '\n'.join(line for line in page.splitlines() if not re.search(r'Downloaded from .* by .* user on ', line))
                for start in range(0, len(page), 2150):
                    chunk = page[start:start + 2400].strip()
                    if len(chunk) >= 60:
                        db.execute('INSERT INTO passages(doi,pdf_page,body) VALUES(?,?,?)', (doi, number, chunk))
                        count += 1
            changed += 1
        db.execute('''INSERT INTO documents VALUES(?,?,?,?,?,?,?,?,?,?,?)
          ON CONFLICT(doi) DO UPDATE SET title=excluded.title,authors=excluded.authors,
          year=excluded.year,volume=excluded.volume,issue=excluded.issue,
          printed_pages=excluded.printed_pages,pdf_file=excluded.pdf_file,
          status=excluded.status,fingerprint=excluded.fingerprint,indexed_chunks=excluded.indexed_chunks''',
          (doi,item['title'],item.get('authors'),item.get('year'),str(item.get('volume')),str(item.get('issue')),
           item.get('pages'),item.get('file'),status,fingerprint,count))
    db.commit()
coverage = {
    'all_issues_complete': audit['all_issues_complete'],
    'requested_scope': audit.get('requested_scope'),
    'requested_scope_complete': audit.get('requested_scope_complete', False),
    'metadata_records': audit['metadata_distinct_dois'],
    'validated_pdfs': audit['validated_pdfs'],
    'indexed_documents': db.execute("SELECT COUNT(*) FROM documents WHERE status='pdf_validated' AND indexed_chunks>0").fetchone()[0],
    'documents_indexed_or_updated_this_run': changed,
    'citation_page_basis': 'pdf_page is the 1-based PDF page, not necessarily the printed journal page'
}
result = {'coverage': coverage, 'query': args.query,
          'search_limitation': 'Text matches may be in a bibliography or a discussion of another author; inspect surrounding text before attributing claims.',
          'hits': []}
if args.query:
    try:
        rows = db.execute('''SELECT d.doi,d.title,d.authors,d.year,d.volume,d.issue,d.printed_pages,
          d.pdf_file,p.pdf_page,bm25(passages) AS rank,
          snippet(passages,2,'[',']',' … ',70) AS excerpt
          FROM passages p JOIN documents d ON d.doi=p.doi
          WHERE passages MATCH ? AND d.status='pdf_validated'
          ORDER BY rank LIMIT ?''', (args.query, max(1, min(20,args.limit))*20)).fetchall()
        per_paper = {}
        for row in rows:
            count = per_paper.get(row['doi'], 0)
            if count >= max(1,args.per_paper):
                continue
            hit = dict(row)
            hit['text_file'] = str(root / 'text' / (Path(hit['pdf_file']).stem + '.txt'))
            result['hits'].append(hit)
            per_paper[row['doi']] = count + 1
            if len(result['hits']) >= max(1,min(20,args.limit)):
                break
    except sqlite3.OperationalError as error:
        parser.error('FTS query failed. Use English terms or a quoted phrase: ' + str(error))
print(json.dumps(result, ensure_ascii=False, indent=2))
db.close()
