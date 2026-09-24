from math import sqrt
w=param('lid_width',220.0);d=param('lid_depth',114.0);height=param('lid_height',61.4);roof=param('lid_roof_thickness',2.2);wall=param('lid_wall',6.0)
hy=param('lid_hinge_y',60.5);hz=param('lid_hinge_z',128.0);seam=param('lid_seam_z',128.6)
r=param('lid_barrel_radius',3.8);bore=param('lid_bore',4.4);barrel_l=param('lid_barrel_length',58.8)
rw=param('lid_rear_width',220.0);R=param('spine_common_radius',88.33333333333333);ft=param('lid_spine_thickness',3.5);ey=param('lid_spine_end_y',-51.0)
mx=param('lid_magnet_x',72.0);my=param('lid_magnet_y',-47.0)
relief=param('lid_rear_bottom_relief',0.6);cheek=param('lid_end_cheek_thickness',2.0);sweep=param('lid_cheek_inner_radius',108.0)
g=param('lid_page_groove_depth',0.45);gw=param('lid_page_groove_width',1.0);wrap=param('lid_corner_groove_depth',0.45)
page=param('lid_page_recess',0.25);cover=param('lid_cover_band',4.0);pitch=param('lid_groove_pitch',6.0)
px=param('lid_panel_center_x',108.0);slot=param('lid_panel_clearance_width',4.6)
bw=param('lid_band_width',30.0);bt=param('lid_band_recess',1.0);bs=param('lid_band_rear_start',134.0)
c=param('lid_outer_chamfer',0.4)
frame=Pos(0,hy-55.0,hz-128.0)
b=seam-hz;top=b+height;sag=R-sqrt(R*R-height*height/4)
lid=Pos(0,(ey+d/2)/2-hy,top-roof)*Box(w,d/2-ey,roof,align=(Align.CENTER,Align.CENTER,Align.MIN))
rear=Pos(0,d/2-hy-wall/2,b)*Box(rw,wall,height,align=(Align.CENTER,Align.CENTER,Align.MIN))
cut=extrude(Plane.YZ*Polygon((d/2-hy-relief,b-0.1),(d/2-hy+1,b-0.1),(d/2-hy+1,b+relief+1),align=None),amount=rw+2,both=True)
rear-=cut;lid+=rear
cy=ey+R-sag-hy;cz=b+height/2
outer=Pos(0,cy,cz)*Rot(0,90,0)*Cylinder(R,w)
curve=(outer-Pos(0,cy+ft,cz)*Rot(0,90,0)*Cylinder(R,w+1))&Pos(0,ey-hy-sag/2+ft,cz)*Box(w,2*(sag+ft+1),height)
safe=Rot(0,90,0)*Cylinder(sweep,w+2)
for s in [-1,1]:
 cx=s*(w/2-cheek/2)
 cap=(Pos(cx,cy,cz)*Rot(0,90,0)*Cylinder(R,cheek))&Pos(cx,(ey-sag)/2-hy,cz)*Box(cheek,sag-ey,height)
 cap-=safe;curve+=cap
 curve-=safe&Pos(s*px,-hy,cz)*Box(slot,120,height+0.2)
lid+=curve
for s in [-1,1]:
 lid-=Pos(s*px,49-hy,b+(height-roof)/2)*Box(slot,2.6,height-roof)
 lid-=Pos(s*39.5,0,0)*Rot(0,90,0)*Cylinder(r+0.6,19.8)
 lid-=Pos(s*50.7,0,0)*Rot(0,90,0)*Cylinder(3.5,2.2)
lid+=Pos(0,(d/2-wall/2-hy)/2,r-0.8)*Box(barrel_l,hy-(d/2-wall/2),1.6)
lid+=Rot(0,90,0)*Cylinder(r,barrel_l)
lid-=Rot(0,90,0)*Cylinder(bore/2,100.4)
lid-=Pos(0,d/2-page/2-hy,cz)*Box(rw+2,page,height-2*cover)
# Side page fields use the lower side-panel's straight front datum.
lap=param('spine_lap_rear_y',-47.5)
sidegap=param('lid_side_page_front_clearance',0.3)
pagefront=lap+sidegap
for s in [-1,1]:
 lid-=Pos(s*(w/2-page/2),(pagefront+d/2)/2-hy,cz)*Box(page,d/2-pagefront,height-2*cover)
 for i in range(-4,5):
  lid-=Pos(s*(w/2-(page+wrap)/2),(pagefront+d/2)/2-hy,cz+i*pitch)*Box(page+wrap,d/2-pagefront,gw)
# Rear grooves join the side field around the back corners.
for i in range(-4,5):
 zz=cz+i*pitch
 lid-=Pos(0,d/2-(page+g)/2-hy,zz)*Box(rw+2,page+g,gw)

