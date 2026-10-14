import sys,json,hashlib
from pathlib import Path
from math import sqrt
from build123d import import_step,Pos,Box,GeomType
path,revision=sys.argv[1:3]
p={s.label:s.clean() for s in import_step(path).children};lid=p['lid'];lid.parent=None
checks=[]
def expect(name,actual,expected,tol=1e-5):
 checks.append(dict(name=name,actual=actual,expected=expected,passed=abs(actual-expected)<tol))
for y,sgn in [(-49.85,1),(53.35,-1)]:
 def section(x):
  q=lid & Pos(x,y+sgn*2,150.9)*Box(.1,4.4,2.4)
  return q.volume if q else 0
 baseline=section(56)
 for sign in [-1,1]:
  for x in [30,56,82.5,84.9,88,92]:expect(f'constant section y{y} x{sign*x}',section(sign*x),baseline)
 edge_y=y+sgn*sqrt(3.3**2-3**2)
 edges=[e for e in lid.edges() if e.geom_type==GeomType.LINE and abs(e.center().Z-152)<1e-5 and abs(e.center().Y-edge_y)<1e-5 and abs(e.length-70)<1e-5]
 expect(f'two straight70mm face edges y{y}',len(edges),2)
result=dict(revision=revision,step_sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),checks=checks)
Path('design/archive_handbag/verification/straight-lid-edges-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(checks=len(checks),failed=[c for c in checks if not c['passed']])))
assert all(c['passed'] for c in checks)
