# Разбор 196 отчётов Аргона в одну таблицу находок: work/all_findings.csv
import glob, re, csv, os, pathlib, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fs = sorted(glob.glob(os.path.join(ROOT, 'FOR_FINAL_REPORT', '[0-9]*.md')))

TOPICS = {1: 'Sw', 2: 'Por/Perm', 3: 'SCAL', 4: 'NTG', 5: 'Pressure/T/contacts', 6: 'Fractures/faults',
          7: 'Well tests', 8: 'Lithology/facies', 9: 'PVT/rock', 10: 'Reserves', 11: 'Logs', 12: 'Other'}
PDF_EXT = ('.pdf',)


def make_link(relative, page):
    rel = relative.replace('\\', '/')
    url = pathlib.Path(ROOT).as_uri() + '/Hanze_docs/' + urllib.parse.quote(rel, safe='/!,-_.')
    if rel.lower().endswith(PDF_EXT) and page:
        url += f'#page={page}'
    return url


def first_page(ref):
    m = re.search(r'(\d+)', ref)
    return int(m.group(1)) if m else None


rows = []
WELL_RE = re.compile(r'F\s?0?2[- ]?(?:A[- ]?0?\d(?:\s?[zZyY])?|B[- ]?0?1|0?[356])(?:[- ]?S(?:IDETRACK)?\s?\d)?', re.I)
for f in fs:
    t = open(f, encoding='utf-8').read()
    name = os.path.basename(f)
    rid = name.split('_')[0]
    rel = re.search(r'^relative:\s*"(.*)"', t, re.M).group(1).replace('\\\\', '/')
    pm = re.search(r'^part:\s*"(\d+)/(\d+), стр\. (\d+)-(\d+)', t, re.M)
    a = int(pm.group(3)) if pm else 1
    part = f'{pm.group(1)}/{pm.group(2)} p{pm.group(3)}-{pm.group(4)}' if pm else ''
    body = t.split('## Найдено', 1)[1] if '## Найдено' in t else ''
    body = body.split('## Не найдено')[0]
    topic = None
    cur = None
    items = []
    for line in body.splitlines():
        h = re.match(r'^\s*(?:\*\*|###\s*)(\d{1,2})\.\s', line)
        if h and not line.lstrip().startswith(('* ', '- ')):
            topic = int(h.group(1)); continue
        if line.lstrip().startswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if all(re.fullmatch(r':?-{2,}:?', c) or not c for c in cells):
                continue  # разделитель таблицы
            if cells and cells[0] in ('Параметр', 'Параметр / Уравнение') or re.match(r'^(Параметр|№)\b', cells[0] or ''):
                continue  # шапка таблицы
            cur = [topic, ' | '.join(cells)]; items.append(cur); cur = None
            continue
        if re.match(r'^\s*[\*\-]\s+', line):
            cur = [topic, line.strip()[2:].strip()]; items.append(cur)
        elif cur is not None and line.strip():
            cur[1] += ' ' + line.strip()
    for tp, txt in items:
        refs = re.findall(r'\[(стр\.[^\]]*|лист[^\]]*)\]\(<[^>]*>\)', txt)
        clean = re.sub(r'\(<file:[^>]*>\)', '', txt).strip()
        p = first_page(refs[0]) if refs and refs[0].startswith('стр') else None
        op = (a + p - 1) if p else None
        rows.append({
            'rid': rid, 'report': name, 'relative': rel, 'part': part, 'topic': tp,
            'topic_name': TOPICS.get(tp, ''), 'pages_in_report': '; '.join(refs),
            'orig_page': op if op else '', 'link': make_link(rel, op),
            'wells': '; '.join(sorted({re.sub(r'\s', '', w.upper()) for w in WELL_RE.findall(clean)})),
            'unreadable': 'НЕЧИТАЕМО' in clean.upper(),
            'text': clean,
        })

out = os.path.join(ROOT, 'work', 'all_findings.csv')
with open(out, 'w', encoding='utf-8-sig', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(len(fs), 'reports;', len(rows), 'findings')
from collections import Counter
print(Counter(r['topic'] for r in rows))
print('unreadable:', sum(r['unreadable'] for r in rows))
print('no topic:', sum(1 for r in rows if r['topic'] is None))
print('no page:', sum(1 for r in rows if not r['orig_page']))
