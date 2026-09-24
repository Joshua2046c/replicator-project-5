"""Verify plain upper spine ends, paired clearance arcs and full lid motion from exact STEP."""
import json,math,sys,hashlib
from pathlib import Path
from itertools import combinations
from build123d import import_step,Plane,mirror,Pos,Box,Vertex,Axis
path,revision=sys.argv[1:]
assembly=import_step(path)
p={s.label:s.clean() for s in assembly.children}
def volume(a,b):
 aa=a.bounding_box();bb=b.bounding_box()
 if not all(tuple(aa.max)[i]>tuple(bb.min)[i]+1e-7 and tuple(bb.max)[i]>tuple(aa.min)[i]+1e-7 for i in range(3)):return 0
 x=a&b
 return abs(x.volume) if x else 0
hits=[]
for a,b in combinations(p,2):
 v=volume(p[a],p[b])
 if v>1e-5:hits.append({'a':a,'b':b,'volume_mm3':v})
R=88+1/3;cy=-51+math.sqrt(R*R-32**2)
probes=[]
for sign in [-1,1]:
 for z in [5,16,32,48,63,64,65,80,96,112,127]:
  cz=32 if z<=64 else 96
  y=cy-math.sqrt(R*R-(z-cz)**2)
  q=Pos(sign*108,y+.35,z)*Box(.2,.2,.2)
  name='side_left' if sign<0 else 'side_right'
  probes.append({'x':sign*108,'z':z,'spine_volume_mm3':volume(q,p['blue_spine']),'side_volume_mm3':volume(q,p[name]),'lap_back_distance_mm':p['blue_spine'].distance_to(Vertex(sign*108,-47.5,z))})
gaps={n:p[n].distance_to(p['blue_spine']) for n in ['side_left','side_right']}
ref=mirror(p['side_right'],about=Plane.YZ)
delta=sum(abs(s.volume) if s else 0 for s in [p['side_left']-ref,ref-p['side_left']])
moving=['lid','upper_binding','pink_marks','nameplate','lid_magnet_left','lid_magnet_right']
axis=Axis((0,60.5,128),(1,0,0))
opening=[]
# Revalidate every moving lid component against the entire fixed assembly.
for deg in range(0,101,5):
 for name in moving:
  a=p[name].rotate(axis,-deg)
  for fixed in [n for n in p if n not in moving]:
   v=volume(a,p[fixed])
   if v>1e-5:opening.append({'angle_deg':deg,'moving':name,'fixed':fixed,'volume_mm3':v})
 print('opening',deg,'collisions',len(opening),flush=True)
removed=('thumb_screw_','eye_','pivot_','ring_nut_','backplate_')
opened={n:(s.rotate(axis,-100) if n in moving else s) for n,s in p.items() if not n.startswith(removed)}
extraction=[]
for name in ['side_left','side_right']:
 for dz in [0,.4,1,5,20,50,100,125,150,185,200]:
  a=Pos(0,0,dz)*p[name]
  for fixed,s in opened.items():
   if name==fixed:continue
   v=volume(a,s)
   if v>1e-5:extraction.append({'panel':name,'lift_mm':dz,'fixed':fixed,'volume_mm3':v})
contact=[]
for z in range(84,101):
 q=Vertex(0,cy-math.sqrt(R*R-(z-96)**2),z)
 contact.append(max(p['buckle'].distance_to(q),p['central_binding'].distance_to(q)))
arc_probes=[]
for sign in [-1,1]:
 for deg in [2,5,10,15,20,25,30]:
  a=math.radians(deg)
  lp=Vertex(sign*108.5,60.5-108*math.cos(a),128+108*math.sin(a))
  sp=Vertex(sign*108.5,60.5-107.7*math.cos(a),128+107.7*math.sin(a))
  name='side_left' if sign<0 else 'side_right'
  arc_probes.append({'side':name,'angle_deg':deg,'lid_face_distance_mm':p['lid'].distance_to(lp),'side_face_distance_mm':p[name].distance_to(sp),'paired_gap_mm':lp.distance_to(sp)})
plain=[]
for sign in [-1,1]:
 for center,name in [(32,'blue_spine'),(96,'blue_spine'),(159.3,'lid')]:
  for i in range(-4,5):
   z=center+i*6
   q=Pos(sign*109.8,-50,z)*Box(.1,.1,.4)
   plain.append({'object':name,'x':sign*109.8,'z':z,'material_mm3':volume(q,p[name])})
r={'revision':revision,'step_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'objects':len(p),'solids':len(assembly.solids()),'all_valid':all(s.is_valid for s in p.values()),'pairs_screened':len(p)*(len(p)-1)//2,'closed_collisions':hits,'front_coverage_probes':probes,'minimum_front_side_gaps_mm':gaps,'side_mirror_difference_mm3':delta,'opening_angles_deg':list(range(0,101,5)),'opening_collisions':opening,'extraction_collisions':extraction,'max_tongue_contact_distance_mm':max(contact),'scope':'Exact B-rep at discrete motion samples; no continuous-motion or load certification.'}
r['arc_clearance_probes']=arc_probes
r['plain_spine_end_probes']=plain
r['upper_side_clearance_mm']={n:p[n].distance_to(p['lid']) for n in ['side_left','side_right']}
r['passed']=all(x['material_mm3']>.00399 for x in plain) and all(max(x['lid_face_distance_mm'],x['side_face_distance_mm'])<1e-5 and abs(x['paired_gap_mm']-.3)<1e-5 for x in arc_probes) and r['all_valid'] and not hits and not opening and not extraction and delta<1e-5 and max(contact)<1e-5 and all(abs(v-.3)<1e-5 for v in gaps.values()) and all(x['spine_volume_mm3']>.00799 and x['side_volume_mm3']<1e-6 and x['lap_back_distance_mm']<1e-5 for x in probes)
Path('design/archive_handbag/verification/lid-interface-check.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k not in ['front_coverage_probes','arc_clearance_probes','plain_spine_end_probes']},indent=2),flush=True)
assert r['passed']
