# cell: brown_binding

# Overall height drives the existing 190mm design basis; stock thickness and hardware stay unchanged.
height_ratio=param('case_height',152.0)/190.0
# cell: brown_binding
# cell: brown_binding
from math import sqrt
R=param('spine_common_radius',88.33333333333333)
w=param('lower_binding_width',30.0);t=param('lower_binding_thickness',1.0)
front=param('lower_binding_front_y',-51.0);rear=param('lower_binding_rear_y',57.0);bottom=param('lower_binding_base_z',0.0);backtop=param('lower_binding_back_top',123.5)
out=param('central_binding_outward',2.0)
foot=param('central_binding_base_transition',4.0)

# Preserve the existing spine sag while shortening its chord.
sag_basis=R-sqrt(R*R-32.0**2)
R=(32.0*height_ratio)**2/(2*sag_basis)+sag_basis/2
backtop=128.0*height_ratio-(128.0-backtop)
cy=front+sqrt(R*R-(32.0*height_ratio)**2)
band=Pos(0,(front-8+rear)/2,bottom+t/2)*Box(w,rear-front+8,t)&(Pos(0,cy,32*height_ratio)*Rot(0,90,0)*Cylinder(R,w)+Pos(0,(cy+rear)/2,bottom+t/2)*Box(w,rear-cy,t))
band+=Pos(0,rear-t/2,backtop/2)*Box(w,t,backtop)
for z,h in [(32.0*height_ratio,64.0*height_ratio),(96.0*height_ratio,64.0*height_ratio)]:
 cy=front+sqrt(R*R-h*h/4)
 strip=(Pos(0,cy,z)*Rot(0,90,0)*Cylinder(R,w)-Pos(0,cy+t,z)*Rot(0,90,0)*Cylinder(R,w+2))&Pos(0,front,z)*Box(w,20,h)
 band+=strip
 # Add material outward while keeping the bottom footprint unchanged.
 raised=(Pos(0,cy-out,z)*Rot(0,90,0)*Cylinder(R,w)-Pos(0,cy+t,z)*Rot(0,90,0)*Cylinder(R,w+2))&Pos(0,front-out/2,z)*Box(w,20+out,h)
 if abs(z-32.0*height_ratio)<1e-6:
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
pegz*=height_ratio
pegy=front+sqrt(R*R-(32.0*height_ratio)**2)-sqrt(R*R-(pegz-96.0*height_ratio)**2)
clear=param('buckle_mount_side_clearance',0.15);endgap=param('buckle_mount_end_clearance',0.2)
socket=Pos(pegx,pegy+(pegl+endgap-out-0.05)/2,pegz)*Box(pegw+2*clear,pegl+endgap+out+0.05,pegw+2*clear)
band-=socket
band=refine_spine(band)
publish('central_binding',band,'连续圆弧贴面带')
w2=param('upper_binding_width',30.0);t2=param('upper_binding_thickness',1.0);seam=param('upper_binding_front_base',128.6);top=param('upper_binding_top_z',190.0);backbase=param('upper_binding_back_base',134.0);ey=param('upper_binding_front_y',-51.0);ry=param('upper_binding_rear_y',57.0)
out2=param('upper_binding_outward',2.0)
seam=128.0*height_ratio+(seam-128.0);top*=height_ratio;backbase=128.0*height_ratio+(backbase-128.0)
h=top-seam;z=(top+seam)/2;cy=ey+sqrt(R*R-h*h/4)
strip=(Pos(0,cy-out2,z)*Rot(0,90,0)*Cylinder(R,w2)-Pos(0,cy+t2,z)*Rot(0,90,0)*Cylinder(R,w2+2))&Pos(0,ey-out2/2,z)*Box(w2,20+out2,h)
strip+=Pos(0,(ey+ry)/2,top+(out2-t2)/2)*Box(w2,ry-ey+2*out2,t2+out2)
strip+=Pos(0,ry+(out2-t2)/2,(top+out2+backbase)/2)*Box(w2,t2+out2,top+out2-backbase)
c2=param('upper_binding_outer_chamfer',0.4)
for yy,sg in [(ry+out2,1)]:
 strip-=extrude(Plane.YZ*Polygon((yy-sg*c2,top+out2),(yy+sg*2,top+out2),(yy+sg*2,top+out2-c2-2),align=None),amount=w2+2,both=True)
