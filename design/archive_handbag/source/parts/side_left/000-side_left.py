from math import sqrt
t=param('side_left_thickness',4.0);d=param('side_left_depth',100.0);h=param('side_left_height',183.4)
g=param('side_left_groove_depth',0.45);gw=param('side_left_groove_width',1.0)
b1=param('side_left_book_boundary1',60.0);b2=param('side_left_book_boundary2',124.0)
pitch=param('side_left_page_pitch',6.0);margin=param('side_left_page_margin',0.0);page=param('side_left_page_recess',0.25);cover=param('side_left_cover_band',4.0)
by=param('side_left_bolt_y',0.0);bz=param('side_left_bolt_z',170.0);bd=param('side_left_bolt_diameter',4.5)
rr=param('side_left_relief_radius',108.9);ry=param('side_left_relief_axis_y',60.5);rz=param('side_left_relief_axis_z',124.0);start=param('side_left_relief_start_z',124.3)
upperbase=param('side_left_upper_book_base',124.6);uppertop=param('side_left_upper_book_top',186.0)
R=param('spine_common_radius',88.33333333333333);ey=param('side_left_spine_end_y',-51.0);c=param('side_left_outer_chamfer',0.4)
panel=Box(t,d,h,align=(Align.CENTER,Align.CENTER,Align.MIN))
# True single-piece lower side: front circular lobes are fused before continuous page cuts.
for lo,hi in [(-4,b1),(b1,b2)]:
 z=(lo+hi)/2;H=hi-lo;cy=ey+sqrt(R*R-H*H/4);bottom=max(0,lo)
 outer=Pos(0,cy,z)*Rot(0,90,0)*Cylinder(R,t)
 lobe=outer&Pos(0,ey,(bottom+hi)/2)*Box(t,2*(R-sqrt(R*R-H*H/4)+abs(ey+d/2)+1),hi-bottom)
 taper=Pos(c/2,cy,z)*Rot(0,90,0)*Cylinder(R,t-c)
 taper+=Pos(-t/2+c/2,cy,z)*Rot(0,90,0)*Cone(R-c,R,c)
 lobe&=taper
 panel+=lobe
corner=Pos(0,0,(start+h)/2)*Box(t+2,d+2,h-start)
safe=Pos(0,ry,rz)*Rot(0,90,0)*Cylinder(rr,t+4)
panel-=corner-safe
for lo,hi in [(-4,b1),(b1,b2),(upperbase,uppertop)]:
 center=(lo+hi)/2
 # Cut through front arc outline, no strip of blank material or straight internal seam.
 panel-=Pos(-t/2+page/2,-R/2,center)*Box(page,d+R-2*margin,hi-lo-2*cover)
 for i in range(-4,5):panel-=Pos(-t/2+(page+g)/2,-R/2,center+i*pitch)*Box(page+g,d+R-2*margin,gw)
for z in [b1,b2]:panel-=Pos(-t/2+g/2,-R/2,z)*Box(g,d+R-2*margin,0.6)
panel-=Pos(0,by,bz)*Rot(0,90,0)*Cylinder(bd/2,t+2)
assert len(panel.solids())==1
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
panel=refine_spine(panel)
publish('side_left',panel,'圆弧一体左书页板')