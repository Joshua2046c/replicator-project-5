"""Supplement timed-out automatic checks against the exact handoff STEP."""
import sys, json, hashlib
from pathlib import Path
from itertools import combinations
from build123d import import_step

path, revision = sys.argv[1:]
assembly = import_step(path)
# Unify tangent analytic face partitions in memory only; exported geometry is untouched.
parts = {p.label: p.clean() for p in assembly.children}
hits = []
exact = 0
for a, b in combinations(parts, 2):
    aa, bb = parts[a].bounding_box(), parts[b].bounding_box()
    if not all(tuple(aa.max)[i] > tuple(bb.min)[i]+1e-7 and tuple(bb.max)[i] > tuple(aa.min)[i]+1e-7 for i in range(3)):
        continue
    exact += 1
    common = parts[a] & parts[b]
    volume = abs(common.volume) if common else 0
    if volume > 1e-5:
        hits.append({'a':a, 'b':b, 'volume_mm3':volume})
report = {'revision':revision, 'step_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(), 'pairs_screened':len(parts)*(len(parts)-1)//2, 'exact_pairs':exact, 'overlaps':hits, 'all_valid':all(p.is_valid for p in parts.values()), 'scope':'Closed pose only; supplements automatic timeout, not load testing.'}
report['passed'] = report['all_valid'] and not hits
Path('design/archive_handbag/verification/export-interference-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2),flush=True)
assert report['passed']
