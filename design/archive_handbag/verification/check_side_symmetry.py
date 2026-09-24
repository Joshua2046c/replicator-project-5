"""Verify the exported left panel against the reflected right panel and its mating parts."""
import hashlib,json,sys
from pathlib import Path
from build123d import import_step,mirror,Plane
path,revision=sys.argv[1:]
assembly=import_step(path)
p={s.label:s for s in assembly.children}
left=p['side_left'];right=p['side_right'];reflected=mirror(right,about=Plane.YZ)
a=left-reflected;b=reflected-left
delta=(abs(a.volume) if a else 0)+(abs(b.volume) if b else 0)
connections={name:{'left_mm':left.distance_to(p[name]),'right_mm':right.distance_to(p[name])} for name in ['blue_spine','body','bottom_panel','lid']}
passed=delta<1e-6 and len(left.solids())==len(right.solids())==1 and left.is_valid and right.is_valid and all(abs(v['left_mm']-v['right_mm'])<1e-6 for v in connections.values())
report={'revision':revision,'step_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'mirror_plane':'assembly YZ, X=0','left_right_symmetric_difference_mm3':delta,'connections':connections,'valid':left.is_valid and right.is_valid,'solids_each':[len(left.solids()),len(right.solids())],'passed':passed,'scope':'Closed geometry includes the entire outline, page cuts, mount hole and guide mating faces. Does not certify physical strength.'}
Path('design/archive_handbag/verification/side-symmetry-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert passed
