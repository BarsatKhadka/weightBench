"""Invalidate graphify cache entries for README files in pool/checkpoints dirs.
PEFT auto-generated README.md files have polluted the graph with hundreds
of duplicate "Model Card for Model ID" nodes. We've deleted the files;
this script clears the semantic cache so they don't reappear.
"""
import json
from pathlib import Path

with open('graphify-out/manifest.json', encoding='utf-8') as f:
    manifest = json.load(f)

to_invalidate = []
BACKSLASH = chr(92)
for path, meta in manifest.items():
    n = path.replace(BACKSLASH, '/')
    if '/pool/' in n or '/pool_' in n or '/checkpoints/' in n:
        if n.endswith('README.md'):
            to_invalidate.append((path, meta.get('hash')))

print(f'README entries to invalidate: {len(to_invalidate)}')

sem_dir = Path('graphify-out/cache/semantic')
removed = 0
for path, h in to_invalidate:
    if not h:
        continue
    cache_file = sem_dir / f'{h}.json'
    if cache_file.exists():
        cache_file.unlink()
        removed += 1
print(f'Semantic cache entries removed: {removed}')

invalidate_keys = {p for p, _ in to_invalidate}
new_manifest = {k: v for k, v in manifest.items() if k not in invalidate_keys}
print(f'Manifest entries dropped: {len(manifest) - len(new_manifest)}')

with open('graphify-out/manifest.json', 'w', encoding='utf-8') as f:
    json.dump(new_manifest, f, indent=2)
print('manifest updated')
