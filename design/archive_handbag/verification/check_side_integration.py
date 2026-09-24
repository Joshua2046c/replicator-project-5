"""Read-only exact-build checks: integral side lobes, forward page cuts, local round band end."""
import sys,json,math
from pathlib import Path
from build123d import import_step,Pos,Box,Vertex
root=Path(sys.argv[1]);build=int(sys.argv[2]);s={p.stem:import_step(str(p)) for p in (root/'validated/objects').rglob('*.step')}
def v(a,b):
 q=a&b
 return max(0,q.volume) if q is not None else 0
checks=[]
def probe(n,label,p,material):
 a=v(s[n],Pos(*p)*Box(.04,.04,.04));checks.append(dict(object=n,label=label,point=p,volume=a,passed=a>.000063 if material else a<1e-9))
R=88+1/3;cy=-51+math.sqrt(R*R-32**2)
for sg,n in [(-1,'side_left'),(1,'side_right')]:
 for center in [32,96]:
  for i in range(-4,5):
   z=center+6*i;y=cy-math.sqrt(R*R-(z-center)**2)+.6
   probe(n,'groove_reaches_curved_edge',(sg*109.5,y,z),False)
   probe(n,'groove_has_floor',(sg*109.1,y,z),True)
  for y in [-53,-50.1,-50,-49.9,-47]:
   probe(n,'solid_land_across_former_straight_seam',(sg*109.5,y,center+3),True)
   probe(n,'page_recess_across_former_straight_seam',(sg*109.9,y,center+3),False)
  probe('blue_spine','no_duplicate_lobe',(sg*108,-55,center+3),False)
# Only terminal plan is circular; no transverse crown anywhere along the rise.
flat=[]
for y in [-30,-10,0,10,12]:
 heights=[]
 for x in [-10,0,10]:
  q=s['upper_binding']&Pos(x,y,192)*Box(.1,.1,6)
  heights.append(q.bounding_box().max.Z)
 flat.append(dict(y=y,top_z=heights,passed=max(heights)-min(heights)<1e-5))
arc=[]
for degrees in [15,45,90,135,165]:
 theta=math.radians(degrees);x=15*math.cos(theta);y=10+15*math.sin(theta)
 dist=s['upper_binding'].distance_to(Vertex(x,y,191.5))
 a=v(s['upper_binding'],Pos(14.9*math.cos(theta),10+14.9*math.sin(theta),191.5)*Box(.04,.04,.04))
 b=v(s['upper_binding'],Pos(15.1*math.cos(theta),10+15.1*math.sin(theta),191.5)*Box(.04,.04,.04))
 arc.append(dict(angle=degrees,distance=dist,inside=a,outside=b,passed=dist<1e-5 and a>.000063 and b<1e-9))
report=dict(buildNumber=build,source_build_path=str(root),side_solids={n:len(s[n].solids()) for n in ['side_left','side_right']},probes=checks,band_flat_cross_sections=flat,band_plan_end_arc=arc,side_to_front_clearance_mm={n:s[n].distance_to(s['blue_spine']) for n in ['side_left','side_right']},note='Lower two circular side regions are owned by sliding side boards. Upper lid remains independently hinged. Numeric probes corroborate visual review; no structural certification.')
report['status']='pass' if all(c['passed'] for c in checks+flat+arc) and all(k==1 for k in report['side_solids'].values()) and all(abs(k-.3)<1e-5 for k in report['side_to_front_clearance_mm'].values()) else 'failed'
Path('design/archive_handbag/verification/side-integration-check.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],report['side_solids'],report['side_to_front_clearance_mm']);print('failed',[c for c in checks+flat+arc if not c['passed']]);assert report['status']=='pass'
