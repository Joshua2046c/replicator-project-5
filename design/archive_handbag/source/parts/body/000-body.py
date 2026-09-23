# Rebuild body target from source to repair stale raw-object cache paths.
from screwjoint import make_screw_joint_v1, ScrewJointNotApplicableV1
W=param('case_width',220.0); D=param('body_depth',114.0); H=param('body_height',128.0)
wall=param('body_wall',6.0); floor=param('body_floor',4.0); sidewall=param('body_sidewall',8.0)
slot_t=param('body_slot_thickness',3.6); slot_d=param('body_slot_depth',87.6); opening=param('body_side_opening',77.0); panel_x=param('body_panel_center_x',107.5)
hy=param('body_hinge_y',54.0); hz=param('body_hinge_z',132.0); hr=param('body_hinge_radius',5.0); bore=param('body_hinge_bore',4.4)
mount_y=param('body_ring_mount_y',46.5); mount_z=param('body_ring_mount_z',100.0); mount_pitch=param('body_ring_mount_pitch',20.0); mount_hole=param('body_ring_hole',4.5)
mx=param('body_magnet_x',72.0); my=param('body_magnet_y',-47.0)
body=Box(W,D,H,align=(Align.CENTER,Align.CENTER,Align.MIN))-Pos(0,0,floor)*Box(W-2*sidewall,D-2*wall,H,align=(Align.CENTER,Align.CENTER,Align.MIN))
for s in [-1,1]:
 body-=Pos(s*W/2,0,floor)*Box(24,opening,H,align=(Align.CENTER,Align.CENTER,Align.MIN))
 body-=Pos(s*panel_x,0,floor)*Box(slot_t,slot_d,H,align=(Align.CENTER,Align.CENTER,Align.MIN))
 body+=Pos(s*(W/2-5),47.5,H/2)*Box(10,7,H)
 for z in [mount_z-mount_pitch/2,mount_z+mount_pitch/2]:
  try: make_screw_joint_v1(size='M4',at=Location((s*W/2,mount_y,z)),through=[],into=body,engage_depth=3.2,strategy='captive_nut',material='PETG',label='ring-through-bolt')
  except ScrewJointNotApplicableV1: pass
  body-=Pos(s*(W/2-5),mount_y,z)*Rot(0,90,0)*Cylinder(mount_hole/2,14)
for x in [-39.5,39.5]:
 body+=Pos(x,hy,H-1)*Box(19,6,hz-H+2,align=(Align.CENTER,Align.CENTER,Align.MIN))
 body+=Pos(x,hy,hz)*Rot(0,90,0)*Cylinder(hr,19)
 body-=Pos(x,hy,hz)*Rot(0,90,0)*Cylinder(bore/2,20)
for s,side in [(-1,'left'),(1,'right')]:
 cid='body_mag_cap_'+side
 cw=param(cid+'_width',22.0); cd=param(cid+'_depth',14.0); ct=param(cid+'_edge_thickness',2.6); membrane=param(cid+'_membrane',0.6); cp=param(cid+'_screw_half_pitch',8.0)
 body+=Pos(s*mx,my,H-12)*Box(28,18,12,align=(Align.CENTER,Align.CENTER,Align.MIN))
 body-=Pos(s*mx,my,H-3.8)*Cylinder(7.3/2,3.9,align=(Align.CENTER,Align.CENTER,Align.MIN))
 body-=Pos(s*mx,my,H-ct)*Box(cw+0.4,cd+0.4,ct+0.1,align=(Align.CENTER,Align.CENTER,Align.MIN))
 cap=Pos(s*mx,my,H-ct/2)*Box(cw,cd,ct)
 cap-=Pos(s*mx,my,H-ct)*Cylinder(4.1,ct-membrane,align=(Align.CENTER,Align.CENTER,Align.MIN))
 for j,dx in enumerate([-cp,cp]):
  cap-=Pos(s*mx+dx,my,H-2)*Cylinder(2.1,2.1,align=(Align.CENTER,Align.CENTER,Align.MIN))
  joint=make_screw_joint_v1(size='M2',at=Location((s*mx+dx,my,H-2)),through=[(cap,ct-2)],into=body,engage_depth=5.4,material='PETG',head='socket_cap',label=cid+str(j))
  cap-=joint.through_cuts[0]; body=body+joint.bosses-joint.engage_cuts
  publish(cid+'_screw_'+str(j),joint.hardware,'磁铁盖 M2 螺钉')
  print(cid,'M2 screw length',joint.screw_length_mm)
 publish(cid,cap,'内置磁铁防脱盖')
for s,side in [(-1,'left'),(1,'right')]:
 cid='axle_stop_'+side
 w=param(cid+'_width',12.0); d=param(cid+'_depth',10.0); t=param(cid+'_base_thickness',3.0); sh=param(cid+'_stop_height',9.0); st=param(cid+'_stop_thickness',2.0); x=param(cid+'_inner_x',50.4)
 cap=Pos(s*(x+w/2),hy,H+t/2)*Box(w,d,t)
 cap+=Pos(s*(x+st/2),hy,H+sh/2)*Box(st,d,sh)
 joint=make_screw_joint_v1(size='M3',at=Location((s*(x+w-3.5),hy,H+t)),through=[(cap,t)],into=body,engage_depth=7,material='PETG',label=cid)
 cap-=joint.through_cuts[0]; body=body+joint.bosses-joint.engage_cuts
 publish(cid,cap,'转轴端部止挡');publish(cid+'_screw',joint.hardware,'止挡 M3 螺钉')
 print(cid,'M3 screw length',joint.screw_length_mm)
body.color=Color(0.09,0.10,0.11)
assert len(body.solids())==1
publish('body',body,'贯通承重包体')