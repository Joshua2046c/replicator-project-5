from math import sqrt, radians
w=param('width',185.0);h=param('height',49.0);R=param('spine_radius',57.6133333333333)
ft=param('shell_thickness',3.5);cheek=param('cheek_thickness',2.0)
top=param('top_from_axis',3.0);ey=param('end_y',-3.65);seam=param('square_rear_y',-0.15);roof=param('lip_thickness',2.2)
b=top-h;cz=(top+b)/2;cy=ey+sqrt(R*R-h*h/4)
outer=Pos(0,cy,cz)*Rot(0,90,0)*Cylinder(R,w)
shape=(outer-Pos(0,cy+ft,cz)*Rot(0,90,0)*Cylinder(R,w+2))&Pos(0,ey,cz)*Box(w,24,h)
for s in [-1,1]:
 x=s*(w/2-cheek/2)
 shape+=(Pos(x,cy,cz)*Rot(0,90,0)*Cylinder(R,cheek))&Pos(x,(ey-12+seam)/2,cz)*Box(cheek,seam-ey+12,h)
shape+=outer&Pos(0,(ey-12+seam)/2,top-roof/2)*Box(w,seam-ey+12,roof)
mx=param('magnet_x',54.5);my=param('magnet_y',1.55)
od=param('magnet_mount_diameter',11.3);mh=param('magnet_mount_height',5.4);pd=param('magnet_pocket_diameter',7.3);dep=param('magnet_pocket_depth',3.2)
for s in [-1,1]:
 shape+=(Pos(s*mx,my,b+mh/2)*Cylinder(od/2,mh))&outer
 shape-=Pos(s*mx,my,b-0.1)*Cylinder(pd/2,dep+0.1,align=(Align.CENTER,Align.CENTER,Align.MIN))
bw=param('binding_width',45.0);bt=param('binding_recess',1.0)
band=(outer-Pos(0,cy+bt,cz)*Rot(0,90,0)*Cylinder(R,w+2))&Pos(0,ey,cz)*Box(bw,24,h)
band+=Pos(0,(ey-12+seam)/2,top-bt/2)*Box(bw,seam-ey+12,bt)
shape-=band
mw=param('mark_width',3.0);mhh=param('mark_height',20.0);xx=param('mark_x',-66.5);pitch=param('mark_pitch',13.0);md=param('mark_depth',1.2);mc=param('mark_clearance',0.15)
for x in [xx,xx+pitch]:
 cut=Pos(x,cy,cz)*Rot(0,90,0)*Cylinder(R+2,mw+2*mc)-Pos(x,cy,cz)*Rot(0,90,0)*Cylinder(R-md,mw+2*mc+2)
 shape-=cut&Pos(x,ey,cz)*Box(mw+2*mc,30,mhh+2*mc)
# Local internal relief permits the first 12 degrees of outward unfolding.
from math import tan
relief_angle=param('opening_relief_deg',30.0)
slope=tan(radians(relief_angle))
relief=extrude(Plane.YZ*Polygon((seam,0),(20,0),(20,20),(seam-slope*20,20),align=None),amount=w+2,both=True)
shape-=relief

r=param('knuckle_outer_radius',3.0);bore=param('pin_bore_diameter',3.4);fork_l=param('extended_fork_length',52.0);fork_x=29.4+0.6+fork_l/2
web_d=param('web_depth',4.5);web_h=param('web_height',3.0)
for s in [-1,1]:
 shape+=Pos(s*fork_x,-web_d/2,0)*Box(fork_l,web_d,web_h)
 shape+=Pos(s*fork_x,0,0)*Rot(0,90,0)*Cylinder(r,fork_l)
clear_r=param('middle_clearance_radius',3.3);clear_l=param('central_clearance_length',59.8)
shape-=Rot(0,90,0)*Cylinder(clear_r,clear_l)
cap_r=param('end_cap_clearance_radius',3.2);cap_x=param('extended_cap_center',84.9);cap_l=param('cap_clearance_length',4.4)
for s in [-1,1]: shape-=Pos(s*cap_x,0,0)*Rot(0,90,0)*Cylinder(cap_r,cap_l)
shape-=Rot(0,90,0)*Cylinder(bore/2,w+2)
assert shape.is_valid and len(shape.solids())==1
from OCP.ShapeUpgrade import ShapeUpgrade_ShapeDivideAngle, ShapeUpgrade_UnifySameDomain
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder
angle=param('surface_max_angle_deg',2.0)
divide=ShapeUpgrade_ShapeDivideAngle(radians(angle),shape.wrapped);divide.Perform()
split=Solid.cast(divide.Result());unify=ShapeUpgrade_UnifySameDomain(split.wrapped,True,True,False)
for face in split.faces():
 surface=BRepAdaptor_Surface(face.wrapped)
 if surface.GetType()==GeomAbs_Cylinder and abs(surface.Cylinder().Radius()-R)<2:
  for edge in face.edges(): unify.KeepShape(edge.wrapped)
unify.Build();shape=Solid.cast(unify.Shape())
assert shape.is_valid and len(shape.solids())==1
publish('fold_spine',shape,'内轴折叠上层书脊',material='petg')
