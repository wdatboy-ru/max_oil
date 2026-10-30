# Вывод находок из all_findings.csv с фильтрами: python show.py topic=4 rid=089 re=regex not=regex w=400
import csv, os, re, sys
args = dict(a.split('=', 1) for a in sys.argv[1:])
w = int(args.get('w', 400))
rows = list(csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_findings.csv'), encoding='utf-8-sig')))
last = None
for x in rows:
    if 'topic' in args and x['topic'] not in args['topic'].split(','):
        continue
    if 'rid' in args and x['rid'] not in args['rid'].split(','):
        continue
    if 're' in args and not re.search(args['re'], x['text'], re.I):
        continue
    if 'not' in args and re.search(args['not'], x['text'], re.I):
        continue
    if x['relative'] != last:
        print(f"## {x['rid']} {x['relative']} {x['part']}")
        last = x['relative']
    t = re.sub(r'\s+', ' ', x['text'])
    print(f"- T{x['topic']} p{x['orig_page']}: {t[:w]}")
