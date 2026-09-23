"""Read-only checks of exact committed Workbench STEP solids. Never writes CAD geometry."""
import sys,json,itertools
from pathlib import Path
from build123d import import_step, Axis, Pos
root=Path(sys.argv[1]); build=int(sys.argv[2])
files={f.stem:f for f in (root/'validated'/'objects').rglob('*.step')}
shapes={k:import_step(str(v)) for k,v in files.items()}
moving_names=[n for n in shapes if n=='lid' or n.startswith('lid_mag') or n in ['pink_spine','pink_marks','upper_binding']]
released=['central_binding','binding_overlap','buckle']
static_names=[n for n in shapes if n not in moving_names and n not in released]
axis=Axis((0,55,128),(1,0,0))
def intersects_bb(a,b):
 aa=a.bounding_box();bb=b.bounding_box()
 return all(tuple(aa.max)[i]>tuple(bb.min)[i]+1e-6 and tuple(bb.max)[i]>tuple(aa.min)[i]+1e-6 for i in range(3))
def collision(a,b):
 if not intersects_bb(a,b):return 0
 common=a & b
 return max(0,common.volume) if common is not None else 0
failures=[];maxvol=0;tests=0
angles=list(range(0,101,5)) if len(sys.argv)<4 else [int(a) for a in sys.argv[3].split(",")]
for angle in angles:
 moved={n:s.rotate(axis,-angle) for n,s in shapes.items() if n in moving_names}
 for n,a in moved.items():
  for m in static_names:
   v=collision(a,shapes[m]);tests+=1;maxvol=max(maxvol,v)
   if v>0.001:failures.append({'angle':angle,'moving':n,'fixed':m,'volume_mm3':round(v,6)})
 Path('design/archive_handbag/verification/'+(sys.argv[4] if len(sys.argv)>4 else 'motion')+'-progress.json').write_text(json.dumps({'build':build,'angle':angle,'collisions':failures},indent=2))
 print('opening',angle,'deg; collisions',len(failures),flush=True)
open_shapes={n:(s.rotate(axis,-100) if n in moving_names else s) for n,s in shapes.items() if n not in released}
removal=[]
for panel in ['side_left','side_right']:
 for dz in [0,0.4,1,5,20,50,100,125,150,185,200]:
  a=Pos(0,0,dz)*shapes[panel]
  for n,s in open_shapes.items():
   if n==panel:continue
   v=collision(a,s)
   if v>0.001:removal.append({'panel':panel,'lift_mm':dz,'other':n,'volume_mm3':round(v,6)})
# Closure prevents removal: 0.4mm top clearance, then solid contact with roof.
retention={n:collision(Pos(0,0,1)*shapes[n],shapes['lid']) for n in ['side_left','side_right']}
exclude=[n for n in shapes if n.startswith(('eye_','ring_bolt_','ring_nut_','pivot_','thumb_nut_','ring_bridge_','bridge_'))]
main=[s for n,s in shapes.items() if n not in exclude]
mins=[min(tuple(s.bounding_box().min)[i] for s in main) for i in range(3)]
maxs=[max(tuple(s.bounding_box().max)[i] for s in main) for i in range(3)]
report={'buildNumber':build,'source_build_path':str(root),'method':'exact B-rep intersections at discrete motion samples; not continuous swept-volume proof or structural certification','opening_angles_deg':angles,'released_before_opening':released,'opening_tests':tests,'opening_collisions':failures,'removal_collisions':removal,'closed_lift_1mm_blocking_volume_mm3':retention,'main_envelope_mm':[round(b-a,4) for a,b in zip(mins,maxs)],'solid_validity':{n:s.is_valid for n,s in shapes.items()},'status':'pass' if not failures and not removal and all(v>0 for v in retention.values()) else 'failed'}
out=Path('design/archive_handbag/verification/'+(sys.argv[4] if len(sys.argv)>4 else 'motion')+'-check.json');out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['solid_validity','opening_angles_deg']},ensure_ascii=False,indent=2))
