# Deliberately custom planar 304 side swivel rings; no top bridges or welded feet.
for side,s in [('left',-1),('right',1)]:
 oid='eye_'+side
 t=param(oid+'_thickness',3.0);d=param(oid+'_depth',28.0);h=param(oid+'_height',32.0);r=param(oid+'_corner_radius',5.0)
 sy=param(oid+'_slot_width',14.0);sz=param(oid+'_slot_height',24.0);ph=param(oid+'_pivot_bore',6.4)
 x=param(oid+'_side_x',s*110.3);y=param(oid+'_side_y',54.0);z=param(oid+'_side_z',116.0)
 off=param(oid+'_outline_offset_z',14.0);so=param(oid+'_slot_offset_z',20.0)
 profile=Pos(0,off)*RectangleRounded(d,h,r)-Pos(0,so)*RectangleRounded(sy,sz,3)-Circle(ph/2)
 ring=Pos(x,y,z)*extrude(Plane.YZ*profile,amount=s*t)
 publish(oid,ring,'侧装可转挂环')
 oid='backplate_'+side
 t=param(oid+'_thickness',2.0);d=param(oid+'_depth',11.0);h=param(oid+'_height',20.0);hole=param(oid+'_hole',4.5)
 x=param(oid+'_side_x',s*100.0);y=param(oid+'_side_y',51.0);z=param(oid+'_side_z',116.0);off=param(oid+'_hole_offset_y',3.0)
 p=Pos(x+s*t/2,y,z)*Box(t,d,h)-Pos(x,y+off,z)*Rot(0,s*90,0)*Cylinder(hole/2,t,align=(Align.CENTER,Align.CENTER,Align.MIN))
 publish(oid,p,'侧轴承力垫板')
 oid='pivot_sleeve_'+side;od=param(oid+'_diameter',6.0);bd=param(oid+'_bore',4.3);h=param(oid+'_length',2.6)
 x=param(oid+'_side_x',s*110.0);y=param(oid+'_side_y',54.0);z=param(oid+'_side_z',116.0)
 publish(oid,Pos(x,y,z)*Rot(0,s*90,0)*(Cylinder(od/2,h,align=(Align.CENTER,Align.CENTER,Align.MIN))-Cylinder(bd/2,h,align=(Align.CENTER,Align.CENTER,Align.MIN))),'侧轴金属隔套')
 oid='pivot_washer_'+side;od=param(oid+'_diameter',10.0);bd=param(oid+'_bore',4.3);t=param(oid+'_thickness',1.4)
 publish(oid,Pos(x+s*h,y,z)*Rot(0,s*90,0)*(Cylinder(od/2,t,align=(Align.CENTER,Align.CENTER,Align.MIN))-Cylinder(bd/2,t,align=(Align.CENTER,Align.CENTER,Align.MIN))),'侧轴止推垫片')
 oid='thumb_nut_'+side;od=param(oid+'_diameter',10.0);nh=param(oid+'_height',4.0);kn=param(oid+'_knurl_depth',0.3)
 nut=Cylinder(od/2,nh,align=(Align.CENTER,Align.CENTER,Align.MIN))-Cylinder(2,nh,align=(Align.CENTER,Align.CENTER,Align.MIN)) # M4 nominal thread envelope
 for a in range(0,360,15):nut-=Rot(0,0,a)*Pos(od/2,0,nh/2)*Box(2*kn,0.5,nh+0.1)
 publish(oid,Pos(x+s*(h+t),y,z)*Rot(0,s*90,0)*nut,'外侧小手拧螺帽')