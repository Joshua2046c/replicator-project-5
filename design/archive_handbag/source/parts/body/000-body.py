from screwjoint import make_screw_joint_v1
W=param('case_width',220.0);H=param('body_height',128.0);floor=param('body_floor',4.0)
wall=param('body_wall',6.0);hy=param('body_hinge_y',60.5);hz=param('body_hinge_z',128.0);hr=param('body_hinge_radius',3.8);bore=param('body_hinge_bore',4.4)
px=param('body_panel_center_x',108.0);slot=param('body_slot_thickness',4.6)
rear_y=param('body_rear_center_y',54.0);groove=param('body_page_depth',0.45);groovew=param('body_page_width',1.0)
page=param('body_page_recess',0.25);cover=param('body_cover_band',4.0);pitch=param('body_page_pitch',6.0);boundary=param('body_book_boundary',64.0)
wrap=param('body_corner_groove_depth',0.45);lip=param('body_guide_lip_width',7.0)
tl=param('body_tongue_length',70.0);tt=param('body_tongue_thickness',2.4);td=param('body_tongue_depth',2.2);tx=param('body_tongue_x',60.0)
bw=param('body_band_width',30.0);bt=param('body_band_depth',1.0);bend=param('body_band_top',123.5)
hc=param('body_axle_head_clearance',0.4)
body=Pos(0,rear_y,(H+floor)/2)*Box(W,wall,H-floor)
for s in [-1,1]:
 body+=Pos(s*tx,rear_y,floor-td/2)*Box(tl,tt,td+0.02)
 body+=Pos(s*(W/2-lip/2),49,(H+floor)/2)*Box(lip,8,H-floor)
 body-=Pos(s*px,0,floor)*Box(slot,100.6,H,align=(Align.CENTER,Align.CENTER,Align.MIN))
for lo,hi in [(0,boundary),(boundary,H)]:
 center=(lo+hi)/2
 body-=Pos(0,rear_y+wall/2-page/2,center)*Box(W+2,page,hi-lo-2*cover)
 for s in [-1,1]:body-=Pos(s*(W/2-page/2),51,center)*Box(page,14,hi-lo-2*cover)
 for i in range(-4,5):
  zz=center+i*pitch
  body-=Pos(0,rear_y+wall/2-(page+groove)/2,zz)*Box(W+2,page+groove,groovew)
  for s in [-1,1]:body-=Pos(s*(W/2-(page+wrap)/2),51,zz)*Box(page+wrap,14,groovew)
body-=Pos(0,rear_y+wall/2-groove/2,boundary)*Box(W+2,groove,0.6)
for s in [-1,1]:body-=Pos(s*(W/2-wrap/2),51,boundary)*Box(wrap,14,0.6)
body-=Pos(0,rear_y+wall/2-bt/2,(bend+floor)/2)*Box(bw,bt,bend-floor)
for x in [-39.5,39.5]:
 body+=Pos(x,(rear_y+hy)/2,H-hr/2)*Box(19,hy-rear_y,hr)
 body+=Pos(x,hy,hz)*Rot(0,90,0)*Cylinder(hr,19)
body-=Pos(0,hy,hz)*Rot(0,90,0)*Cylinder(hr+0.6,59.8)
body-=Pos(0,hy,hz)*Rot(0,90,0)*Cylinder(bore/2,100.4)
for s in [-1,1]:body-=Pos(s*50.7,hy,hz)*Rot(0,90,0)*Cylinder(3+hc,1.4+2*hc)
for x in [-80,-40,40,80]:
 proxy=Pos(x,rear_y,2)*Box(16,6,4)
 joint=make_screw_joint_v1(size='M3',at=Location((x,rear_y,0),(180,0,0)),through=[(proxy,4)],into=body,engage_depth=8,head='countersunk',material='PETG',label='rear-bottom')
 body=body+joint.bosses-joint.engage_cuts-joint.through_cuts[0]
assert len(body.solids())==1
publish('body',body,'无内伸支臂后板')