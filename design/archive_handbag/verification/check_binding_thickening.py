"""Check unchanged bottom, seating and new moving envelopes against exported B-rep."""
import json,sys,hashlib,math
from pathlib import Path
from itertools import combinations
from build123d import import_step, Pos, Box, Vertex, Axis
path, baseline, rev=sys.argv[1:]
p={s.label:s.clean() for s in import_step(path).children}
old={s.label:s.clean() for s in import_step(baseline).children}
def vol(s):
 if not s:return 0.0
 return abs(s.volume) if hasattr(s,'volume') else sum(abs(x.volume) for x in s)
def overlap(a,b):
 aa,bb=a.bounding_box(),b.bounding_box()
 if not all(tuple(aa.max)[i]>tuple(bb.min)[i]+1e-7 and tuple(bb.max)[i]>tuple(aa.min)[i]+1e-7 for i in range(3)):return 0.0
 return vol(a&b)
hits=[]
for a,b in combinations(p,2):
 v=overlap(p[a],p[b])
 if v>1e-5:hits.append([a,b,v])
print('closed pairs checked',len(hits),flush=True)
clip=Pos(0,0,.45)*Box(100,200,1.1)
a=p['central_binding']&clip;b=old['central_binding']&clip
bottom_delta=vol(a-b)+vol(b-a)
R=88+1/3;cy=-51+math.sqrt(R*R-32**2)-2
contact=[]
for z in range(84,101):
 q=Vertex(2,cy-math.sqrt(R*R-(z-96)**2),z)
 contact.append(max(p['buckle'].distance_to(q),p['central_binding'].distance_to(q)))
moving=['lid','upper_binding','pink_marks','nameplate','lid_magnet_left','lid_magnet_right']
axis=Axis((0,60.5,128),(1,0,0));motion=[]
for deg in range(0,101,5):
 for name in moving:
  fixed=[n for n in p if n not in moving] if name=='upper_binding' else ['central_binding','buckle']
  shape=p[name].rotate(axis,-deg)
  for target in fixed:
   v=overlap(shape,p[target])
   if v>1e-5:motion.append([deg,name,target,v])
 print('opening',deg,'hits',len(motion),flush=True)
r={'revision':rev,'step_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'baseline_step_sha256':hashlib.sha256(Path(baseline).read_bytes()).hexdigest(),'all_valid':all(s.is_valid for s in p.values()),'pairs_screened':378,'closed_overlaps':hits,'bottom_region_z_mm':[-.1,1],'bottom_symmetric_difference_mm3':bottom_delta,'tongue_back_max_contact_distance_mm':max(contact),'opening_angles_deg':list(range(0,101,5)),'changed_envelope_motion_collisions':motion,'scope':'Exact closed B-rep and discrete changed-part motion samples; no continuous sweep or physical load test.'}
r['passed']=r['all_valid'] and not hits and bottom_delta<1e-5 and max(contact)<1e-5 and not motion
Path('design/archive_handbag/verification/binding-thickening-check.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2),flush=True)
assert r['passed']
