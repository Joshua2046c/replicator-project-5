from screwjoint import make_screw_joint_v1
w=param('bottom_panel_width',220.0);d=param('bottom_panel_depth',114.0);t=param('bottom_panel_thickness',4.0);channel=param('bottom_panel_band_width',30.4);recess=param('bottom_panel_band_recess',1.1)
xs=param('bottom_panel_joint_half_span',80.0);ix=param('bottom_panel_joint_inner_x',40.0);fy=param('bottom_panel_front_joint_y',-46.0);ry=param('bottom_panel_rear_joint_y',54.0)
p=Box(w,d,t,align=(Align.CENTER,Align.CENTER,Align.MIN));p-=Pos(0,0,recess/2)*Box(channel,d+1,recess)
for side,y,depth in [('front',fy,12),('rear',ry,6)]:
 for j,x in enumerate([-xs,-ix,ix,xs]):
  receiver=Pos(x,y,t+6)*Box(14,depth,12)
  joint=make_screw_joint_v1(size='M3',at=Location((x,y,0),(180,0,0)),through=[(p,t)],into=receiver,engage_depth=8,head='countersunk',material='PETG',label='bottom-'+side)
  # Kit countersink omits its own head's small rim; subtract the exact kit hardware envelope as well.
  p=p-joint.through_cuts[0]-joint.hardware
  publish('bottom_screw_'+side+str(j),joint.hardware,'底板沉头M3螺钉')
  print(side,joint.screw_length_mm)
publish('bottom_panel',p,'螺接独立底板')