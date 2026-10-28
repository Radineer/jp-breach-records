"""台帳（radineer.asia/cyber）の公開データから、配布用の CSV と JSON を作る。

使い方: python3 scripts/export.py <台帳の data.json> data/
- 公表文からの引用（quotes）は入れない。事実の項目と出典の URL だけを出す。
- 1行 = 1つの組織が出した公表（同じ組織の続報は1行にまとめ済み）。事案（インシデント）の単位ではない。
"""
import csv
import json
import sys
from pathlib import Path

src, out = sys.argv[1], Path(sys.argv[2])
rows = json.load(open(src, encoding='utf-8'))
FIELDS = ['id', 'org', 'published', 'latest', 'events', 'status', 'nature', 'where', 'how', 'device',
          'info_types', 'counts', 'sources', 'review', 'url']
recs = []
for r in sorted(rows, key=lambda r: (r.get('published') or '9999', r['id'])):
    recs.append({
        'id': r['id'], 'org': r['org'], 'published': r.get('published') or '', 'latest': r.get('latest') or '',
        'events': r['events'], 'status': r['status'], 'nature': r['nature'], 'where': r['where'], 'how': r['how'],
        'device': r['device'], 'info_types': r['info_types'],
        'counts': [{'label': c.get('label'), 'value': c.get('value'), 'status': c.get('status')} for c in r['counts']],
        'sources': r['sources'], 'review': r['review'], 'url': f"https://radineer.asia/cyber/cases/{r['id']}/",
    })
out.mkdir(parents=True, exist_ok=True)
json.dump(recs, open(out / 'records.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
with open(out / 'records.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(FIELDS)
    for r in recs:
        w.writerow([' / '.join(r[k]) if k in ('events', 'info_types', 'sources') else
                    ' / '.join(f"{c['label']}: {c['value']}（{c['status']}）" for c in r[k]) if k == 'counts' else r[k]
                    for k in FIELDS])
print(len(recs), 'records')
