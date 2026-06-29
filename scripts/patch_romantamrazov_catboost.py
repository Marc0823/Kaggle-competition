import json
from pathlib import Path


notebook = Path("artifacts/romantamrazov_super_solution_top3/rogii-super-solution-lb-top-3.ipynb")
nb = json.loads(notebook.read_text(encoding="utf-8"))

changed = False
for cell in nb.get("cells", []):
    source = cell.get("source", "")
    source_is_list = isinstance(source, list)
    text = "".join(source) if source_is_list else source

    if "CB_PARAMS=dict(" not in text or "subsample=0.75," not in text:
        continue
    if "bootstrap_type" in text:
        continue

    text = text.replace(
        "    subsample=0.75,\n    border_count=254,",
        '    subsample=0.75,\n    bootstrap_type="Bernoulli",\n    border_count=254,',
    )
    cell["source"] = text.splitlines(True) if source_is_list else text
    changed = True

if not changed:
    raise SystemExit("No CatBoost parameter block was patched")

notebook.write_text(json.dumps(nb, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print("Patched CatBoost bootstrap_type=\"Bernoulli\"")
