# Nominal envelopes regenerated for outer-panel revision; not supplier STEP models.
for oid,x,z in [('body_magnet_left',-72,124.2),('body_magnet_right',72,124.2),('lid_magnet_left',-72,129.4),('lid_magnet_right',72,129.4)]:
 dia=param(oid+'_diameter',7.0);h=param(oid+'_thickness',3.0);xx=param(oid+'_center_x',x);yy=param(oid+'_center_y',-47.0);zz=param(oid+'_bottom_z',z)
 publish(oid,Pos(xx,yy,zz)*Cylinder(dia/2,h,align=(Align.CENTER,Align.CENTER,Align.MIN)),'磁铁规格包络7×3')