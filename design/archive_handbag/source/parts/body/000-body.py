W=param('case_width',220.0);H=param('body_height',128.0);floor=param('body_floor',4.0)
wall=param('body_wall',6.0);hy=param('body_hinge_y',60.5);hz=param('body_hinge_z',128.0);hr=param('body_hinge_radius',3.8);bore=param('body_hinge_bore',4.4)
px=param('body_panel_center_x',108.0);slot=param('body_slot_thickness',4.6)
rear_y=param('body_rear_center_y',54.0);groove=param('body_page_depth',0.45);groovew=param('body_page_width',1.0)
page=param('body_page_recess',0.25);cover=param('body_cover_band',4.0);pitch=param('body_page_pitch',6.0);boundary=param('body_book_boundary',64.0)
wrap=param('body_corner_groove_depth',0.45);lip=param('body_guide_lip_width',7.0)
bw=param('body_band_width',30.0);bt=param('body_band_depth',1.0);bend=param('body_band_top',123.5)
hc=param('body_axle_head_clearance',0.4)
py=param('body_peg_y',52.0);pw=param('body_peg_socket_width',4.4);pd=param('body_peg_socket_depth',6.3);pad=param('body_peg_pad_width',10.0);ph=param('body_peg_pad_height',8.0);xs=param('body_peg_outer_x',80.0);ix=param('body_peg_inner_x',40.0)
c=param('body_outer_chamfer',0.4)
body=Pos(0,rear_y,(H+floor)/2)*Box(W,wall,H-floor)
for s in [-1,1]:
 body+=Pos(s*(W/2-lip/2),49,(H+floor)/2)*Box(lip,8,H-floor)
 body-=Pos(s*px,0,floor)*Box(slot,100.6,H,align=(Align.CENTER,Align.CENTER,Align.MIN))
for x in [-xs,-ix,ix,xs]:
 body+=Pos(x,py,floor+ph/2)*Box(pad,pad,ph)
 body-=Pos(x,py,floor+pd/2-.01)*Box(pw,pw,pd+.02)
for s in [-1,1]:
 body-=extrude(Plane.XY*Polygon((s*(W/2-c),rear_y+wall/2),(s*(W/2+2),rear_y+wall/2),(s*(W/2+2),rear_y+wall/2-c-2),align=None),amount=H+1,both=True)
for lo,hi in [(0,boundary),(boundary,H)]:
 center=(lo+hi)/2
 body-=Pos(0,rear_y+wall/2-page/2,center)*Box(W+2,page,hi-lo-2*cover)
 for s in [-1,1]:body-=Pos(s*(W/2-page/2),51,center)*Box(page,14,hi-lo-2*cover)
 # Explicit +Z for both mirrored triangular profiles: polygon winding must not reverse the cut.
 for s in [-1,1]:
  body-=Pos(0,0,lo+cover)*extrude(Plane.XY*Polygon((s*(W/2-page-c),rear_y+wall/2-page),(s*(W/2+2),rear_y+wall/2-page),(s*(W/2+2),rear_y+wall/2-2*page-c-2),align=None),amount=hi-lo-2*cover,dir=(0,0,1))
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
assert len(body.solids())==1
publish('body',body,'小倒角方孔后板')