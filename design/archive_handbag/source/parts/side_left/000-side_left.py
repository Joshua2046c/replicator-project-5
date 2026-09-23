t=param('side_left_thickness',3.0);d=param('side_left_depth',87.0);h=param('side_left_height',182.4)
g=param('side_left_groove_depth',0.45);gw=param('side_left_groove_width',1.0)
b1=param('side_left_book_boundary1',60.0);b2=param('side_left_book_boundary2',124.0)
ud=param('side_left_upper_depth',114.0);shoulder=param('side_left_upper_shoulder',124.6)
panel=Box(t,d,h,align=(Align.CENTER,Align.CENTER,Align.MIN))
panel+=Pos(0,0,shoulder)*Box(t,ud,h-shoulder,align=(Align.CENTER,Align.CENTER,Align.MIN))
for z in [b1,b2]: panel-=Pos(-t/2+g/2,0,z)*Box(g,d-12,2.4)
for start,stop,dd in [(8,b1-4,d),(b1+6,b2-4,d),(b2+6,h-5,ud)]:
 z=start
 while z<stop:
  panel-=Pos(-t/2+g/2,0,z)*Box(g,dd-12,gw)
  z+=6
panel.color=Color(0.92,0.88,0.76)
publish('side_left',panel,'左侧三层书页插板')