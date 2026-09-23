t=param('side_left_thickness',3.0);d=param('side_left_depth',100.0);h=param('side_left_height',182.4)
g=param('side_left_groove_depth',0.45);gw=param('side_left_groove_width',1.0)
b1=param('side_left_book_boundary1',60.0);b2=param('side_left_book_boundary2',124.0)
pitch=param('side_left_page_pitch',6.0);margin=param('side_left_page_margin',0.0)
by=param('side_left_bolt_y',0.0);bz=param('side_left_bolt_z',170.0);bd=param('side_left_bolt_diameter',4.5)
panel=Box(t,d,h,align=(Align.CENTER,Align.CENTER,Align.MIN))
for z in [b1,b2]:panel-=Pos(-t/2+g/2,0,z)*Box(g,d-2*margin,2.4)
for start,stop in [(8,b1-4),(b1+6,b2-4),(b2+6,h-5)]:
 z=start
 while z<stop:
  panel-=Pos(-t/2+g/2,0,z)*Box(g,d-2*margin,gw);z+=pitch
panel-=Pos(0,by,bz)*Rot(0,90,0)*Cylinder(bd/2,t+2)
publish('side_left',panel,'齐平矩形侧板')