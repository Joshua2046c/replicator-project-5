from math import sqrt
w=param('buckle_width',42.0);h=param('buckle_height',44.0);t=param('buckle_thickness',1.0);rim=param('buckle_rim',5.0);r=param('buckle_corner_radius',5.0);z=param('buckle_center_z',100.0)
tw=param('buckle_tongue_width',5.0);tl=param('buckle_tongue_length',22.0);tz=param('buckle_tongue_center_z',100.0);tx=param('buckle_tongue_tip_x',0.0)
lift=param('buckle_tongue_relief',0.0) # retained offset parameter; flush contact at zero
R=param('spine_common_radius',88.33333333333333)
# Custom metal bottom-rooted half-height tongue; tz is the preserved tip datum.
H=64.0;ey=-51.0;cz=96.0;cy=ey+sqrt(R*R-H*H/4)
shell=Pos(0,cy-t,cz)*Rot(0,90,0)*Cylinder(R,w)-Pos(0,cy,cz)*Rot(0,90,0)*Cylinder(R,w+2)
outline=Pos(0,-70,z)*Rot(90,0,0)*extrude(RectangleRounded(w,h,r)-RectangleRounded(w-2*rim,h-2*rim,max(0.5,r-2)),amount=40,both=True)
frame=shell&outline&Pos(0,ey-6,z)*Box(w,20,h)
# Analytic circular tongue: back follows the same cylinder as the strap.
# No sampled polygon and no rising free tip. Default metal thickness is 1 mm.
tongue_shell=Pos(tx,cy-t-lift,cz)*Rot(0,90,0)*Cylinder(R,tw)-Pos(tx,cy-lift,cz)*Rot(0,90,0)*Cylinder(R,tw+2)
tongue=tongue_shell&Pos(tx,ey-6,tz-tl/2)*Box(tw,20,tl)
frame+=tongue
# Shared hidden square locating interface; all dimensions in mm.
pegw=param('buckle_mount_peg_width',3.0);pegl=param('buckle_mount_peg_length',2.0)
pegx=param('buckle_mount_center_x',0.0);pegz=param('buckle_mount_center_z',96.0)
pegy=-51.0+sqrt(R*R-32.0**2)-sqrt(R*R-(pegz-96.0)**2)
embed=param('buckle_mount_root_embed',0.3)
frame+=Pos(pegx,pegy+(pegl-embed)/2,pegz)*Box(pegw,pegl+embed,pegw)
assert len(frame.solids())==1
publish('buckle',frame,'贴带曲面金属扣舌',material='stainless_steel')
