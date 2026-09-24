"""Read-only exact committed STEP probes for the12 macro-edge regions and raised details."""
import json,sys,math
from pathlib import Path
from build123d import import_step,Pos,Box,Vertex
root=Path(sys.argv[1]);build=int(sys.argv[2]);s={p.stem:import_step(str(p)) for p in (root/'validated/objects').rglob('*.step')}
def v(a,p):
 q=a&p
 return max(0,q.volume) if q is not None else 0
checks=[]
def probe(label,obj,air,land):
 av=v(s[obj],Pos(*air)*Box(.04,.04,.04));lv=v(s[obj],Pos(*land)*Box(.04,.04,.04))
 checks.append(dict(region=label,object=obj,removed_material_mm3=av,remaining_material_mm3=lv,passed=av<1e-8 and lv>.000063))
#4top and4bottom regions, with each width-direction edge sampled outside the central decorative channel.
for sg in [-1,1]:
 probe('top_side_'+str(sg),'lid',(sg*109.95,0,189.95),(sg*109.3,0,189.3))
 probe('bottom_side_'+str(sg),'bottom_panel',(sg*109.95,0,.05),(sg*109.3,0,.7))
for label,y,inside in [('front',-50.95,-50.3),('rear',56.95,56.3)]:
 probe('top_'+label,'lid',(40,y,189.95),(40,inside,189.3))
 probe('bottom_'+label,'bottom_panel',(40,y,.05),(40,inside,.7))
#Two rear vertical regions: lower cover, recessed page land and upper cover.
for sg in [-1,1]:
 for obj,zz,x,y in [('body',66,110,57),('body',99,109.75,56.75),('lid',188,110,57)]:
  probe('rear_vertical_'+str(sg)+'_'+str(zz),obj,(sg*(x-.05),y-.05,zz),(sg*(x-.7),y-.7,zz))
#Two front vertical regions follow all three curved spines.
R=88+1/3
for sg in [-1,1]:
 for obj,cz,hh in [('blue_spine',32,64),('blue_spine',96,64),('lid',159.3,61.4)]:
  # Lower curved outer edges now belong to the one-piece sliding side boards.
  if obj=='blue_spine':obj='side_left' if sg<0 else 'side_right'
  y=-51+math.sqrt(R*R-hh*hh/4)-R
  # At the lid center this crosses a horizontal page groove: sample inside its0.7mm recess, not on its boundary.
  probe('front_vertical_'+str(sg)+'_'+str(cz),obj,(sg*109.95,y+.05,cz),(sg*109.1,y+.9,cz))
# Flat-width crown with local semicircular plan end; verify forward blend height.
crown=s['upper_binding'];sections=[]
for yy in [-40,-30,-20,-10,0,5,10]:
 slab=crown&Pos(0,yy,192)*Box(1,.01,6)
 sections.append({'y':yy,'top_z':slab.bounding_box().max.Z})
height=crown.bounding_box().max.Z
cy=-51+math.sqrt(R*R-32**2);z=99.9;u=(z-78)/22;raised_y=cy-math.sqrt(R*R-(z-96)**2)-2*(3*u*u-2*u*u*u)-.5
metal=v(s['buckle'],Pos(0,raised_y,z)*Box(1,.1,.1))
report={'buildNumber':build,'source_build_path':str(root),'macro_regions_count':12,'macro_edge_probes':checks,'crown_sections':sections,'crown_top_z_mm':height,'tongue_tip_region_material_mm3':metal,'tongue_bottom_root_single_solid':len(s['buckle'].solids())==1,'status':'pass' if all(c['passed'] for c in checks) and abs(height-193)<1e-4 and all(b['top_z']>=a['top_z'] for a,b in zip(sections,sections[1:])) and metal>.009 and len(s['buckle'].solids())==1 else 'failed','scope':'Outer edge regions only:4top+4bottom+2front curved+2rear vertical; horizontal page-groove fine edges and functional mating surfaces excluded. Not carrying certification.'}
Path('design/archive_handbag/verification/cosmetic-edge-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
assert report['status']=='pass'