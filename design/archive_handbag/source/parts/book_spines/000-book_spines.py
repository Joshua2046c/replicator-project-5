for oid,z,h,col in [('green_spine',32,58,(0.03,0.48,0.27)),('blue_spine',96,59,(0.15,0.17,0.68)),('pink_spine',159,55,(0.94,0.09,0.45))]:
 w=param(oid+'_width',216.0);hh=param(oid+'_height',h);t=param(oid+'_thickness',1.0);rr=param(oid+'_corner_radius',3.0);zz=param(oid+'_center_z',z);yy=param(oid+'_mount_y',-57.0)
 plate=extrude(RectangleRounded(w,hh,rr),amount=t)
 plate=Pos(0,yy,zz)*Rot(90,0,0)*plate
 plate.color=Color(*col)
 publish(oid,plate,{'green_spine':'绿色下层书脊','blue_spine':'蓝色中层书脊','pink_spine':'粉色上层书脊'}[oid])
# Decorative adhesive-backed panels, not load-bearing closures.