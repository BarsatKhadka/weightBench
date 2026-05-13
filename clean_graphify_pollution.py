"""Surgically remove README pollution nodes from graphify-out/graph.json.

These nodes came from past LLM extraction of PEFT-auto-generated
'Model Card for Model ID' README.md files inside LoRA pool/ and
checkpoints/ directories. They polluted the graph with ~1700 duplicate
nodes from boilerplate text. The source files were deleted from disk
but the graph.json still contains the extracted nodes.

Strategy:
1. Load graph.json
2. Identify polluted node IDs (source_file under pool/, pool_traj/, pool_dense/,
   or checkpoints/)
3. Remove those nodes
4. Remove all edges incident to them
5. Save back
6. Run `graphify update .` after to regenerate graph.html / GRAPH_REPORT.md
"""
import json
import shutil
from pathlib import Path

GRAPH = Path('graphify-out/graph.json')
backup = GRAPH.with_suffix('.json.bak')
shutil.copy2(GRAPH, backup)
print(f'Backup saved: {backup}')

with open(GRAPH, encoding='utf-8') as f:
    g = json.load(f)

n_before = len(g['nodes'])
e_before = len(g['links'])


def is_polluted(node):
    src = (node.get('source_file') or '').replace(chr(92), '/')
    return ('/pool/' in src or '/pool_traj/' in src or '/pool_dense/' in src
            or '/checkpoints/' in src)


polluted_ids = {n['id'] for n in g['nodes'] if is_polluted(n)}
print(f'Polluted node IDs: {len(polluted_ids)}')

# Filter nodes
g['nodes'] = [n for n in g['nodes'] if n['id'] not in polluted_ids]
print(f'Nodes: {n_before} ->{len(g["nodes"])}')

# Filter edges (any link touching a polluted node)
g['links'] = [l for l in g['links']
              if l['source'] not in polluted_ids
              and l['target'] not in polluted_ids]
print(f'Edges: {e_before} ->{len(g["links"])}')

# Filter hyperedges if any
if 'hyperedges' in g:
    hb = len(g['hyperedges'])
    g['hyperedges'] = [
        h for h in g['hyperedges']
        if not any(m in polluted_ids for m in (h.get('members') or []))
    ]
    print(f'Hyperedges: {hb} ->{len(g["hyperedges"])}')

with open(GRAPH, 'w', encoding='utf-8') as f:
    json.dump(g, f, indent=2)
print(f'Cleaned graph written to {GRAPH}')

# Also clean manifest entries for the deleted files
manifest_path = Path('graphify-out/manifest.json')
if manifest_path.exists():
    with open(manifest_path, encoding='utf-8') as f:
        m = json.load(f)
    mb = len(m)
    m = {k: v for k, v in m.items()
         if not any(seg in k.replace(chr(92), '/')
                    for seg in ('/pool/', '/pool_traj/', '/pool_dense/',
                                 '/checkpoints/'))}
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(m, f, indent=2)
    print(f'Manifest: {mb} ->{len(m)} entries')
