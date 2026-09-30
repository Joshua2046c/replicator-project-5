from math import sqrt
R=param('spine_common_radius',88.33333333333333)
w=param('lower_binding_width',30.0);t=param('lower_binding_thickness',1.0)
front=param('lower_binding_front_y',-51.0);rear=param('lower_binding_rear_y',57.0);bottom=param('lower_binding_base_z',0.0);backtop=param('lower_binding_back_top',123.5)
out=param('central_binding_outward',2.0)
foot=param('central_binding_base_transition',4.0)
cy=front+sqrt(R*R-32.0**2)
band=Pos(0,(front-8+rear)/2,bottom+t/2)*Box(w,rear-front+8,t)&Pos(0,cy,32)*Rot(0,90,0)*Cylinder(R,w)
band+=Pos(0,rear-t/2,backtop/2)*Box(w,t,backtop)
for z,h in [(32.0,64.0),(96.0,64.0)]:
 cy=front+sqrt(R*R-h*h/4)
 strip=(Pos(0,cy,z)*Rot(0,90,0)*Cylinder(R,w)-Pos(0,cy+t,z)*Rot(0,90,0)*Cylinder(R,w+2))&Pos(0,front,z)*Box(w,20,h)
 band+=strip
 # Add material outward while keeping the bottom footprint unchanged.
 raised=(Pos(0,cy-out,z)*Rot(0,90,0)*Cylinder(R,w)-Pos(0,cy+t,z)*Rot(0,90,0)*Cylinder(R,w+2))&Pos(0,front-out/2,z)*Box(w,20+out,h)
 if z==32.0:
  zb=bottom+t
  ya=cy-sqrt(R*R-(zb-z)**2)
  yb=cy-sqrt(R*R-(zb+foot-z)**2)-out
  taper=extrude(Plane.YZ*Polygon((ya,zb),(yb,zb+foot),(front-20,h),(front+5,h),(front+5,zb),align=None),amount=w/2,both=True)
  raised &= taper
 band+=raised
# Back outward layer fades to zero above the unchanged bottom band.
band+=extrude(Plane.YZ*Polygon((rear-t,bottom+t),(rear,bottom+t),(rear+out,bottom+t+foot),(rear+out,backtop),(rear-t,backtop),align=None),amount=w/2,both=True)
c=param('central_binding_outer_chamfer',0.4)
for yy,sg in [(front,-1),(rear,1)]:
 band-=extrude(Plane.YZ*Polygon((yy-sg*c,bottom),(yy+sg*2,bottom),(yy+sg*2,bottom+c+2),align=None),amount=w+2,both=True)
assert len(band.solids())==1
# Analytic surface refinement for smooth display; small holes retain their original topology.
from OCP.ShapeUpgrade import ShapeUpgrade_ShapeDivideAngle, ShapeUpgrade_UnifySameDomain
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder, GeomAbs_Cone
from math import radians
angle=param('spine_surface_max_angle_deg',2.0)
def refine_spine(shape):
    divide=ShapeUpgrade_ShapeDivideAngle(radians(angle),shape.wrapped)
    divide.Perform()
    split=Solid.cast(divide.Result())
    unify=ShapeUpgrade_UnifySameDomain(split.wrapped,True,True,False)
    for face in split.faces():
        surface=BRepAdaptor_Surface(face.wrapped)
        kind=surface.GetType()
        radius=surface.Cylinder().Radius() if kind==GeomAbs_Cylinder else (surface.Cone().RefRadius() if kind==GeomAbs_Cone else 0)
        if abs(radius-R)<2:
            for edge in face.edges(): unify.KeepShape(edge.wrapped)
    unify.Build()
    result=Solid.cast(unify.Shape())
    assert result.is_valid and len(result.solids())==1
    return result
# Shared hidden square locating interface; all dimensions in mm.
pegw=param('buckle_mount_peg_width',3.0);pegl=param('buckle_mount_peg_length',2.0)
pegx=param('buckle_mount_center_x',0.0);pegz=param('buckle_mount_center_z',96.0)
pegy=-51.0+sqrt(R*R-32.0**2)-sqrt(R*R-(pegz-96.0)**2)
clear=param('buckle_mount_side_clearance',0.15);endgap=param('buckle_mount_end_clearance',0.2)
socket=Pos(pegx,pegy+(pegl+endgap-out-0.05)/2,pegz)*Box(pegw+2*clear,pegl+endgap+out+0.05,pegw+2*clear)
band-=socket
band=refine_spine(band)
publish('central_binding',band,'连续圆弧贴面带')
w2=param('upper_binding_width',30.0);t2=param('upper_binding_thickness',1.0);seam=param('upper_binding_front_base',128.6);top=param('upper_binding_top_z',190.0);backbase=param('upper_binding_back_base',134.0);ey=param('upper_binding_front_y',-51.0);ry=param('upper_binding_rear_y',57.0)
out2=param('upper_binding_outward',2.0)
h=top-seam;z=(top+seam)/2;cy=ey+sqrt(R*R-h*h/4)
strip=(Pos(0,cy-out2,z)*Rot(0,90,0)*Cylinder(R,w2)-Pos(0,cy+t2,z)*Rot(0,90,0)*Cylinder(R,w2+2))&Pos(0,ey-out2/2,z)*Box(w2,20+out2,h)
strip+=Pos(0,(ey+ry)/2,top+(out2-t2)/2)*Box(w2,ry-ey+2*out2,t2+out2)
strip+=Pos(0,ry+(out2-t2)/2,(top+out2+backbase)/2)*Box(w2,t2+out2,top+out2-backbase)
c2=param('upper_binding_outer_chamfer',0.4)
for yy,sg in [(ey-out2,-1),(ry+out2,1)]:
 strip-=extrude(Plane.YZ*Polygon((yy-sg*c2,top+out2),(yy+sg*2,top+out2),(yy+sg*2,top+out2-c2-2),align=None),amount=w2+2,both=True)
rise=param('upper_binding_crown_radius',3.0);peak=param('upper_binding_crown_y',10.0);start=param('upper_binding_transition_front_y',-40.0)
top+=out2
# Legacy crown_radius remains the editable rise. Only the terminal PLAN outline is round.
a=(0,start,top);b=(0,peak,top+rise)
arc=Edge.make_bezier(a,(0,start+(peak-start)*.45,top),(0,peak-(peak-start)*.25,top+rise),b)
wire=Wire([arc,Edge.make_line(b,(0,peak,top-t2/2)),Edge.make_line((0,peak,top-t2/2),(0,start,top-t2/2)),Edge.make_line((0,start,top-t2/2),a)])
fade=Pos(-w2/2,0,0)*extrude(Face(wire),amount=w2,dir=(1,0,0))
cap=Pos(0,peak,top-t2/2)*Cylinder(w2/2,rise+t2/2,align=(Align.CENTER,Align.CENTER,Align.MIN))
cap &= Pos(0,peak+w2/4,top+(rise-t2/2)/2)*Box(w2,w2/2,rise+t2/2)
strip+=fade+cap
assert len(strip.solids())==1
angle=param('upper_binding_surface_max_angle_deg',1.0)
strip=refine_spine(strip)
publish('upper_binding',strip,'局部半圆端头顶带')