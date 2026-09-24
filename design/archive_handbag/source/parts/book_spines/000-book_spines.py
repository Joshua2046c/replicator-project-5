from math import sqrt
R=param('spine_common_radius',88.33333333333333)
xs=param('spine_joint_half_span',80.0);pitch=param('spine_joint_inner_x',40.0)
guide=param('spine_end_guide_thickness',7.0);base=param('front_panel_base_z',4.0)
bw=param('front_panel_band_width',30.0);bt=param('front_panel_band_depth',1.0)
gdepth=param('front_panel_curved_end_depth',9.0)
py=param('front_panel_peg_y',-47.0);pw=param('front_panel_peg_socket_width',4.4);pd=param('front_panel_peg_socket_depth',6.3);pad=param('front_panel_peg_pad_width',10.0);ph=param('front_panel_peg_pad_height',8.0)
c=param('blue_spine_outer_chamfer',0.4)
lap=param('spine_lap_rear_y',-47.5)
parts={};curves={}
for oid,z,h in [('green_spine',32,64),('blue_spine',96,64)]:
 w=param(oid+'_width',220.0);hh=param(oid+'_height',h);t=param(oid+'_thickness',3.5);zz=param(oid+'_center_z',z)
 end_y=param(oid+'_end_y',-51.0);panelx=param(oid+'_guide_x',108.0);slot=param(oid+'_guide_width',4.6)
 sag=R-sqrt(R*R-hh*hh/4);cy=end_y+R-sag
 outer=Pos(0,cy,zz)*Rot(0,90,0)*Cylinder(R,w);inner=Pos(0,cy+t,zz)*Rot(0,90,0)*Cylinder(R,w+2)
 bottom=max(base,zz-hh/2);top=zz+hh/2
 window=Pos(0,end_y-sag/2+t,(bottom+top)/2)*Box(w,2*(sag+t+1),top-bottom)
 plate=(outer-inner)&window;curves[oid]=outer
 for s in [-1,1]:
  cx=s*(w/2-guide/2)
  endpart=((Pos(cx,cy,zz)*Rot(0,90,0)*Cylinder(R,guide))-(Pos(cx,cy+gdepth,zz)*Rot(0,90,0)*Cylinder(R,guide+2)))&Pos(cx,-50,(bottom+top)/2)*Box(guide,16,top-bottom)
  # Full-width spine owns the outside curved corner. The side slides behind its planar lap.
  capwindow=Pos(cx,(end_y-sag+lap)/2,(bottom+top)/2)*Box(guide,lap-end_y+sag,top-bottom)
  plate+=endpart+(outer&capwindow)
  plate-=Pos(s*panelx,lap+R+abs(end_y),zz)*Box(slot,2*(R+abs(end_y)),hh+0.2)
 if oid=='green_spine':
  for x in [-xs,-pitch,pitch,xs]:plate+=Pos(x,py,base+ph/2)*Box(pad,pad,ph)&outer
 taper=Pos(0,cy,zz)*Rot(0,90,0)*Cylinder(R,w-2*c)
 taper+=Pos(-w/2+c/2,cy,zz)*Rot(0,90,0)*Cone(R-c,R,c)
 taper+=Pos(w/2-c/2,cy,zz)*Rot(0,90,0)*Cone(R,R-c,c)
 plate-=outer-taper
 band=(outer-Pos(0,cy+bt,zz)*Rot(0,90,0)*Cylinder(R,w+2))&Pos(0,end_y-sag/2+t,(bottom+top)/2)*Box(bw,2*(sag+t+1),top-bottom)
 plate-=band
 name=oid.replace('_spine','_marks')
 mw=param(name+'_bar_width',3.0);mh=param(name+'_bar_height',25.0);xx0=param(name+'_left_x',-84.0);mp=param(name+'_pitch',13.0);mz=param(name+'_center_z',z)
 md=param(name+'_pocket_depth',1.2);mc=param(name+'_pocket_clearance',0.15)
 mspan=param(name+'_spine_height',h);mey=param(name+'_end_y',-51.0);mcy=mey+sqrt(R*R-mspan*mspan/4)
 for xx in [xx0,xx0+mp]:
  cut=Pos(xx,mcy,mz)*Rot(0,90,0)*Cylinder(R+2,mw+2*mc)-Pos(xx,mcy,mz)*Rot(0,90,0)*Cylinder(R-md,mw+2*mc+2)
  plate-=cut&Pos(xx,mey,mz)*Box(mw+2*mc,30,mh+2*mc)
 parts[oid]=plate
front=parts['green_spine']+parts['blue_spine']
for x in [-xs,-pitch,pitch,xs]:front-=Pos(x,py,base+pd/2-.01)*Box(pw,pw,pd+.02)
mx=param('body_magnet_x',72.0);my=param('body_magnet_y',-45.8);mtop=param('body_magnet_seat_top',128.0)
for s,side in [(-1,'left'),(1,'right')]:
 oid='magnet_mount_'+side;od=param(oid+'_diameter',11.3);mh=param(oid+'_height',5.4);md=param(oid+'_pocket_diameter',7.3);dep=param(oid+'_pocket_depth',3.2)
 front+=(Pos(s*mx,my,mtop-mh/2)*Cylinder(od/2,mh))&curves['blue_spine']
 front-=Pos(s*mx,my,mtop-dep)*Cylinder(md/2,dep+0.1,align=(Align.CENTER,Align.CENTER,Align.MIN))
assert len(front.solids())==1
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
front=refine_spine(front)
publish('blue_spine',front,'外包侧板一体书脊')