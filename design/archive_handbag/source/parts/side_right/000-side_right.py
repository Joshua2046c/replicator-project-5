t=param('side_right_thickness',4.0);d=param('side_right_depth',100.0);h=param('side_right_height',182.4)
g=param('side_right_groove_depth',0.45);gw=param('side_right_groove_width',1.0)
b1=param('side_right_book_boundary1',60.0);b2=param('side_right_book_boundary2',124.0)
pitch=param('side_right_page_pitch',6.0);margin=param('side_right_page_margin',0.0)
by=param('side_right_bolt_y',0.0);bz=param('side_right_bolt_z',170.0);bd=param('side_right_bolt_diameter',4.5)
rr=param('side_right_relief_radius',108.4);ry=param('side_right_relief_axis_y',60.0);rz=param('side_right_relief_axis_z',124.0);start=param('side_right_relief_start_z',124.3)
topmargin=param('side_right_page_end_margin',1.0)
panel=Box(t,d,h,align=(Align.CENTER,Align.CENTER,Align.MIN))
corner=Pos(0,0,(start+h)/2)*Box(t+2,d+2,h-start)
safe=Pos(0,ry,rz)*Rot(0,90,0)*Cylinder(rr,t+4)
panel-=corner-safe
for z in [b1,b2]:panel-=Pos(t/2-g/2,0,z)*Box(g,d-2*margin,2.4)
for begin,stop in [(8,b1-4),(b1+6,b2-4),(b2+6,h-topmargin)]:
 z=begin
 while z<stop:
  panel-=Pos(t/2-g/2,0,z)*Box(g,d-2*margin,gw);z+=pitch
panel-=Pos(0,by,bz)*Rot(0,90,0)*Cylinder(bd/2,t+2)
publish('side_right',panel,'补齐上层页槽的圆弧插板')