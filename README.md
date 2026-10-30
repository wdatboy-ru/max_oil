# F02a Hanze — входные данные для модели (двойная пористость / DFN)

Сбор и проверка входных данных для модели месторождения F02a Hanze (трещиноватый мел + плиоценовый газ) в tNavigator / Petrel.

## Что здесь

| Путь | Что это |
| --- | --- |
| `FINAL_REPORT.md` | Итоговый отчёт (собран из `work/FINAL_REPORT.src.md`) |
| `FINAL_parameters.xlsx` | Таблица параметров + все находки (собирается `work/build_xlsx.py`) |
| `FOR_FINAL_REPORT/` | 196 отчётов Argon (Gemini) по документам из `Hanze_docs/` + `index.md`, `_audit.md`, `task.md` |
| `work/all_findings.csv` | 11 754 находки Argon со ссылками на страницы оригиналов |
| `work/FINAL_REPORT.src.md` | Исходник отчёта с плейсхолдерами `{{КОД:стр}}` |
| `work/notes_verified.md` | Значения, сверенные со сканами |
| `work/las_inventory.md` | Инвентаризация каротажа |
| `work/topic_*.md`, `p*.txt`, `pages/` | Выборки по темам, извлечённый текст и картинки страниц |

## Скрипты (`work/`)

Пути считаются от расположения скриптов, так что всё работает из любой папки (Windows / macOS).

```bash
cd work
python parse_reports.py                                      # FOR_FINAL_REPORT/*.md → all_findings.csv
python show.py topic=4 rid=089 re=regex not=regex w=400      # фильтр по находкам
python checklist.py                                          # полнота ≈58 %, надёжность ≈79 %
python render_links.py FINAL_REPORT.src.md ../FINAL_REPORT.md # {{КОД:стр}} → file:///…#page=N
python build_xlsx.py                                         # FINAL_REPORT.md + csv → FINAL_parameters.xlsx (нужен openpyxl)
```

Порядок правки: редактировать `work/FINAL_REPORT.src.md` → `render_links.py` → `build_xlsx.py`.

## Чего нет в репозитории

`Hanze_docs/` (1.7 ГБ, оригиналы NLOG: PDF-сканы, LAS/DLIS — есть файлы > 100 МБ), `books/`, `Petrel_manuals/`, `tNav_manuals/`, статьи в PDF. Их нужно положить рядом вручную (диск / облако), сохранив структуру папок:

```
<корень репо>/Hanze_docs/...
<корень репо>/Petrel_manuals/...
```

Ссылки `file:///` в закоммиченных `FINAL_REPORT.md`, `FINAL_parameters.xlsx` и `all_findings.csv` указывают на `D:/Downloads/for_claude/…` (Windows). После того как `Hanze_docs/` окажется на месте, перегенерировать их под текущую машину: `parse_reports.py`, `render_links.py`, `build_xlsx.py`.

## Важно

Отчёты Argon содержат ошибки (например, в CPI F02-03 перепутаны RW и RMF) — каждое значение проверять по скану оригинала.
