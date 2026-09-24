"""Read-only exact committed STEP checks for the arm-removal revision."""
from pathlib import Path
import json,sys
from build123d import import_step,Pos,Box
root=Path(sys.argv[1]);build=int(sys.argv[2])
s={p.stem:import_step(str(p)) for p in (root/'validated/objects').rglob('*.step')}
def vol(a,b):
 c=a&b
 return max(0,c.volume) if c is not None else 0
# Entire previously occupied inward arm space forward of rear guide (not just sample points).
empty=vol(s['body'],Pos(0,0,120)*Box(230,80,140))
locks=[]
for side in ['left','right']:
 panel=s['side_'+side];bolt=s['side_lock_'+side];nut=s['side_lock_nut_'+side]
 lift=vol(Pos(0,0,1)*panel,bolt)
 bearing=panel.distance_to(bolt)
 guide=s['blue_spine'].distance_to(nut)
 locks.append({'side':side,'head_to_countersink_distance_mm':bearing,'nut_to_guide_distance_mm':guide,'lift_1mm_blocking_volume_mm3':lift,'nut_thickness_mm':2.4,'tip_protrusion_mm':0.95})
r={'buildNumber':build,'source_build_path':str(root),'former_arm_region_body_material_mm3':empty,'side_locks':locks,'status':'pass' if empty<1e-6 and all(x['head_to_countersink_distance_mm']<1e-6 and x['nut_to_guide_distance_mm']<1e-6 and x['lift_1mm_blocking_volume_mm3']>.001 for x in locks) else 'failed','limits':'Nominal rigid geometry; not a 2kg load test, contact pressure, thread stripping, fatigue or creep certification.'}
Path('design/archive_handbag/verification/arm-removal-check.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
