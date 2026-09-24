from math import sqrt
w=param('buckle_width',42.0);h=param('buckle_height',44.0);t=param('buckle_thickness',1.0);rim=param('buckle_rim',5.0);r=param('buckle_corner_radius',5.0);z=param('buckle_center_z',100.0)
tw=param('buckle_tongue_width',5.0);tl=param('buckle_tongue_length',22.0);tz=param('buckle_tongue_center_z',100.0);tx=param('buckle_tongue_tip_x',0.0)
R=param('spine_common_radius',88.33333333333333)
# Custom metal frame with integral half-width tongue from left rail to centre, no centre block.
H=64.0;ey=-51.0;cz=96.0;cy=ey+sqrt(R*R-H*H/4)
shell=Pos(0,cy-t,cz)*Rot(0,90,0)*Cylinder(R,w)-Pos(0,cy,cz)*Rot(0,90,0)*Cylinder(R,w+2)
outline=Pos(0,-70,z)*Rot(90,0,0)*extrude(RectangleRounded(w,h,r)-RectangleRounded(w-2*rim,h-2*rim,max(0.5,r-2)),amount=40,both=True)
outline+=Pos(tx-tl/2,-70,tz)*Box(tl,80,tw)
frame=shell&outline&Pos(0,ey-6,z)*Box(w,20,h)
assert len(frame.solids())==1
publish('buckle',frame,'半截金属舌方扣框')