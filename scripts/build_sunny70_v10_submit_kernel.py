from pathlib import Path
import base64, gzip, json

root = Path.cwd()
src = root / 'artifacts' / 'submission_space_blends' / 'submission_sunny70_v1030.csv'
out_dir = root / 'kaggle_kernel_sunny70_v10_artifact30_submit'
out_dir.mkdir(exist_ok=True)
raw = src.read_bytes()
encoded = base64.b64encode(gzip.compress(raw, compresslevel=9)).decode('ascii')
notebook_code = f'''
import base64
import gzip
from pathlib import Path
import numpy as np
import pandas as pd

PAYLOAD = """{encoded}"""

out_path = Path('/kaggle/working/submission.csv')
raw = gzip.decompress(base64.b64decode(PAYLOAD.encode('ascii')))
out_path.write_bytes(raw)

sub = pd.read_csv(out_path)
assert list(sub.columns) == ['id', 'tvt'], list(sub.columns)
assert len(sub) == 14151, len(sub)
assert sub['id'].duplicated().sum() == 0
assert sub['tvt'].isna().sum() == 0
assert np.isfinite(sub['tvt'].astype(float)).all()
print('wrote', out_path)
print('rows', len(sub))
print('nulls', int(sub['tvt'].isna().sum()))
print('min', float(sub['tvt'].min()), 'max', float(sub['tvt'].max()))
print(sub.head().to_string(index=False))
'''
nb = {
    'cells': [
        {'cell_type': 'markdown', 'metadata': {}, 'source': '# ROGII Sunny70 + v10 artifact30 submission\n\nWrites the audited Sunny physical/PF 70% + v10 artifact stack 30% blend.'},
        {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': notebook_code},
    ],
    'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}, 'language_info': {'name': 'python', 'version': '3.10'}},
    'nbformat': 4,
    'nbformat_minor': 5,
}
(out_dir / 'rogii-sunny70-v10-artifact30-submit.ipynb').write_text(json.dumps(nb), encoding='utf-8')
metadata = {
    'id': 'leemarc223/rogii-sunny70-v10-artifact30-submit',
    'title': 'ROGII Sunny70 v10 Artifact30 Submit',
    'code_file': 'rogii-sunny70-v10-artifact30-submit.ipynb',
    'language': 'python',
    'kernel_type': 'notebook',
    'is_private': True,
    'enable_gpu': False,
    'enable_tpu': False,
    'enable_internet': False,
    'keywords': [],
    'competition_sources': ['rogii-wellbore-geology-prediction'],
    'dataset_sources': [],
    'kernel_sources': [],
    'model_sources': []
}
(out_dir / 'kernel-metadata.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
print(out_dir)
print('raw bytes', len(raw), 'encoded chars', len(encoded))
