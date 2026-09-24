w=param('buckle_width',42.0);h=param('buckle_height',44.0);t=param('buckle_thickness',1.0);rim=param('buckle_rim',5.0);r=param('buckle_corner_radius',5.0);z=param('buckle_center_z',100.0)
# Matched blue book outer arc from front panel interface, not a floating planar frame.
H=64.0;sag=6.0;ey=-51.0;cz=96.0;R=(H*H/4+sag*sag)/(2*sag);cy=ey+R-sag
shell=Pos(0,cy-t,cz)*Rot(0,90,0)*Cylinder(R,w)-Pos(0,cy,cz)*Rot(0,90,0)*Cylinder(R,w+2)
outline=Pos(0,-70,z)*Rot(90,0,0)*extrude(RectangleRounded(w,h,r)-RectangleRounded(w-2*rim,h-2*rim,max(0.5,r-2)),amount=40,both=True)
frame=shell&outline&Pos(0,ey-sag,z)*Box(w,20,h)
publish('buckle',frame,'贴面空心扣框')