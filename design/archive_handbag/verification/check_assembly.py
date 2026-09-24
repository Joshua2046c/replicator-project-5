"""Read-only exact committed STEP checks; never generates or changes CAD geometry."""
import sys,json,itertools
from pathlib import Path
from build123d import import_step,Pos,Box
root=Path(sys.argv[1]);build=int(sys.argv[2]);out=Path('design/archive_handbag/verification')
s={p.stem:import_step(str(p)) for p in (root/'validated'/'objects').rglob('*.step')}
def bb_hit(a,b):
 aa=a.bounding_box();bb=b.bounding_box()
 return all(tuple(aa.max)[i]>tuple(bb.min)[i]+1e-7 and tuple(bb.max)[i]>tuple(aa.min)[i]+1e-7 for i in range(3))
def vol(a,b):
 if not bb_hit(a,b):return 0.0
 c=a&b
 return max(0,c.volume) if c is not None else 0.0
hits=[];exact=0
for a,b in itertools.combinations(s,2):
 if not bb_hit(s[a],s[b]):continue
 exact+=1;v=vol(s[a],s[b])
 if v>0.001:hits.append({'a':a,'b':b,'volume_mm3':v})
r={'buildNumber':build,'source_build_path':str(root),'objects':len(s),'solids':sum(len(a.solids()) for a in s.values()),'pairs_screened':len(s)*(len(s)-1)//2,'exact_bbox_overlap_pairs':exact,'collisions':hits,'solid_validity':{n:a.is_valid for n,a in s.items()},'status':'pass' if not hits and all(a.is_valid for a in s.values()) else 'failed'}
(out/'closed-pose-check.json').write_text(json.dumps(r,indent=2)+'\n');print({k:v for k,v in r.items() if k!='solid_validity'},flush=True)
contacts=[]
for a,b in [('central_binding','blue_spine'),('central_binding','bottom_panel'),('central_binding','body'),('upper_binding','lid'),('buckle','central_binding'),('ring_nut_right','backplate_right'),('ring_nut_left','backplate_left'),('thumb_screw_right','pivot_washer_right'),('thumb_screw_left','pivot_washer_left')]:
 contacts.append({'a':a,'b':b,'distance_mm':s[a].distance_to(s[b]),'overlap_mm3':vol(s[a],s[b])})
insert=[]
for name in ['blue_spine','body']:
 for dz in [0,0.4,1,2,3,5]:insert.append({'part':name,'lift_mm':dz,'overlap_bottom_mm3':vol(Pos(0,0,dz)*s[name],s['bottom_panel'])})
# Both peened heads must contact the fixed knuckles before the pin can slide free.
retention={str(dx):vol(Pos(dx,0,0)*s['axle'],s['body']) for dx in [-1.2,1.2]}
# Continuous matched uppermost182mm page-groove probes, outside groove material absent and deeper wall remains.
probes=[]
# Rear lid probe at X40 avoids the central30mm decorative-strip recess.
for name,x,y in [('side_right',109.8,20),('side_left',-109.8,20),('lid',40,56.8)]:
 absent=vol(s[name],Pos(x,y,182)*Box(.1,.1,.4))
 inside=(x-0.4 if x>0 else x+0.4,y) if name!='lid' else (x,y-0.4)
 present=vol(s[name],Pos(inside[0],inside[1],182)*Box(.1,.1,.4))
 probes.append({'object':name,'groove_air_volume_mm3':absent,'wall_material_volume_mm3':present})
r={'buildNumber':build,'source_build_path':str(root),'contacts':contacts,'panel_insertion':insert,'thumb_screw_solids':{n:len(s[n].solids()) for n in ['thumb_screw_left','thumb_screw_right']},'axle_pull_1_2mm_blocking_mm3':retention,'upper182mm_groove_probes':probes,'deleted_hardware_absent':not any(n.startswith(('axle_stop','ring_bolt','thumb_nut')) for n in s),'front_panel_solid_count':len(s['blue_spine'].solids()),'status':'pass' if all(c['overlap_mm3']<.001 and c['distance_mm']<1e-5 for c in contacts) and all(c['overlap_bottom_mm3']<.001 for c in insert) and all(v>.001 for v in retention.values()) and all(p['groove_air_volume_mm3']<1e-6 and p['wall_material_volume_mm3']>.003 for p in probes) else 'failed','note':'Nominal rigid B-rep geometry; thread shapes simplified; no torque, thread strength, creep, magnetic force, watertightness or physical load certification.'}
(out/'integral-panel-contact-check.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))