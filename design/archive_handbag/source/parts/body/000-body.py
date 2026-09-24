from screwjoint import make_screw_joint_v1
from math import sqrt
W=param('case_width',220.0);H=param('body_height',128.0);floor=param('body_floor',4.0)
wall=param('body_wall',6.0);hy=param('body_hinge_y',58.2);hz=param('body_hinge_z',128.0);hr=param('body_hinge_radius',3.8);bore=param('body_hinge_bore',4.4)
px=param('body_panel_center_x',108.0);slot=param('body_slot_thickness',4.6)
rear_y=param('body_rear_center_y',54.0);groove=param('body_page_depth',0.45);groovew=param('body_page_width',1.0)
sy=param('body_side_pivot_y',0.0);sz=param('body_side_pivot_z',174.0);sd=param('body_side_pivot_hole',4.5)
aw=param('body_carry_arm_thickness',8.0);ad=param('body_carry_arm_depth',20.0);at=param('body_carry_arm_top',184.0);az=param('body_carry_arm_base',110.0);ah=param('body_carry_beam_height',16.0)
ax=param('body_carry_arm_outer_x',106.0);pd=param('body_carry_pad_recess',4.0);pw=param('body_side_pad_pocket_width',14.4);ph=param('body_side_pad_pocket_height',20.4)
wrap=param('body_corner_groove_depth',0.45);lip=param('body_guide_lip_width',7.0)
tl=param('body_tongue_length',70.0);tt=param('body_tongue_thickness',2.4);td=param('body_tongue_depth',2.2);tx=param('body_tongue_x',60.0)
bw=param('body_band_width',30.0);bt=param('body_band_depth',1.0);bend=param('body_band_top',123.5)
nx=param('body_nut_pocket_inner_x',96.5);naf=param('body_nut_pocket_across_flats',7.4);nb=param('body_nut_boss_size',12.0);no=param('body_nut_pocket_outer_x',100.0)
hc=param('body_axle_head_clearance',0.4)
body=Pos(0,rear_y,(H+floor)/2)*Box(W,wall,H-floor)
for s in [-1,1]:
 body+=Pos(s*tx,rear_y,floor-td/2)*Box(tl,tt,td+0.02)
 body+=Pos(s*(W/2-lip/2),49,(H+floor)/2)*Box(lip,8,H-floor)
 body-=Pos(s*px,0,floor)*Box(slot,100.6,H,align=(Align.CENTER,Align.CENTER,Align.MIN))
 beam_front=sy-ad/2;beam_back=rear_y
 body+=Pos(s*(ax-aw/2),(beam_front+beam_back)/2,az+ah/2)*Box(aw,beam_back-beam_front,ah)
 body+=Pos(s*(ax-aw/2),sy,(az+at)/2)*Box(aw,ad,at-az)
 body-=Pos(s*(ax-aw+pd/2),sy-3,sz)*Box(pd,pw,ph)
 body-=Pos(s*(ax-aw/2),sy,sz)*Rot(0,90,0)*Cylinder(sd/2,aw+2)
 # Standard metal M4 nut: unthreaded locating pocket, no printed thread.
 body+=Pos(s*(nx+no)/2,sy,sz)*Box(no-nx,nb,nb)
 nutcut=extrude(RegularPolygon(naf/sqrt(3),6),amount=no-nx+0.4)
 body-=Pos(s*(nx-0.2),sy,sz)*Rot(0,s*90,0)*nutcut
for zz,width in [(64,2.4),(128,2.4)]+[(z,groovew) for a,b in [(12,60),(70,124)] for z in range(a,b,6)]:
 body-=Pos(0,rear_y+wall/2-groove/2,zz)*Box(W+2,groove,width)
 for s in [-1,1]:body-=Pos(s*(W/2-wrap/2),51,zz)*Box(wrap,14,width)
body-=Pos(0,rear_y+wall/2-bt/2,(bend+floor)/2)*Box(bw,bt,bend-floor)
for x in [-39.5,39.5]:
 body+=Pos(x,(rear_y+hy)/2,H-hr/2)*Box(19,hy-rear_y,hr)
 body+=Pos(x,hy,hz)*Rot(0,90,0)*Cylinder(hr,19)
body-=Pos(0,hy,hz)*Rot(0,90,0)*Cylinder(hr+0.6,59.8)
body-=Pos(0,hy,hz)*Rot(0,90,0)*Cylinder(bore/2,100.4)
# Custom pin interface: heads radius3, centers +/-50.7, thickness1.4.
for s in [-1,1]:body-=Pos(s*50.7,hy,hz)*Rot(0,90,0)*Cylinder(3+hc,1.4+2*hc)
for x in [-80,-40,40,80]:
 proxy=Pos(x,rear_y,2)*Box(16,6,4)
 joint=make_screw_joint_v1(size='M3',at=Location((x,rear_y,0),(180,0,0)),through=[(proxy,4)],into=body,engage_depth=8,head='countersunk',material='PETG',label='rear-bottom')
 body=body+joint.bosses-joint.engage_cuts-joint.through_cuts[0]
assert len(body.solids())==1
publish('body',body,'外移铰轴承力后板')