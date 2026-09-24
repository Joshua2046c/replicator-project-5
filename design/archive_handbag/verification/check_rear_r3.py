"""Check full-height R3 rear rounds and preservation of the previously tested assembly."""
import json,math,hashlib,sys
from pathlib import Path
from build123d import import_step,Pos,Box,Vertex
oldpath,newpath,revision=sys.argv[1:]
old={s.label:s.clean() for s in import_step(oldpath).children}
a=import_step(newpath);new={s.label:s.clean() for s in a.children}
def vol(s):
 if not s:return 0
 return abs(s.volume) if hasattr(s,"volume") else sum(vol(x) for x in s)
def outside(s,mask):
 if not s:return 0
 return vol(s-mask) if hasattr(s,"wrapped") else sum(outside(x,mask) for x in s)
changed=['lid','body','bottom_panel']
unchanged={n:vol(old[n]-new[n])+vol(new[n]-old[n]) for n in old if n not in changed}
mask=Pos(-108.5,55.5,95)*Box(3.002,3.002,192)+Pos(108.5,55.5,95)*Box(3.002,3.002,192)
changes={n:{'added_mm3':vol(new[n]-old[n]),'removed_mm3':vol(old[n]-new[n]),'outside_corner_mm3':outside(old[n]-new[n],mask)} for n in changed}
probes=[]
for side in [-1,1]:
 for name,z,radius in [('lid',188.5,3),('lid',190,2.6),('lid',161.3,2.75),('lid',159.3,2.3),('body',62,3),('body',126,3),('body',34,2.75),('body',98,2.75),('body',32,2.3),('body',96,2.3),('body',64,2.55),('bottom_panel',2,3),('bottom_panel',0,2.6)]:
  for deg in [0,15,30,45,60,75,90]:
   angle=math.radians(deg);p=Vertex(side*(107+radius*math.cos(angle)),54+radius*math.sin(angle),z)
   probes.append({'object':name,'side':side,'z':z,'radius_mm':radius,'angle_deg':deg,'distance_mm':new[name].distance_to(p)})
r={'revision':revision,'step_sha256':hashlib.sha256(Path(newpath).read_bytes()).hexdigest(),'baseline_step_sha256':hashlib.sha256(Path(oldpath).read_bytes()).hexdigest(),'objects':len(new),'solids':len(a.solids()),'all_valid':all(s.is_valid for s in new.values()),'unchanged_other_objects_mm3':unchanged,'local_changes':changes,'round_surface_probes':probes,'collision_reasoning':'Each changed part is a subset of its previously validated shape; all other bodies and placements are identical. Therefore prior collision-free closed and sampled motion poses remain collision-free. Baseline evidence: lid-corner-round-check.json and previous handoff receipt; lid-detail-check.json holds sampled motion evidence.'}
r['passed']=r['all_valid'] and len(new)==28 and len(a.solids())==31 and max(unchanged.values())<1e-5 and all(q['added_mm3']<1e-5 and q['outside_corner_mm3']<1e-5 and q['removed_mm3']>0 for q in changes.values()) and max(q['distance_mm'] for q in probes)<1e-5
Path('design/archive_handbag/verification/rear-r3-check.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k not in ['round_surface_probes','unchanged_other_objects_mm3']},indent=2));assert r['passed']
