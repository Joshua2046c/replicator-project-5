for name,z,H in [('green_marks',32,60.0),('blue_marks',96,64.0),('pink_marks',159,60.4)]:
 w=param(name+'_bar_width',3.0);h=param(name+'_bar_height',25.0);t=param(name+'_thickness',0.7);x=param(name+'_left_x',-84.0);pitch=param(name+'_pitch',13.0);zz=param(name+'_center_z',z)
 sag=param(name+'_spine_sag',6.0);span=param(name+'_spine_height',H);ey=param(name+'_end_y',-51.0)
 R=(span*span/4+sag*sag)/(2*sag);cy=ey+R-sag
 bars=[]
 for xx in [x,x+pitch]:
  bar=(Pos(xx,cy,zz)*Rot(0,90,0)*Cylinder(R+t,w)-Pos(xx,cy,zz)*Rot(0,90,0)*Cylinder(R,w+1))&Pos(xx,ey-sag,zz)*Box(w,2*(sag+t),h)
  bars.append(bar)
 publish(name,Compound(children=bars),'随弧面书脊标线')