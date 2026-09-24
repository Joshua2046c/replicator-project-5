t=param('side_left_thickness',4.0);d=param('side_left_depth',100.0);h=param('side_left_height',183.4)
g=param('side_left_groove_depth',0.45);gw=param('side_left_groove_width',1.0)
b1=param('side_left_book_boundary1',60.0);b2=param('side_left_book_boundary2',124.0)
pitch=param('side_left_page_pitch',6.0);margin=param('side_left_page_margin',0.0);page=param('side_left_page_recess',0.25);cover=param('side_left_cover_band',4.0)
by=param('side_left_bolt_y',0.0);bz=param('side_left_bolt_z',170.0);bd=param('side_left_bolt_diameter',4.5)
rr=param('side_left_relief_radius',108.9);ry=param('side_left_relief_axis_y',60.5);rz=param('side_left_relief_axis_z',124.0);start=param('side_left_relief_start_z',124.3)
upperbase=param('side_left_upper_book_base',124.6);uppertop=param('side_left_upper_book_top',186.0)
panel=Box(t,d,h,align=(Align.CENTER,Align.CENTER,Align.MIN))
corner=Pos(0,0,(start+h)/2)*Box(t+2,d+2,h-start)
safe=Pos(0,ry,rz)*Rot(0,90,0)*Cylinder(rr,t+4)
panel-=corner-safe
for lo,hi in [(-4,b1),(b1,b2),(upperbase,uppertop)]:
 center=(lo+hi)/2
 panel-=Pos(-t/2+page/2,0,center)*Box(page,d-2*margin,hi-lo-2*cover)
 for i in range(-4,5):panel-=Pos(-t/2+(page+g)/2,0,center+i*pitch)*Box(page+g,d-2*margin,gw)
for z in [b1,b2]:panel-=Pos(-t/2+g/2,0,z)*Box(g,d-2*margin,0.6)
panel-=Pos(0,by,bz)*Rot(0,90,0)*Cylinder(bd/2,t+2)
publish('side_left',panel,'无侧锁孔左书页')