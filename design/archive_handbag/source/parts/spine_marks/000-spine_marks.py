for name,z in [('green_marks',32),('blue_marks',96),('pink_marks',159)]:
 w=param(name+'_bar_width',3.0);h=param(name+'_bar_height',25.0);t=param(name+'_thickness',0.7);x=param(name+'_left_x',-84.0);pitch=param(name+'_pitch',13.0);zz=param(name+'_center_z',z)
 marks=Compound(children=[Pos(xx,-58-t/2,zz)*Box(w,t,h) for xx in [x,x+pitch]])
 marks.color=Color(0.96,0.73,0.14);publish(name,marks,'金色书脊标线')