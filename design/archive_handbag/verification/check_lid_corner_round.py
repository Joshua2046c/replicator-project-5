"""Check small rear rounds and preservation of the previously tested assembly."""
import json,math,hashlib,sys
from pathlib import Path
from build123d import import_step,Pos,Box,Vertex
oldpath,newpath,revision=sys.argv[1:]
old={s.label:s.clean() for s in import_step(oldpath).children}
a=import_step(newpath);new={s.label:s.clean() for s in a.children}
def vol(s):return abs(s.volume) if s else 0
unchanged={n:vol(old[n]-new[n])+vol(new[n]-old[n]) for n in old if n!='lid'}
added=vol(new['lid']-old['lid']);removed=old['lid']-new['lid']
mask=Pos(-109.5,56.5,159.3)*Box(1.002,1.002,63)+Pos(109.5,56.5,159.3)*Box(1.002,1.002,63)
probes=[]
for side in [-1,1]:
 for z,radius in [(188.5,1),(190,.6),(161.3,.75),(159.3,.3)]:
  for deg in [0,15,30,45,60,75,90]:
   angle=math.radians(deg);p=Vertex(side*(109+radius*math.cos(angle)),56+radius*math.sin(angle),z)
   probes.append({'side':side,'z':z,'radius_mm':radius,'angle_deg':deg,'distance_mm':new['lid'].distance_to(p)})
r={'revision':revision,'step_sha256':hashlib.sha256(Path(newpath).read_bytes()).hexdigest(),'baseline_step_sha256':hashlib.sha256(Path(oldpath).read_bytes()).hexdigest(),'objects':len(new),'solids':len(a.solids()),'all_valid':all(s.is_valid for s in new.values()),'unchanged_other_objects_mm3':unchanged,'added_lid_volume_mm3':added,'removed_lid_volume_mm3':vol(removed),'change_outside_two_corners_mm3':vol(removed-mask),'round_surface_probes':probes,'collision_reasoning':'The new lid is a subset of the previously validated lid, all other bodies and placements identical. Therefore prior collision-free closed and sampled motion poses remain collision-free. Baseline evidence: lid-detail-check.json.'}
r['passed']=r['all_valid'] and len(new)==28 and len(a.solids())==31 and max(unchanged.values())<1e-5 and added<1e-5 and r['change_outside_two_corners_mm3']<1e-5 and vol(removed)>0 and max(q['distance_mm'] for q in probes)<1e-5
Path('design/archive_handbag/verification/lid-corner-round-check.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k not in ['round_surface_probes','unchanged_other_objects_mm3']},indent=2));assert r['passed']
