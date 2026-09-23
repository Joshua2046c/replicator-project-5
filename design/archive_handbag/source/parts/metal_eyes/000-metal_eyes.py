# Custom 304 stainless plate eyelets, not supplier D-ring models.
for oid,s in [('eye_left',-1),('eye_right',1)]:
 t=param(oid+'_thickness',3.0);d=param(oid+'_depth',36.0);h=param(oid+'_height',42.0);r=param(oid+'_corner_radius',5.0)
 sy=param(oid+'_slot_width',14.0);sz=param(oid+'_slot_height',24.0);sc=param(oid+'_slot_offset_y',6.0);hd=param(oid+'_mount_hole',4.5);pitch=param(oid+'_mount_pitch',20.0)
 cx=param(oid+'_mount_x',s*110.0);cy=param(oid+'_center_y',58.0);cz=param(oid+'_center_z',100.0)
 profile=RectangleRounded(d,h,r)-Pos(sc,0)*RectangleRounded(sy,sz,3)
 for z in [-pitch/2,pitch/2]: profile-=Pos(-11.5,z)*Circle(hd/2)
 eye=Pos(cx,cy,cz)*extrude(Plane.YZ*profile,amount=s*t)
 eye.color=Color(0.6,0.62,0.65);publish(oid,eye,'独立金属穿带环')
for oid,s in [('backplate_left',-1),('backplate_right',1)]:
 t=param(oid+'_thickness',2.0);d=param(oid+'_depth',11.0);h=param(oid+'_height',40.0);hole=param(oid+'_hole',4.5);pitch=param(oid+'_hole_pitch',20.0)
 cx=param(oid+'_outer_x',s*100.0);cy=param(oid+'_center_y',45.5);cz=param(oid+'_center_z',100.0)
 profile=RectangleRounded(d,h,2)
 for z in [-pitch/2,pitch/2]: profile-=Pos(1,z)*Circle(hole/2)
 plate=Pos(cx,cy,cz)*extrude(Plane.YZ*profile,amount=-s*t)
 publish(oid,plate,'金属承力背板')