from math import sqrt
R=param('spine_common_radius',88.33333333333333)
for name,z,H in [('green_marks',32,64.0),('blue_marks',96,64.0),('pink_marks',159.3,61.4)]:
 w=param(name+'_bar_width',3.0);h=param(name+'_bar_height',25.0);t=param(name+'_thickness',0.7);x=param(name+'_left_x',-84.0);pitch=param(name+'_pitch',13.0);zz=param(name+'_center_z',z)
 span=param(name+'_spine_height',H);ey=param(name+'_end_y',-51.0)
 dep=param(name+'_pocket_depth',1.2);bed=param(name+'_bottom_allowance',0.1)
 sag=R-sqrt(R*R-span*span/4);cy=ey+R-sag
 bars=[]
 for xx in [x,x+pitch]:
  # Same outer crown as before, now extending1.1mm into its own matching blind slot.
  bar=(Pos(xx,cy,zz)*Rot(0,90,0)*Cylinder(R+t,w)-Pos(xx,cy,zz)*Rot(0,90,0)*Cylinder(R-dep+bed,w+1))&Pos(xx,ey-sag,zz)*Box(w,2*(sag+t+dep),h)
  bars.append(bar)
 publish(name,Compound(children=bars),'曲面插入书脊饰块')