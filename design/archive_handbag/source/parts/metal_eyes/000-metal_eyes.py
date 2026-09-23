# Custom 304 top-ring assembly. Reference mounting coordinates retained; outboard pivot clears full lid sweep.
outset=param('swivel_outset',31.0);rise=param('swivel_bracket_rise',2.0)
for oid,s in [('eye_left',-1),('eye_right',1)]:
 t=param(oid+'_thickness',3.0);d=param(oid+'_depth',28.0);h=param(oid+'_height',32.0);r=param(oid+'_corner_radius',5.0)
 sy=param(oid+'_slot_width',14.0);sz=param(oid+'_slot_height',24.0)
 fw=param(oid+'_foot_width',18.0);fd=param(oid+'_foot_depth',18.0);ft=param(oid+'_foot_thickness',2.0);ph=param(oid+'_pivot_bore',6.4)
 cx=param(oid+'_top_x',s*97.0)+s*outset;cy=param(oid+'_top_y',49.0);cz=param(oid+'_top_z',190.3)+rise
 foot=Pos(cx,cy,cz+ft/2)*Box(fw,fd,ft)-Pos(cx,cy,cz)*Cylinder(ph/2,ft,align=(Align.CENTER,Align.CENTER,Align.MIN))
 profile=RectangleRounded(d,h,r)-RectangleRounded(sy,sz,3)
 upright=Pos(cx+s*(fw/2-t),cy,cz+h/2)*extrude(Plane.YZ*profile,amount=s*t)
 ring=foot+upright
 assert len(ring.solids())==1
 publish(oid,ring,'顶部可转背带环')
for oid,s in [('backplate_left',-1),('backplate_right',1)]:
 t=param(oid+'_thickness',2.0);d=param(oid+'_depth',11.0);hole=param(oid+'_hole',4.5);pd=param(oid+'_pad_depth',12.0)
 x=param(oid+'_top_x',s*97.0);y=param(oid+'_top_y',49.0);z=param(oid+'_top_z',178.0)
 p=Pos(x,y,z+t/2)*Box(d,pd,t)-Pos(x,y,z)*Cylinder(hole/2,t,align=(Align.CENTER,Align.CENTER,Align.MIN))
 publish(oid,p,'顶部支座承力垫板')
for side,s in [('left',-1),('right',1)]:
 oid='pivot_sleeve_'+side;od=param(oid+'_diameter',6.0);bd=param(oid+'_bore',4.3);h=param(oid+'_length',2.6);x=param(oid+'_x',s*97.0)+s*outset;y=param(oid+'_y',49.0);z=param(oid+'_z',190.0)+rise
 publish(oid,Pos(x,y,z)*(Cylinder(od/2,h,align=(Align.CENTER,Align.CENTER,Align.MIN))-Cylinder(bd/2,h,align=(Align.CENTER,Align.CENTER,Align.MIN))),'金属转环隔套')
 oid='pivot_washer_'+side;od=param(oid+'_diameter',10.0);bd=param(oid+'_bore',4.3);h=param(oid+'_thickness',1.4);z=param(oid+'_z',192.6)+rise
 publish(oid,Pos(x,y,z)*(Cylinder(od/2,h,align=(Align.CENTER,Align.CENTER,Align.MIN))-Cylinder(bd/2,h,align=(Align.CENTER,Align.CENTER,Align.MIN))),'外侧止推垫片')
 oid='thumb_nut_'+side;od=param(oid+'_diameter',10.0);h=param(oid+'_height',4.0);z=param(oid+'_z',194.0)+rise;knurl=param(oid+'_knurl_depth',0.3)
 # Nominal M4 thread envelope, not manufacturing tap-drill size.
 nut=Cylinder(od/2,h,align=(Align.CENTER,Align.CENTER,Align.MIN))-Cylinder(2.0,h,align=(Align.CENTER,Align.CENTER,Align.MIN))
 for a in range(0,360,15):nut-=Rot(0,0,a)*Pos(od/2,0,h/2)*Box(2*knurl,0.5,h+0.1)
 publish(oid,Pos(x,y,z)*nut,'外置小手拧螺帽')
for side,s in [('left',-1),('right',1)]:
 oid='ring_bridge_'+side
 w=param(oid+'_width',47.0);d=param(oid+'_depth',18.0);t=param(oid+'_thickness',2.0);cx=param(oid+'_center_x',s*113.5);y=param(oid+'_y',49.0);z=param(oid+'_z',190.0)
 inner=param(oid+'_mount_x',s*97.0);outer=inner+s*outset;hole=param(oid+'_hole',4.5);key=param(oid+'_key_drop',5.0);gap=param(oid+'_panel_slot',3.6)
 p=Pos(cx,y,z+t/2)*Box(w,d,t)
 for x in [inner,outer]:p-=Pos(x,y,z)*Cylinder(hole/2,t,align=(Align.CENTER,Align.CENTER,Align.MIN))
 # Rear folded anti-rotation tab bears on the rear board, no reliance on bolt friction alone.
 p+=Pos(inner,58,z-key/2)*Box(14,2,key)
 p+=Pos(inner,57.5,z+t/2)*Box(14,1,t)
 # Slot passes the rectangular side panel on upward extraction.
 p-=Pos(s*107.5,0,z)*Box(gap,100.6,t+2,align=(Align.CENTER,Align.CENTER,Align.MIN))
 publish(oid,p,'顶部外移金属支架')
 oid='bridge_washer_'+side;od=param(oid+'_diameter',10.0);bd=param(oid+'_bore',4.3);h=param(oid+'_thickness',2.0)
 publish(oid,Pos(inner,y,z+t)*(Cylinder(od/2,h,align=(Align.CENTER,Align.CENTER,Align.MIN))-Cylinder(bd/2,h,align=(Align.CENTER,Align.CENTER,Align.MIN))),'支架锁紧垫圈')
 oid='bridge_nut_'+side;od=param(oid+'_diameter',10.0);h=param(oid+'_height',4.0);kn=param(oid+'_knurl_depth',0.3)
 n=Cylinder(od/2,h,align=(Align.CENTER,Align.CENTER,Align.MIN))-Cylinder(2,h,align=(Align.CENTER,Align.CENTER,Align.MIN))
 for a in range(0,360,15):n-=Rot(0,0,a)*Pos(od/2,0,h/2)*Box(2*kn,0.5,h+0.1)
 publish(oid,Pos(inner,y,z+t+2)*n,'支架手拧锁帽')
 oid='pivot_backplate_'+side;w=param(oid+'_width',11.0);d=param(oid+'_depth',12.0);t=param(oid+'_thickness',2.0);bd=param(oid+'_hole',4.5)
 p=Pos(outer,y,z-t/2)*Box(w,d,t)-Pos(outer,y,z-t)*Cylinder(bd/2,t,align=(Align.CENTER,Align.CENTER,Align.MIN))
 publish(oid,p,'转轴下承力垫片')