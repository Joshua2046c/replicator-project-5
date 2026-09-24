"""Observe exact committed STEP geometry; does not write or regenerate CAD."""
from pathlib import Path
import sys,json
from build123d import import_step,Box,Pos
root=Path(sys.argv[1]);build=int(sys.argv[2]);s={p.stem:import_step(str(p)) for p in (root/'validated/objects').rglob('*.step')}
def vol(a,b):
 c=a&b
 return max(0,c.volume) if c is not None else 0
pegs=[]
for host,y in [('blue_spine',-47),('body',52)]:
 for x in [-80,-40,40,80]:
  probe=Pos(x,y,6)*Box(3.8,3.8,3)
  outside=Pos(x+2.1,y,6)*Box(.1,.1,1)
  pegs.append({'host':host,'xy':[x,y],'peg_core_material_mm3':vol(s['bottom_panel'],probe),'socket_core_material_mm3':vol(s[host],probe),'side_clearance_probe_material_mm3':vol(s[host],outside)+vol(s['bottom_panel'],outside)})
# Former long locating slots between pegs now solid bottom plate, while former tongues belowZ4 are absent.
old_slots=[]
for host,y in [('blue_spine',-49.5),('body',54)]:
 for x in [-60,60]:
  p=Pos(x,y,3)*Box(1,1,1)
  old_slots.append({'xy':[x,y],'bottom_material_mm3':vol(s['bottom_panel'],p),'board_tongue_material_mm3':vol(s[host],p)})
side_filled=[]
for host,x in [('side_left',-108),('side_right',108)]:side_filled.append({'object':host,'former_lock_hole_material_mm3':vol(s[host],Pos(x,-46.5,100)*Box(1,1,1))})
# User now wants the tongue rooted on the BOTTOM rail, raised toward the viewer.
# Probe center strip and an empty aperture point at the same Z; old leftward tongue must be gone.
from math import sqrt
zz=94;u=(zz-78)/22;rise=2*(3*u*u-2*u*u*u)
cy=-51+sqrt((88+1/3)**2-32**2);y=cy-sqrt((88+1/3)**2-(zz-96)**2)-rise-.5
metal=vol(s['buckle'],Pos(0,y,zz)*Box(1,.2,1));air=vol(s['buckle'],Pos(8,y,zz)*Box(1,.2,1))
checks={'eight_square_pegs':len(pegs)==8 and all(abs(p['peg_core_material_mm3']-43.32)<1e-5 and p['socket_core_material_mm3']<1e-6 and p['side_clearance_probe_material_mm3']<1e-6 for p in pegs),'long_slots_and_tongues_removed':all(abs(p['bottom_material_mm3']-1)<1e-5 and p['board_tongue_material_mm3']<1e-6 for p in old_slots),'side_lock_holes_filled':all(abs(p['former_lock_hole_material_mm3']-1)<1e-5 for p in side_filled),'obsolete_screws_absent':not any(n.startswith(('bottom_screw','side_lock')) for n in s),'buckle_single_connected_solid':len(s['buckle'].solids())==1,'half_tongue':metal>.19 and air<1e-6}
r={'buildNumber':build,'source_build_path':str(root),'checks':checks,'pegs':pegs,'former_slot_probes':old_slots,'side_hole_probes':side_filled,'tongue_material_mm3':metal,'opposite_aperture_material_mm3':air,'geometry_status':'pass' if all(checks.values()) else 'failed','nominal_interface_mm':{'square_post':4,'height':6,'socket':4.4,'depth':6.3,'clearance_per_side':.2,'roof_clearance':.3},'retention_status':'unresolved_for_2kg_carrying','warning':'Straight clearance pegs and unlocked sliding sides are not positive pullout restraints. No bottom or side locking screws remain per user instruction. Dry assembled model must not be represented as carrying-ready; no adhesive or other retention has been validated.'}
Path('design/archive_handbag/verification/square-peg-check.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))