for s,side in [(-1,'left'),(1,'right')]:
 oid='lid_magnet_mount_'+side;od=param(oid+'_diameter',11.3);mh=param(oid+'_height',5.4);pd=param(oid+'_pocket_diameter',7.3);dep=param(oid+'_pocket_depth',3.2)
 lid+=(Pos(s*mx,my-hy,b+mh/2)*Cylinder(od/2,mh))&outer
 lid-=Pos(s*mx,my-hy,b-0.1)*Cylinder(pd/2,dep+0.1,align=(Align.CENTER,Align.CENTER,Align.MIN))
band=(outer-Pos(0,cy+bt,cz)*Rot(0,90,0)*Cylinder(R,w+2))&Pos(0,ey-hy,cz)*Box(bw,20,height)
band+=Pos(0,(ey+d/2)/2-hy,top-bt/2)*Box(bw,d/2-ey,bt)
band+=Pos(0,d/2-hy-bt/2,(top+bs-hz)/2)*Box(bw,bt,top-(bs-hz))
lid-=band
taper=Pos(0,cy,cz)*Rot(0,90,0)*Cylinder(R,w-2*c)
taper+=Pos(-w/2+c/2,cy,cz)*Rot(0,90,0)*Cone(R-c,R,c)
taper+=Pos(w/2-c/2,cy,cz)*Rot(0,90,0)*Cone(R,R-c,c)
lid-=(outer-taper)&Pos(0,ey-hy,cz)*Box(w+2,20,height)
for xx,sg in [(-w/2,-1),(w/2,1)]:
 lid-=extrude(Plane.XZ*Polygon((xx-sg*c,top),(xx+sg*2,top),(xx+sg*2,top-c-2),align=None),amount=d+20,both=True)
for yy,sg in [(ey-hy,-1),(d/2-hy,1)]:
 lid-=extrude(Plane.YZ*Polygon((yy-sg*c,top),(yy+sg*2,top),(yy+sg*2,top-c-2),align=None),amount=w+2,both=True)
# Blind roof nameplate pocket, keeping1.2mm roof floor at default settings.
nw=param('nameplate_width',20.0);nl=param('nameplate_length',36.0);nx=param('nameplate_x',-75.0);ny=param('nameplate_y',4.0);nd=param('nameplate_pocket_depth',1.0);nc=param('nameplate_clearance',0.15)
lid-=Pos(nx,ny-hy,top-nd)*Box(nw+2*nc,nl+2*nc,nd+1,align=(Align.CENTER,Align.CENTER,Align.MIN))
# Matching pair of curved pink-spine inlay pockets.
mw=param('pink_marks_bar_width',3.0);mh=param('pink_marks_bar_height',25.0);xx0=param('pink_marks_left_x',-84.0);mp=param('pink_marks_pitch',13.0);mz=param('pink_marks_center_z',159.3)-hz
md=param('pink_marks_pocket_depth',1.2);mc=param('pink_marks_pocket_clearance',0.15);ms=param('pink_marks_spine_height',61.4);mey=param('pink_marks_end_y',-51.0);mcy=mey+sqrt(R*R-ms*ms/4)-hy
for xx in [xx0,xx0+mp]:
 cut=Pos(xx,mcy,mz)*Rot(0,90,0)*Cylinder(R+2,mw+2*mc)-Pos(xx,mcy,mz)*Rot(0,90,0)*Cylinder(R-md,mw+2*mc+2)
 lid-=cut&Pos(xx,mey-hy,mz)*Box(mw+2*mc,30,mh+2*mc)
assert len(lid.solids())==1
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
lid=refine_spine(lid)
# Preserve the smooth large-cylinder partitions while adding small corner rounds.
from build123d import SkipClean
with SkipClean():
 # Two rear corners: tangent round in plan, including the recessed page field.
 cr=param('lid_rear_corner_radius',1.0)
 assert cr>page+max(g,wrap) and cr>c
 for s in [-1,1]:
  xc=s*(w/2-cr);yc=d/2-hy-cr
  def corner_cut(radius,z0,span):
   square=Pos(s*(w/2-cr/2),d/2-hy-cr/2,z0)*Box(cr,cr,span,align=(Align.CENTER,Align.CENTER,Align.MIN))
   disk=Pos(xc,yc,z0)*Cylinder(radius,span,align=(Align.CENTER,Align.CENTER,Align.MIN))
   return square-disk
  lid-=corner_cut(cr,b-1,height+2)
  lid-=corner_cut(cr-page,b+cover,height-2*cover)
  for i in range(-4,5):
   lid-=corner_cut(cr-page-max(g,wrap),cz+i*pitch-gw/2,gw)
  # Continue the existing top-edge chamfer around the new circular corner.
  square=Pos(s*(w/2-cr/2),d/2-hy-cr/2,top-c)*Box(cr,cr,c,align=(Align.CENTER,Align.CENTER,Align.MIN))
  cone=Pos(xc,yc,top-c)*Cone(cr,cr-c,c,align=(Align.CENTER,Align.CENTER,Align.MIN))
  lid-=square-cone
assert lid.is_valid and len(lid.solids())==1
publish('lid',frame*lid,'光面端部贴合翻盖')