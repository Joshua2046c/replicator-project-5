t=param('side_left_thickness',3.0);d=param('side_left_depth',87.0);h=param('side_left_height',182.4)
g=param('side_left_groove_depth',0.45);gw=param('side_left_groove_width',1.0)
b1=param('side_left_book_boundary1',60.0);b2=param('side_left_book_boundary2',124.0)
pitch=param('side_left_page_pitch',6.0);margin=param('side_left_page_margin',6.0)
panel=Box(t,d,h,align=(Align.CENTER,Align.CENTER,Align.MIN))
for z in [b1,b2]:panel-=Pos(-t/2+g/2,0,z)*Box(g,d-2*margin,2.4)
for start,stop in [(8,b1-4),(b1+6,b2-4),(b2+6,h-5)]:
 z=start
 while z<stop:
  panel-=Pos(-t/2+g/2,0,z)*Box(g,d-2*margin,gw);z+=pitch
publish('side_left',panel,'左侧矩形书页板')