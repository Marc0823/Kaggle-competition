from pathlib import Path
import json

root = Path.cwd()
base_nb_path = root / 'kaggle_kernel_henry_tabicl_stack' / 'fork-of-rogiii-wgp-competition-using-ml-mode.ipynb'
base_meta_path = root / 'kaggle_kernel_henry_tabicl_stack' / 'kernel-metadata.json'
sunny_path = root / 'public_kernels' / 'sunny_physical_model' / 'rogii-wellbore-tvt-physical-model.py'
out_dir = root / 'kaggle_kernel_henry_v10_sunny80_blend'
out_dir.mkdir(exist_ok=True)

nb = json.loads(base_nb_path.read_text(encoding='utf-8'))
meta = json.loads(base_meta_path.read_text(encoding='utf-8'))
sunny_code = sunny_path.read_text(encoding='utf-8')

blend_code = f'''
# Final hidden-compatible Sunny80 + v10 artifact20 blend.
# The upstream notebook has just written /kaggle/working/submission.csv as the v10 artifact stack output.
from pathlib import Path
import pandas as pd
import numpy as np

WORK = Path('/kaggle/working') if Path('/kaggle/working').exists() else Path.cwd()
v10_path = WORK / 'submission.csv'
if not v10_path.exists():
    raise FileNotFoundError(f'v10 submission not found: {{v10_path}}')
v10 = pd.read_csv(v10_path)[['id', 'tvt']].copy()
v10['tvt'] = pd.to_numeric(v10['tvt'], errors='coerce')
if v10['tvt'].isna().any():
    raise RuntimeError('v10 submission contains NaN before Sunny blend')
v10_copy_path = WORK / 'submission_v10_artifact_stack.csv'
v10.to_csv(v10_copy_path, index=False)
print('Saved v10 component:', v10_copy_path, len(v10))

SUNNY_CODE = {sunny_code!r}
# Execute Sunny in an isolated namespace. It writes submission.csv in the working directory.
sunny_ns = {{'__name__': '__sunny_component__'}}
exec(SUNNY_CODE, sunny_ns)

sunny_path = WORK / 'submission.csv'
if not sunny_path.exists():
    sunny_path = Path('submission.csv')
if not sunny_path.exists():
    raise FileNotFoundError('Sunny component did not write submission.csv')
sunny = pd.read_csv(sunny_path)[['id', 'tvt']].copy()
sunny['tvt'] = pd.to_numeric(sunny['tvt'], errors='coerce')
if sunny['tvt'].isna().any():
    raise RuntimeError('Sunny submission contains NaN')
sunny_copy_path = WORK / 'submission_sunny_physical.csv'
sunny.to_csv(sunny_copy_path, index=False)
print('Saved Sunny component:', sunny_copy_path, len(sunny))

if len(sunny) != len(v10):
    raise RuntimeError(f'component row count mismatch: sunny={{len(sunny)}} v10={{len(v10)}}')
if not sunny['id'].astype(str).equals(v10['id'].astype(str)):
    raise RuntimeError('component id order mismatch')

final = v10[['id']].copy()
final['tvt'] = (0.80 * sunny['tvt'].astype(float).to_numpy() + 0.20 * v10['tvt'].astype(float).to_numpy()).round(2)
if final['id'].duplicated().any():
    raise RuntimeError('duplicate ids in final submission')
if final['tvt'].isna().any() or not np.isfinite(final['tvt'].astype(float).to_numpy()).all():
    raise RuntimeError('non-finite final predictions')
final.to_csv(WORK / 'submission.csv', index=False)
summary = {{
    'rows': int(len(final)),
    'min': float(final['tvt'].min()),
    'max': float(final['tvt'].max()),
    'mean': float(final['tvt'].mean()),
    'std': float(final['tvt'].std()),
    'rms_delta_vs_sunny': float(np.sqrt(np.mean((final['tvt'].to_numpy(float) - sunny['tvt'].to_numpy(float))**2))),
    'rms_delta_vs_v10': float(np.sqrt(np.mean((final['tvt'].to_numpy(float) - v10['tvt'].to_numpy(float))**2))),
}}
print('Final Sunny80/v10 artifact20 summary:', summary)
print(final.head().to_string(index=False))
'''

nb['cells'].append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': '## Final Sunny80 + v10 Artifact20 Blend\n\nHidden-compatible reconstruction of Kojimar physical/artifact blend.',
})
nb['cells'].append({
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {},
    'outputs': [],
    'source': blend_code,
})

out_nb = out_dir / 'rogii-henry-v10-sunny80-blend.ipynb'
nb['metadata'].setdefault('kaggle', {})['isGpuEnabled'] = True
out_nb.write_text(json.dumps(nb, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')

meta['id'] = 'leemarc223/rogii-henry-v10-sunny80-blend'
meta['title'] = 'ROGII Henry v10 Sunny80 Blend'
meta['code_file'] = out_nb.name
meta['kernel_type'] = 'notebook'
meta['language'] = 'python'
meta['is_private'] = True
meta['enable_gpu'] = True
meta['enable_tpu'] = False
meta['enable_internet'] = False
(out_dir / 'kernel-metadata.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
print(out_dir)
print(out_nb, out_nb.stat().st_size)
