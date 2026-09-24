from math import sqrt
w=param('buckle_width',42.0);h=param('buckle_height',44.0);t=param('buckle_thickness',1.0);rim=param('buckle_rim',5.0);r=param('buckle_corner_radius',5.0);z=param('buckle_center_z',100.0)
tw=param('buckle_tongue_width',5.0);tl=param('buckle_tongue_length',22.0);tz=param('buckle_tongue_center_z',100.0);tx=param('buckle_tongue_tip_x',0.0)
lift=param('buckle_tongue_relief',2.0)
R=param('spine_common_radius',88.33333333333333)
# Custom metal bottom-rooted half-height tongue; tz is the preserved tip datum.
H=64.0;ey=-51.0;cz=96.0;cy=ey+sqrt(R*R-H*H/4)
shell=Pos(0,cy-t,cz)*Rot(0,90,0)*Cylinder(R,w)-Pos(0,cy,cz)*Rot(0,90,0)*Cylinder(R,w+2)
outline=Pos(0,-70,z)*Rot(90,0,0)*extrude(RectangleRounded(w,h,r)-RectangleRounded(w-2*rim,h-2*rim,max(0.5,r-2)),amount=40,both=True)
frame=shell&outline&Pos(0,ey-6,z)*Box(w,20,h)
# Sample true spine curve with a smooth cubic rise, keeping the root bonded to bottom rail.
pts=[]
for i in range(23):
 zz=tz-tl+tl*i/22;u=i/22
 yy=cy-sqrt(R*R-(zz-cz)**2)-lift*(3*u*u-2*u*u*u)
 pts.append((yy,zz))
profile=Plane.YZ*Polygon(*(pts+[(y-t,zz) for y,zz in reversed(pts)]),align=None)
tongue=Pos(tx-tw/2,0,0)*extrude(profile,amount=tw,dir=(1,0,0))
frame+=tongue
assert len(frame.solids())==1
publish('buckle',frame,'底边凸起金属扣舌')