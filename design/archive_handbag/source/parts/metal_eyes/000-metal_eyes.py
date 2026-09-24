# Custom metal swivel hardware; the M4 nut is an exact separately imported ISO4032 asset.
for side,s in [('left',-1),('right',1)]:
 oid='eye_'+side
 t=param(oid+'_thickness',3.0);d=param(oid+'_depth',28.0);h=param(oid+'_height',44.0);r=param(oid+'_corner_radius',5.0)
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
 oid='pivot_sleeve_'+side;od=param(oid+'_diameter',6.0);bd=param(oid+'_bore',4.3);h=param(oid+'_length',3.6)
 x=param(oid+'_side_x',s*110.0);y=param(oid+'_side_y',54.0);z=param(oid+'_side_z',116.0)
 publish(oid,Pos(x,y,z)*Rot(0,s*90,0)*(Cylinder(od/2,h,align=(Align.CENTER,Align.CENTER,Align.MIN))-Cylinder(bd/2,h,align=(Align.CENTER,Align.CENTER,Align.MIN))),'侧轴金属隔套')
 oid='pivot_washer_'+side;od=param(oid+'_diameter',10.0);bd=param(oid+'_bore',4.3);t=param(oid+'_thickness',1.4)
 # Washer dimensions now drive the integral flange on the custom metal screw.
 flange_d=od;flange_t=t
 oid='thumb_screw_'+side
 hd=param(oid+'_head_diameter',10.0);hh=param(oid+'_head_height',4.0);length=param(oid+'_shaft_length',20.0);kn=param(oid+'_knurl_depth',0.3)
 sx=param(oid+'_head_x',s*115.0);sy=param(oid+'_axis_y',0.0);sz=param(oid+'_axis_z',174.0)
 # M4-0.7 metal thread per matching ISO4032 nut; nominal major-diameter envelope, not printed thread.
 shaft_d=4.0
 screw=Pos(0,0,-length)*Cylinder(shaft_d/2,length,align=(Align.CENTER,Align.CENTER,Align.MIN))+Cylinder(hd/2,hh,align=(Align.CENTER,Align.CENTER,Align.MIN))
 screw+=Pos(0,0,-flange_t)*Cylinder(flange_d/2,flange_t,align=(Align.CENTER,Align.CENTER,Align.MIN))
 for a in range(0,360,15):screw-=Rot(0,0,a)*Pos(hd/2,0,hh/2)*Box(2*kn,0.5,hh+0.1)
 assert len(screw.solids())==1
 publish(oid,Pos(sx,sy,sz)*Rot(0,s*90,0)*screw,'一体金属手拧螺丝')