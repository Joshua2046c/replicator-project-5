from screwjoint import make_screw_joint_v1
W=param('case_width',220.0);H=param('body_height',128.0);floor=param('body_floor',4.0)
wall=param('body_wall',6.0);hy=param('body_hinge_y',55.0);hz=param('body_hinge_z',128.0);hr=param('body_hinge_radius',3.8);bore=param('body_hinge_bore',4.4)
px=param('body_panel_center_x',107.5);slot=param('body_slot_thickness',3.6)
rear_y=param('body_rear_center_y',54.0);groove=param('body_page_depth',0.45);groovew=param('body_page_width',1.0)
sy=param('body_side_pivot_y',54.0);sz=param('body_side_pivot_z',116.0);sd=param('body_side_pivot_hole',4.5)
sw=param('body_side_pad_width',12.0);dep=param('body_side_pad_depth',14.0);sh=param('body_side_pad_height',28.0)
pocket=param('body_side_pad_pocket_depth',8.0);pw=param('body_side_pad_pocket_width',12.4);ph=param('body_side_pad_pocket_height',20.4)
wrap=param('body_corner_groove_depth',1.45)
body=Pos(0,rear_y,(H+floor)/2)*Box(W,wall,H-floor)
for s in [-1,1]:
 body+=Pos(s*(W/2-sw/2),rear_y+wall/2-dep/2,H-sh/2)*Box(sw,dep,sh)
 body+=Pos(s*px,49,(H+floor)/2)*Box(5,8,H-floor)
 body-=Pos(s*px,0,floor)*Box(slot,100.6,H,align=(Align.CENTER,Align.CENTER,Align.MIN))
 # Pocket for inside steel load spreader opens into the cavity and above the rear edge.
 body-=Pos(s*(102-pocket/2),51,sz)*Box(pocket,pw,ph)
 body-=Pos(s*105,sy,sz)*Rot(0,90,0)*Cylinder(sd/2,24)
# Matching grooves extend to each edge and round the rear corner guide lips.
for zz,width in [(64,2.4),(128,2.4)]+[(z,groovew) for a,b in [(12,60),(70,124)] for z in range(a,b,6)]:
 body-=Pos(0,rear_y+wall/2-groove/2,zz)*Box(W+2,groove,width)
 for s in [-1,1]:body-=Pos(s*(W/2-wrap/2),51,zz)*Box(wrap,14,width)
body-=Pos(0,hy,hz)*Rot(0,90,0)*Cylinder(hr+0.6,59.8)
for x in [-39.5,39.5]:body+=Pos(x,hy,hz)*Rot(0,90,0)*Cylinder(hr,19)
body-=Pos(0,hy,hz)*Rot(0,90,0)*Cylinder(bore/2,100.4)
for x in [-80,-40,40,80]:
 proxy=Pos(x,rear_y,2)*Box(16,6,4)
 joint=make_screw_joint_v1(size='M3',at=Location((x,rear_y,0),(180,0,0)),through=[(proxy,4)],into=body,engage_depth=8,head='countersunk',material='PETG',label='rear-bottom')
 body=body+joint.bosses-joint.engage_cuts
for s,side in [(-1,'left'),(1,'right')]:
 cid='axle_stop_'+side
 w=param(cid+'_width',12.0);d=param(cid+'_depth',6.0);t=param(cid+'_base_thickness',3.0);sh=param(cid+'_stop_height',9.0);st=param(cid+'_stop_thickness',2.0);x=param(cid+'_inner_x',50.4)
 cap=Pos(s*(x+w/2),hy,H+t/2)*Box(w,d,t)
 cap+=Pos(s*(x+st/2),hy,H+sh/2)*Box(st,d,sh)
 joint=make_screw_joint_v1(size='M3',at=Location((s*(x+w-3.5),hy,H+t)),through=[(cap,t)],into=body,engage_depth=7,material='PETG',label=cid)
 cap-=joint.through_cuts[0];body=body+joint.bosses-joint.engage_cuts
 publish(cid,cap,'轴端止挡');publish(cid+'_screw',joint.hardware,'止挡螺钉')
assert len(body.solids())==1
publish('body',body,'侧轴承力后外板')