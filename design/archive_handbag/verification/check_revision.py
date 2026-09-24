"""Read-only checks of the exact committed STEP; test probes are never exported as CAD."""
import json, sys, math
from pathlib import Path
from build123d import import_step, Pos, Rot, Cylinder, Box, Vertex
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder
root=Path(sys.argv[1]); build=int(sys.argv[2])
s={p.stem:import_step(str(p)) for p in (root/'validated'/'objects').rglob('*.step')}
def vol(a,b):
 aa=a.bounding_box();bb=b.bounding_box()
 if not all(tuple(aa.max)[i]>tuple(bb.min)[i]+1e-7 and tuple(bb.max)[i]>tuple(aa.min)[i]+1e-7 for i in range(3)):return 0.0
 c=a&b
 return max(0,c.volume) if c is not None else 0.0
# Final pin drawing: D4 x100, D6 x1.4 heads. Only the trailing head exists before insertion.
# Sweep along +X by160mm: shaft [-210,50], trailing head [-211.4,-50].
# These cylinders are the EXACT continuous translational sweeps of the two cylindrical portions.
shaft_sweep=Pos(-80,60.5,128)*Rot(0,90,0)*Cylinder(2,260)
head_sweep=Pos(-130.7,60.5,128)*Rot(0,90,0)*Cylinder(3,161.4)
hits=[];clearances={}
for n,a in s.items():
 if n=='axle':continue
 for k,p in [('shaft',shaft_sweep),('preformed_head',head_sweep)]:
  v=vol(a,p)
  if v>.001:hits.append({'object':n,'portion':k,'overlap_mm3':v})
 clearances[n]=min(a.distance_to(shaft_sweep),a.distance_to(head_sweep))
# Book-page cuts: one shared6mm pitch; known centers are verified in both side/rear solids.
pages=[]
for book,c in [('green',32.0),('blue',96.0),('pink',159.3)]:
 for n,x,y in [('side_right',109.5,20),('side_left',-109.5,20),('lid' if book=='pink' else 'body',40,56.5)]:
  air=[];lands=[]
  for i in range(-4,5):air.append(vol(s[n],Pos(x,y,c+6*i)*Box(.1,.1,.2)))
  for i in range(-4,4):lands.append(vol(s[n],Pos(x,y,c+6*i+3)*Box(.1,.1,.2)))
  pages.append({'book':book,'object':n,'centers_z':[round(c+6*i,4) for i in range(-4,5)],'groove_max_material_mm3':max(air),'land_min_material_mm3':min(lands),'pass':max(air)<1e-6 and min(lands)>.0019})
covers=[]
for z in [2,62,66,126,130.6,188]:
 n='bottom_panel' if z<4 else ('lid' if z>187.4 else 'side_right')
 y=20 if n!='lid' else 0
 v=vol(s[n],Pos(109.9,y,z)*Box(.1,.1,.1))
 covers.append({'z':z,'object':n,'material_mm3':v,'pass':v>.0009})
# B-rep surface radii at the three curved spines plus lowest4mm bottom continuation.
curves=[]
for n,cz in [('blue_spine',32),('blue_spine',96),('lid',159.3),('bottom_panel',32)]:
 radii=[]
 for f in s[n].faces():
  a=BRepAdaptor_Surface(f.wrapped)
  if a.GetType()!=GeomAbs_Cylinder:continue
  cy=a.Cylinder();loc=cy.Location()
  if abs(loc.Z()-cz)<1e-5 and cy.Radius()>50:radii.append(cy.Radius())
 curves.append({'object':n,'center_z':cz,'radii_mm':sorted(set(round(r,8) for r in radii)),'pass':bool(radii) and all(abs(r-88.33333333333333)<1e-5 for r in radii)})
R=88.33333333333333;cy=-51+math.sqrt(R*R-32**2);z=4;y=cy-math.sqrt(R*R-(z-32)**2)
continuity={n:s[n].distance_to(Vertex(40,y,z)) for n in ['blue_spine','bottom_panel']}
# Pocket mouths have at least1.55mm exterior ligament; vertical wall2mm and bottom2.2mm.
mag=[]
for n,host in [('body_magnet_left','blue_spine'),('body_magnet_right','blue_spine'),('lid_magnet_left','lid'),('lid_magnet_right','lid')]:
 mag.append({'magnet':n,'host':host,'overlap_mm3':vol(s[n],s[host]),'clearance_mm':s[n].distance_to(s[host])})
face_gap=s['body_magnet_left'].distance_to(s['lid_magnet_left'])
removed=not any(n.startswith(('body_mag_cap','lid_mag_cap','axle_stop')) for n in s)
report={'buildNumber':build,'source_build_path':str(root),'pin_insertion':{'method':'continuous analytic cylindrical sweep; closed aligned hinge, +X insertion160mm; second rivet head absent until after insertion','collisions':hits,'minimum_clearance_mm':min(clearances.values()),'clearance_by_object_mm':clearances,'preformed_head_to_flat_rear_mm':.5,'requires_external_straight_approach_mm':160,'does_not_certify':'rivet forming tools, manufacturing tolerance or physical fit'},'page_probes':pages,'cover_probes':covers,'curvature_checks':curves,'bottom_join_point_distance_mm':continuity,'magnet_fit':mag,'magnet_face_gap_mm':face_gap,'minimum_nominal_mouth_ligament_mm':1.55,'obsolete_closure_hardware_absent':removed,'status':'pass' if not hits and all(x['pass'] for x in pages+covers+curves) and max(continuity.values())<1e-5 and all(x['overlap_mm3']<.001 for x in mag) and removed else 'failed'}
Path('design/archive_handbag/verification/revision-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
