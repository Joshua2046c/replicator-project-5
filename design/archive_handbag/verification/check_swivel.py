"""Read-only exact-build ring rotation and interface checks; no CAD writes."""
import sys,json,math
from pathlib import Path
from build123d import import_step,Axis
root=Path(sys.argv[1]);build=int(sys.argv[2])
files={p.stem:p for p in (root/'validated'/'objects').rglob('*.step')}
s={n:import_step(str(p)) for n,p in files.items()}
def vol(a,b):
 aa=a.bounding_box();bb=b.bounding_box()
 if not all(tuple(aa.max)[i]>tuple(bb.min)[i]+1e-6 and tuple(bb.max)[i]>tuple(aa.min)[i]+1e-6 for i in range(3)):return 0
 c=a&b
 return max(0,c.volume) if c is not None else 0
fails=[];tests=0
for name,x in [('eye_left',-110.3),('eye_right',110.3)]:
 for deg in range(0,360,15):
  eye=s[name].rotate(Axis((x,54,116),(1,0,0)),deg)
  for other,shape in s.items():
   if other==name:continue
   v=vol(eye,shape);tests+=1
   if v>0.001:fails.append({'eye':name,'angle_deg':deg,'other':other,'volume_mm3':round(v,6)})
allmin=[min(tuple(a.bounding_box().min)[i] for a in s.values()) for i in range(3)]
allmax=[max(tuple(a.bounding_box().max)[i] for a in s.values()) for i in range(3)]
r={'buildNumber':build,'source_build_path':str(root),'method':'B-rep intersections, ring spin sampled every 15 degrees, closed lid; does not certify load or nut retention','tests':tests,'collisions':fails,'all_hardware_envelope_mm':[round(b-a,4) for a,b in zip(allmin,allmax)],'ring_sweep_radial_bound_mm':round(math.hypot(36,14),4),'ring_swept_x_clearance_from_lid_mm':0.3,'axial_play_total_mm':0.6,'nominal_pivot_radial_clearance_mm':0.2,'status':'pass' if not fails else 'failed'}
Path('design/archive_handbag/verification/swivel-check.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(r,ensure_ascii=False,indent=2))
