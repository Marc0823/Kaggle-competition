import json
from pathlib import Path

notebook = Path('artifacts/romantamrazov_super_solution_top3/rogii-super-solution-lb-top-3.ipynb')
nb = json.loads(notebook.read_text(encoding='utf-8'))
changed = False
for cell in nb.get('cells', []):
    source = cell.get('source', '')
    source_is_list = isinstance(source, list)
    text = ''.join(source) if source_is_list else source
    old = text
    if 'CB_PARAMS=dict(' in text:
        if 'subsample=0.75,' in text and 'bootstrap_type' not in text:
            text = text.replace(
                '    subsample=0.75,\n    border_count=254,',
                '    subsample=0.75,\n    bootstrap_type="Bernoulli",\n    border_count=254,',
            )
        text = text.replace('    devices="0:1",           # both T4', '    devices="0",             # single available T4')
        text = text.replace('devices="0:1"', 'devices="0"')
    if text != old:
        cell['source'] = text.splitlines(True) if source_is_list else text
        changed = True
if not changed:
    raise SystemExit('No changes applied')
notebook.write_text(json.dumps(nb, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
print('patched romantamrazov CatBoost bootstrap/device')