# Round the top/front outer transverse edge before surface subdivision.
bend_radius=param('upper_binding_front_bend_radius',1.5)
bend_edges=[e for e in strip.edges().filter_by(Axis.X) if abs(e.center().Y-(ey-out2))<1e-5 and abs(e.center().Z-(top+out2))<1e-5]
assert len(bend_edges)==1
strip=fillet(bend_edges,bend_radius)
rise=param('upper_binding_crown_radius',3.0);peak=param('upper_binding_crown_y',10.0);start=param('upper_binding_transition_front_y',-40.0)
top+=out2
# One inclined plane extends through the semicircular plan end, with no flat cap.
end=peak+w2/2
assert end>start and rise>0
profile=Plane.YZ*Polygon((start,top-t2/2),(end,top-t2/2),(end,top+rise),(start,top),align=None)
ramp=extrude(profile,amount=w2/2,both=True)
footprint=Pos(0,(start+peak)/2)*Rectangle(w2,peak-start)+Pos(0,peak)*Circle(w2/2)
plan_mask=Pos(0,0,top-t2)*extrude(footprint,amount=rise+2*t2)
strip+=ramp&plan_mask
assert len(strip.solids())==1
angle=param('upper_binding_surface_max_angle_deg',1.0)
# Two independent decorations cannot bridge the rotating straight seam.
joint_y=param('binding_fold_joint_y',-49.85)
joint_gap=param('binding_fold_joint_gap',0.3)
span=param('binding_split_mask_span',400.0)
front_strip=strip & Pos(0,joint_y-joint_gap/2-span/2,top/2)*Box(w2+2,span,span)
top_strip=strip & Pos(0,joint_y+joint_gap/2+span/2,top/2)*Box(w2+2,span,span)
from math import tan, radians
axis_z=param('binding_inner_axis_z',149.0)
fold_relief=param('binding_opening_relief_deg',30.0)
slope=tan(radians(fold_relief))
front_strip-=extrude(Plane.YZ*Polygon((joint_y-joint_gap/2,axis_z),(joint_y+20,axis_z),(joint_y+20,axis_z+20),(joint_y-joint_gap/2-slope*20,axis_z+20),align=None),amount=w2+2,both=True)
hinge_clear_radius=param('inner_hinge_binding_clearance',3.3)
hinge_clear=Pos(0,joint_y,axis_z)*Rot(0,90,0)*Cylinder(hinge_clear_radius,w2+2)
front_strip-=hinge_clear
top_strip-=hinge_clear

rear_y=param('binding_rear_fold_joint_y',53.35)
rear_strip=top_strip & Pos(0,rear_y+joint_gap/2+span/2,top/2)*Box(w2+2,span,span)
top_strip=top_strip & Pos(0,rear_y-joint_gap/2-span/2,top/2)*Box(w2+2,span,span)
rear_strip-=extrude(Plane.YZ*Polygon((rear_y+joint_gap/2,axis_z),(rear_y-20,axis_z),(rear_y-20,axis_z+20),(rear_y+joint_gap/2+slope*20,axis_z+20),align=None),amount=w2+2,both=True)
rear_clear=Pos(0,rear_y,axis_z)*Rot(0,90,0)*Cylinder(hinge_clear_radius,w2+2)
rear_strip-=rear_clear
top_strip-=rear_clear
rear_strip=refine_spine(rear_strip)
assert len(rear_strip.solids())==1
publish('rear_fold_binding',rear_strip,'后折叠书面贴带')
front_strip=refine_spine(front_strip);top_strip=refine_spine(top_strip)
assert len(front_strip.solids())==1 and len(top_strip.solids())==1
publish('fold_binding',front_strip,'折叠书脊贴面带')
publish('upper_binding',top_strip,'顶面独立贴面带')
