from screwjoint import make_screw_joint_v1
W=param('case_width',220.0);H=param('body_height',128.0);floor=param('body_floor',4.0)
wall=param('body_wall',6.0);hy=param('body_hinge_y',54.0);hz=param('body_hinge_z',132.0);hr=param('body_hinge_radius',5.0);bore=param('body_hinge_bore',4.4)
px=param('body_panel_center_x',107.5);slot=param('body_slot_thickness',3.6)
postx=param('body_top_post_x',97.0);postw=param('body_top_post_width',14.0);posttop=param('body_top_post_top',190.0);holed=param('body_top_pivot_hole',4.5)
rear_y=param('body_rear_center_y',54.0);pivot_y=param('body_pivot_y',49.0);groove=param('body_page_depth',0.45);groovew=param('body_page_width',1.0)
cw=param('body_corner_cover_width',22.0);cd=param('body_corner_cover_depth',45.2);ct=param('body_corner_cover_thickness',2.2);cz=param('body_corner_cover_top',186.6)
body=Pos(0,rear_y,(H+floor)/2)*Box(W,wall,H-floor)
for s in [-1,1]:
 body+=Pos(s*postx,rear_y,(posttop+H)/2)*Box(postw,wall,posttop-H)
 body+=Pos(s*postx,pivot_y,185)*Box(postw,16,10)
 body+=Pos(s*(W/2-cw/2),rear_y+wall/2-cd/2,cz-ct/2)*Box(cw,cd,ct)
 body-=Pos(s*postx,pivot_y,177)*Cylinder(holed/2,20,align=(Align.CENTER,Align.CENTER,Align.MIN))
 body-=Pos(s*postx,pivot_y,174)*Box(12,13,6,align=(Align.CENTER,Align.CENTER,Align.MIN))
 body+=Pos(s*px,49,(H+floor)/2)*Box(5,8,H-floor)
 body-=Pos(s*px,0,floor)*Box(slot,100.6,posttop,align=(Align.CENTER,Align.CENTER,Align.MIN))
for zz in [64,128]:body-=Pos(0,rear_y+wall/2-groove/2,zz)*Box(W-16,groove,2.4)
for start,stop in [(12,60),(70,124),(134,182)]:
 for zz in range(start,stop,6):body-=Pos(0,rear_y+wall/2-groove/2,zz)*Box(W-16,groove,groovew)
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
publish('body',body,'后侧承力外板')