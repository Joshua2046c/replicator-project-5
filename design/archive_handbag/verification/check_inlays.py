"""Read-only probes of committed STEP inlays and crown; never creates deliverable geometry."""
import sys,json,math
from pathlib import Path
from build123d import import_step,Pos,Box,Vertex
root=Path(sys.argv[1]);build=int(sys.argv[2]);s={p.stem:import_step(str(p)) for p in (root/'validated/objects').rglob('*.step')}
def v(a,b):
 q=a&b
 return max(0,q.volume) if q is not None else 0
checks=[]
def probe(label,n,p,material):
 val=v(s[n],Pos(*p)*Box(.02,.02,.02));ok=val>7.9e-6 if material else val<1e-9
 checks.append(dict(label=label,object=n,point=p,volume=val,passed=ok))
for x in [-84,-75,-66]:
 for y in [-12,4,20]:
  probe('roof_floor','lid',(x,y,188.4),True)
  probe('roof_pocket','lid',(x,y,189.5),False)
probe('nameplate_top','nameplate',(-75,4,189.98),True)
probe('bed_gap','nameplate',(-75,4,189.05),False)
R=88+1/3;floor=[];fits=[]
for name,host,z,H in [('green_marks','blue_spine',32,64),('blue_marks','blue_spine',96,64),('pink_marks','lid',159.3,61.4)]:
 cy=-51+math.sqrt(R*R-H*H/4)
 for xx in [-84,-71]:
  for dz in [-12,0,12]:
   y=cy-math.sqrt((R-1.2)**2-dz*dz)
   probe('slot_air',host,(xx,y-.1,z+dz),False)
   probe('slot_floor',host,(xx,y+.1,z+dz),True)
   # Straight Y remaining wall, measured at each slot sample.
   inner=cy+3.5-math.sqrt(R*R-dz*dz)
   floor.append(inner-y)
   probe('embedded_inlay',name,(xx,y-.3,z+dz),True)
 fits.append(dict(object=name,host=host,minimum_clearance=s[name].distance_to(s[host]),overlap=v(s[name],s[host])))
fits.append(dict(object='nameplate',host='lid',minimum_clearance=s['nameplate'].distance_to(s['lid']),overlap=v(s['nameplate'],s['lid'])))
insert=[]
for name,host,axis in [('green_marks','blue_spine','y'),('blue_marks','blue_spine','y'),('pink_marks','lid','y'),('nameplate','lid','z')]:
 for d in [0,.1,.3,.6,1,1.5,2,3,5,10]:
  shift=Pos(0,-d,0) if axis=='y' else Pos(0,0,d)
  insert.append(dict(object=name,withdraw_mm=d,overlap=v(shift*s[name],s[host])))
cr=39.;samples=[]
for x in [-14,-10,0,10,14]:
 expected=190+3-cr+math.sqrt(cr*cr-x*x)
 distance=s['upper_binding'].distance_to(Vertex(x,10,expected))
 inside=v(s['upper_binding'],Pos(x,10,expected-.04)*Box(.02,.02,.02))
 outside=v(s['upper_binding'],Pos(x,10,expected+.04)*Box(.02,.02,.02))
 samples.append(dict(x=x,expected=expected,surface_distance=distance,below_material=inside,above_material=outside,passed=distance<1e-5 and inside>7.9e-6 and outside<1e-9))

report=dict(buildNumber=build,source_build_path=str(root),probes=checks,nameplate_size_mm=[20,36,.9],nameplate_pocket_mm=[20.3,36.3,1],roof_remaining_floor_mm=1.2,spine_depth_mm=1.2,spine_embed_mm=1.1,spine_bottom_allowance_mm=.1,spine_side_clearance_mm=.15,spine_remaining_wall_y_min_mm=min(floor),fits=fits,insertion_samples=insert,circular_cross_section=samples,limitations='nominal geometry only; loose-fit inlays need nonstructural adhesive retention; no glue or load validation')
report['status']='pass' if all(c['passed'] for c in checks+samples) and all(c['overlap']<.001 for c in fits+insert) and min(floor)>2.28 and abs(s['nameplate'].bounding_box().max.Z-190)<1e-5 else 'failed'
Path('design/archive_handbag/verification/inlay-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(report['status'], 'minimum spine floor',min(floor),'fit clearances',fits)
assert report['status']=='pass'
