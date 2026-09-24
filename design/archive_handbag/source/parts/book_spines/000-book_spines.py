from screwjoint import make_screw_joint_v1
from math import sqrt
R=param('spine_common_radius',88.33333333333333)
xs=param('spine_joint_half_span',80.0);pitch=param('spine_joint_inner_x',40.0);jy=param('spine_joint_y',-46.0);jw=param('spine_joint_tab_width',14.0);jd=param('spine_joint_tab_depth',12.0)
guide=param('spine_end_guide_thickness',7.0);base=param('front_panel_base_z',4.0)
bw=param('front_panel_band_width',30.0);bt=param('front_panel_band_depth',1.0)
tl=param('front_panel_tongue_length',70.0);tt=param('front_panel_tongue_thickness',1.8);th=param('front_panel_tongue_depth',2.2);tx=param('front_panel_tongue_x',60.0);ty=param('front_panel_tongue_y',-49.5)
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
  endpart=(Pos(cx,cy,zz)*Rot(0,90,0)*Cylinder(R,guide))&Pos(cx,-50,(bottom+top)/2)*Box(guide,16,top-bottom)
  plate+=endpart;plate-=Pos(s*panelx,0,zz)*Box(slot,100.6,hh+0.2)
 if oid=='green_spine':
  for x in [-xs,-pitch,pitch,xs]:plate+=Pos(x,jy,9)*Box(jw,jd,10)&outer
  for s in [-1,1]:plate+=Pos(s*tx,ty,base-th/2)*Box(tl,tt,th+0.02)
 band=(outer-Pos(0,cy+bt,zz)*Rot(0,90,0)*Cylinder(R,w+2))&Pos(0,end_y-sag/2+t,(bottom+top)/2)*Box(bw,2*(sag+t+1),top-bottom)
 plate-=band;parts[oid]=plate
front=parts['green_spine']+parts['blue_spine']
for x in [-xs,-pitch,pitch,xs]:
 proxy=Pos(x,jy,2)*Box(jw,jd,4)
 j=make_screw_joint_v1(size='M3',at=Location((x,jy,0),(180,0,0)),through=[(proxy,4)],into=front,engage_depth=8,head='countersunk',material='PETG',label='front-bottom')
 front=front+j.bosses-j.engage_cuts-j.through_cuts[0]
mx=param('body_magnet_x',72.0);my=param('body_magnet_y',-45.8);mtop=param('body_magnet_seat_top',128.0)
for s,side in [(-1,'left'),(1,'right')]:
 oid='magnet_mount_'+side;od=param(oid+'_diameter',11.3);mh=param(oid+'_height',5.4);pd=param(oid+'_pocket_diameter',7.3);dep=param(oid+'_pocket_depth',3.2)
 mount=Pos(s*mx,my,mtop-mh/2)*Cylinder(od/2,mh)&curves['blue_spine']
 front+=mount
 front-=Pos(s*mx,my,mtop-dep)*Cylinder(pd/2,dep+0.1,align=(Align.CENTER,Align.CENTER,Align.MIN))
# Free through-bolt connection after ScrewJointNotApplicableV1: the thin guide cannot receive a blind printed screw joint. Metal M3 nut, no plastic thread or added boss.
ly=param('side_lock_y',-46.5);lz=param('side_lock_z',100.0);sx=param('side_lock_surface_x',109.75);hole=param('side_lock_clearance_diameter',3.4)
for s in [-1,1]:front-=Pos(s*(sx-6),ly,lz)*Rot(0,90,0)*Cylinder(hole/2,14)
assert len(front.solids())==1
publish('blue_spine',front,'圆弧前板与侧板锁孔')