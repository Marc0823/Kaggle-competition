import sys
from pathlib import Path

import nbformat


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: patch_aevion_lb52_fixed.py NOTEBOOK")
        return 2

    path = Path(sys.argv[1])
    nb = nbformat.read(path, as_version=4)
    changed = 0

    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        if "outputs" not in cell:
            cell.outputs = []
        if "execution_count" not in cell:
            cell.execution_count = None
        src = cell.source

        old = (
            "    z_v = ev['Z'].values.astype(float)\n"
            "    \n"
            "    # Calculate GR standard deviation from known section"
        )
        new = (
            "    z_v = ev['Z'].values.astype(float)\n"
            "    n = len(md_v)\n"
            "    \n"
            "    # Calculate GR standard deviation from known section"
        )
        if old in src:
            src = src.replace(old, new)
            changed += 1

        old = (
            '    print(f"train wells: {len(train_wids)} | test wells: {len(test_wids)}")\n'
            "    \n"
            "    # Build enhanced predictions using selector system"
        )
        new = (
            '    print(f"train wells: {len(train_wids)} | test wells: {len(test_wids)}")\n'
            "    # Submission only needs hidden test wells. Skipping train PF avoids timeout and does not use labels.\n"
            "    train_wids = []\n"
            '    print("test-only inference: skipping train-well PF/beam construction")\n'
            "    \n"
            "    # Build enhanced predictions using selector system"
        )
        if old in src:
            src = src.replace(old, new)
            changed += 1

        old = "hw['TVT_input'].iloc[-1] if len(hw[hw['TVT_input'].notna()]) > 0 else 0.0"
        new = "hw['TVT_input'].dropna().iloc[-1] if hw['TVT_input'].notna().any() else 0.0"
        if old in src:
            src = src.replace(old, new)
            changed += 1

        old = (
            "    for wid in test_wids:\n"
            "        if wid in test_preds:\n"
            "            pred = test_preds[wid]\n"
            "            hw, _ = load_well(wid, \"test\")\n"
        )
        new = (
            "    assigned_rows = 0\n"
            "    for wid in test_wids:\n"
            "        if wid not in test_preds and wid in likpf_test and wid in beam_test:\n"
            "            hw_tmp, _ = load_well(wid, \"test\")\n"
            "            _, variant_tmp, _, _ = selector_well_code(hw_tmp)\n"
            "            last_known_tmp = hw_tmp['TVT_input'].dropna().iloc[-1] if hw_tmp['TVT_input'].notna().any() else 0.0\n"
            "            test_preds[wid] = apply_selector_variant(variant_tmp, likpf_test[wid], beam_test[wid], last_known_tmp)\n"
            "            print(f\"fallback selector prediction built for {wid}: variant={variant_tmp}, n={len(test_preds[wid])}\")\n"
            "        if wid in test_preds:\n"
            "            pred = test_preds[wid]\n"
            "            hw, _ = load_well(wid, \"test\")\n"
        )
        if old in src:
            src = src.replace(old, new)
            changed += 1

        old = "                    tvt_val = pred[idx]\n"
        new = "                    tvt_val = pred[i]\n"
        if old in src:
            src = src.replace(old, new)
            changed += 1

        old = "                    sample_sub.loc[sample_sub['id'] == well_id, 'tvt'] = tvt_val\n"
        new = (
            "                    sample_sub.loc[sample_sub['id'] == well_id, 'tvt'] = tvt_val\n"
            "                    assigned_rows += 1\n"
        )
        if old in src:
            src = src.replace(old, new)
            changed += 1

        old = "    # Fill any remaining NaN values\n"
        new = (
            "    print(f\"assigned hidden rows from selector predictions: {assigned_rows}\")\n"
            "    if assigned_rows == 0:\n"
            "        raise RuntimeError(\"Aevion selector produced zero assigned rows; refusing all-zero submission\")\n"
            "    # Fill any remaining NaN values\n"
        )
        if old in src:
            src = src.replace(old, new)
            changed += 1

        cell.source = src

    nbformat.write(nb, path)
    print(f"changed={changed}")
    return 0 if changed >= 2 else 1


if __name__ == "__main__":
    raise SystemExit(main())
