t=param('side_right_thickness',3.0);d=param('side_right_depth',87.0);h=param('side_right_height',182.4)
g=param('side_right_groove_depth',0.45);gw=param('side_right_groove_width',1.0)
b1=param('side_right_book_boundary1',60.0);b2=param('side_right_book_boundary2',124.0)
pitch=param('side_right_page_pitch',6.0);margin=param('side_right_page_margin',6.0)
panel=Box(t,d,h,align=(Align.CENTER,Align.CENTER,Align.MIN))
for z in [b1,b2]:panel-=Pos(t/2-g/2,0,z)*Box(g,d-2*margin,2.4)
for start,stop in [(8,b1-4),(b1+6,b2-4),(b2+6,h-5)]:
 z=start
 while z<stop:
  panel-=Pos(t/2-g/2,0,z)*Box(g,d-2*margin,gw);z+=pitch
publish('side_right',panel,'右侧矩形书页板')