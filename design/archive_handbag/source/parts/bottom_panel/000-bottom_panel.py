from screwjoint import make_screw_joint_v1
w=param('bottom_panel_width',220.0);d=param('bottom_panel_depth',114.0);t=param('bottom_panel_thickness',4.0);channel=param('bottom_panel_band_width',30.0);recess=param('bottom_panel_band_recess',1.0)
xs=param('bottom_panel_joint_half_span',80.0);ix=param('bottom_panel_joint_inner_x',40.0);fy=param('bottom_panel_front_joint_y',-46.0);ry=param('bottom_panel_rear_joint_y',54.0)
front=param('bottom_panel_front_edge_y',-51.0)
tl=param('bottom_panel_slot_length',70.6);tx=param('bottom_panel_slot_x',60.0);depth=param('bottom_panel_slot_depth',2.4);fw=param('bottom_panel_front_slot_width',2.4);rw=param('bottom_panel_rear_slot_width',3.0);sy=param('bottom_panel_front_slot_y',-49.5)
p=Pos(0,(front+d/2)/2,0)*Box(w,d/2-front,t,align=(Align.CENTER,Align.CENTER,Align.MIN));p-=Pos(0,0,recess/2)*Box(channel,d+1,recess)
# Exact 1mm贴面带 bottom corner returns, not free-hanging loops.
p-=Pos(0,front+recess/2,t/2)*Box(channel,recess,t)
p-=Pos(0,d/2-recess/2,t/2)*Box(channel,recess,t)
for s in [-1,1]:
 for y,ww in [(sy,fw),(ry,rw)]:p-=Pos(s*tx,y,t-depth/2)*Box(tl,ww,depth+0.02)
for side,y,dep in [('front',fy,12),('rear',ry,6)]:
 for j,x in enumerate([-xs,-ix,ix,xs]):
  receiver=Pos(x,y,t+6)*Box(14,dep,12)
  joint=make_screw_joint_v1(size='M3',at=Location((x,y,0),(180,0,0)),through=[(p,t)],into=receiver,engage_depth=8,head='countersunk',material='PETG',label='bottom-'+side)
  p=p-joint.through_cuts[0]-joint.hardware
  publish('bottom_screw_'+side+str(j),joint.hardware,'底部防拔脱螺钉')
publish('bottom_panel',p,'前后插槽底板')