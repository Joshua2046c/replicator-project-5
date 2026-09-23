from screwjoint import make_screw_joint_v1
parts={};curves={}
xs=param('spine_joint_half_span',80.0);pitch=param('spine_joint_inner_x',40.0);jy=param('spine_joint_y',-46.0);jw=param('spine_joint_tab_width',14.0);jd=param('spine_joint_tab_depth',12.0)
guide=param('spine_end_guide_thickness',7.0)
for oid,z,h in [('green_spine',34,60),('blue_spine',96,64)]:
 w=param(oid+'_width',220.0);hh=param(oid+'_height',h);t=param(oid+'_thickness',3.5);zz=param(oid+'_center_z',z)
 sag=param(oid+'_arc_sag',6.0);end_y=param(oid+'_end_y',-51.0);panelx=param(oid+'_guide_x',108.0);slot=param(oid+'_guide_width',4.6)
 radius=(hh*hh/4+sag*sag)/(2*sag);cy=end_y+radius-sag
 outer=Pos(0,cy,zz)*Rot(0,90,0)*Cylinder(radius,w);inner=Pos(0,cy+t,zz)*Rot(0,90,0)*Cylinder(radius,w+2)
 plate=(outer-inner)&Pos(0,end_y-sag/2+t,zz)*Box(w,2*(sag+t+1),hh)
 curves[oid]=outer
 for s in [-1,1]:
  cx=s*(w/2-guide/2)
  end=(Pos(cx,cy,zz)*Rot(0,90,0)*Cylinder(radius,guide))&Pos(cx,-50,zz)*Box(guide,16,hh)
  plate+=end;plate-=Pos(s*panelx,0,zz)*Box(slot,100.6,hh+0.2)
 for x in [-xs,-pitch,pitch,xs]:
  if oid=='green_spine':tabs=Pos(x,jy,9)*Box(jw,jd,10)+Pos(x,jy,59)*Box(jw,jd,10)
  else:tabs=Pos(x,jy,66)*Box(jw,jd,4)
  plate+=tabs&outer
 parts[oid]=plate
# Fixed, integral narrow pink end cheeks preserve the full-width appearance without entering the page-panel sweep.
ew=param('blue_spine_upper_edge_width',4.3);top=param('blue_spine_upper_edge_top',186.5);bottom=param('blue_spine_upper_edge_base',127.8)
eh=param('blue_spine_upper_arc_height',60.4);es=param('blue_spine_upper_arc_sag',6.0);ez=param('blue_spine_upper_arc_center_z',158.8);ey=param('blue_spine_upper_arc_end_y',-51.0);back=param('blue_spine_upper_edge_rear_y',-50.3)
R=(eh*eh/4+es*es)/(2*es);cy=ey+R-es
for s in [-1,1]:
 cx=s*(110-ew/2)
 edge=Pos(cx,cy,ez)*Rot(0,90,0)*Cylinder(R,ew)
 edge &= Pos(cx,(ey-es+back)/2,(bottom+top)/2)*Box(ew,back-ey+es,top-bottom)
 parts['blue_spine']+=edge
for j,x in enumerate([-xs,-pitch,pitch,xs]):
 joint=make_screw_joint_v1(size='M3',at=Location((x,jy,68)),through=[(parts['blue_spine'],4)],into=parts['green_spine'],engage_depth=8,material='PETG',label='front-panel-join')
 parts['blue_spine']-=joint.through_cuts[0];parts['green_spine']=parts['green_spine']+joint.bosses-joint.engage_cuts
 publish('spine_join_screw_'+str(j),joint.hardware,'前板拼接M3螺钉')
 proxy=Pos(x,jy,2)*Box(jw,jd,4)
 bottomjoint=make_screw_joint_v1(size='M3',at=Location((x,jy,0),(180,0,0)),through=[(proxy,4)],into=parts['green_spine'],engage_depth=8,head='countersunk',material='PETG',label='front-bottom')
 parts['green_spine']=parts['green_spine']+bottomjoint.bosses-bottomjoint.engage_cuts
mx=param('body_magnet_x',72.0);my=param('body_magnet_y',-39.0);H=128.0 # mating seam
for s,side in [(-1,'left'),(1,'right')]:
 mid='magnet_mount_'+side;mw=param(mid+'_width',28.0);md=param(mid+'_depth',12.0);mh=param(mid+'_height',12.0)
 mount=Pos(s*mx,my-3,H-mh/2)*Box(mw,md+12,mh)&curves['blue_spine']
 cid='body_mag_cap_'+side
 cw=param(cid+'_width',22.0);cd=param(cid+'_depth',14.0);ct=param(cid+'_edge_thickness',2.6);mem=param(cid+'_membrane',0.6);cp=param(cid+'_screw_half_pitch',8.0)
 mount-=Pos(s*mx,my,H-3.8)*Cylinder(7.3/2,4,align=(Align.CENTER,Align.CENTER,Align.MIN));mount-=Pos(s*mx,my,H-ct)*Box(cw+0.4,cd+0.4,ct+0.1,align=(Align.CENTER,Align.CENTER,Align.MIN))
 cap=Pos(s*mx,my,H-ct/2)*Box(cw,cd,ct);cap-=Pos(s*mx,my,H-ct)*Cylinder(4.1,ct-mem,align=(Align.CENTER,Align.CENTER,Align.MIN))
 for j,dx in enumerate([-cp,cp]):
  cap-=Pos(s*mx+dx,my,H-2)*Cylinder(2.1,2.1,align=(Align.CENTER,Align.CENTER,Align.MIN))
  joint=make_screw_joint_v1(size='M2',at=Location((s*mx+dx,my,H-2)),through=[(cap,ct-2)],into=mount,engage_depth=5.4,material='PETG',label=cid+str(j))
  cap-=joint.through_cuts[0];mount=mount+joint.bosses-joint.engage_cuts;publish(cid+'_screw_'+str(j),joint.hardware,'磁铁盖螺钉')
 publish(cid,cap,'磁铁防脱盖');parts['blue_spine']+=mount
for oid,p in parts.items():
 assert len(p.solids())==1
 publish(oid,p,'一致弧形书脊')