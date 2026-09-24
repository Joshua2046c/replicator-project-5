from math import sqrt
w=param('lid_width',220.0);d=param('lid_depth',114.0);height=param('lid_height',61.4);roof=param('lid_roof_thickness',2.2);wall=param('lid_wall',6.0)
hy=param('lid_hinge_y',60.5);hz=param('lid_hinge_z',128.0);seam=param('lid_seam_z',128.6)
r=param('lid_barrel_radius',3.8);bore=param('lid_bore',4.4);barrel_l=param('lid_barrel_length',58.8)
rw=param('lid_rear_width',220.0);R=param('spine_common_radius',88.33333333333333);ft=param('lid_spine_thickness',3.5);ey=param('lid_spine_end_y',-51.0)
mx=param('lid_magnet_x',72.0);my=param('lid_magnet_y',-47.0)
relief=param('lid_rear_bottom_relief',0.6);cheek=param('lid_end_cheek_thickness',2.0);sweep=param('lid_cheek_inner_radius',109.5)
g=param('lid_page_groove_depth',0.45);gw=param('lid_page_groove_width',1.0);wrap=param('lid_corner_groove_depth',0.45)
page=param('lid_page_recess',0.25);cover=param('lid_cover_band',4.0);pitch=param('lid_groove_pitch',6.0)
px=param('lid_panel_center_x',108.0);slot=param('lid_panel_clearance_width',4.6)
bw=param('lid_band_width',30.0);bt=param('lid_band_recess',1.0);bs=param('lid_band_rear_start',134.0)
frame=Pos(0,hy-55.0,hz-128.0)
b=seam-hz;top=b+height;sag=R-sqrt(R*R-height*height/4)
lid=Pos(0,(ey+d/2)/2-hy,top-roof)*Box(w,d/2-ey,roof,align=(Align.CENTER,Align.CENTER,Align.MIN))
rear=Pos(0,d/2-hy-wall/2,b)*Box(rw,wall,height,align=(Align.CENTER,Align.CENTER,Align.MIN))
cut=extrude(Plane.YZ*Polygon((d/2-hy-relief,b-0.1),(d/2-hy+1,b-0.1),(d/2-hy+1,b+relief+1),align=None),amount=rw+2,both=True)
rear-=cut;lid+=rear
cy=ey+R-sag-hy;cz=b+height/2
outer=Pos(0,cy,cz)*Rot(0,90,0)*Cylinder(R,w)
curve=(outer-Pos(0,cy+ft,cz)*Rot(0,90,0)*Cylinder(R,w+1))&Pos(0,ey-hy-sag/2+ft,cz)*Box(w,2*(sag+ft+1),height)
safe=Rot(0,90,0)*Cylinder(sweep,w+2)
for s in [-1,1]:
 cx=s*(w/2-cheek/2)
 cap=(Pos(cx,cy,cz)*Rot(0,90,0)*Cylinder(R,cheek))&Pos(cx,(ey-sag)/2-hy,cz)*Box(cheek,sag-ey,height)
 cap-=safe;curve+=cap
 curve-=safe&Pos(s*px,-hy,cz)*Box(slot,120,height+0.2)
lid+=curve
for s in [-1,1]:
 lid-=Pos(s*px,49-hy,b+(height-roof)/2)*Box(slot,2.6,height-roof)
 lid-=Pos(s*39.5,0,0)*Rot(0,90,0)*Cylinder(r+0.6,19.8)
 lid-=Pos(s*50.7,0,0)*Rot(0,90,0)*Cylinder(3.5,2.2)
lid+=Pos(0,(d/2-wall/2-hy)/2,r-0.8)*Box(barrel_l,hy-(d/2-wall/2),1.6)
lid+=Rot(0,90,0)*Cylinder(r,barrel_l)
lid-=Rot(0,90,0)*Cylinder(bore/2,100.4)
# Nine equal-pitch page lines inside a shallow page block, leaving4mm cover bands.
lid-=Pos(0,d/2-page/2-hy,cz)*Box(rw+2,page,height-2*cover)
for s in [-1,1]:lid-=Pos(s*(w/2-page/2),-hy+3,cz)*Box(page,120,height-2*cover)
for i in range(-4,5):
 zz=cz+i*pitch
 lid-=Pos(0,d/2-(page+g)/2-hy,zz)*Box(rw+2,page+g,gw)
 for s in [-1,1]:lid-=Pos(s*(w/2-(page+g)/2),-hy+3,zz)*Box(page+g,120,gw)
for s,side in [(-1,'left'),(1,'right')]:
 oid='lid_magnet_mount_'+side;od=param(oid+'_diameter',11.3);mh=param(oid+'_height',5.4);pd=param(oid+'_pocket_diameter',7.3);dep=param(oid+'_pocket_depth',3.2)
 lid+=(Pos(s*mx,my-hy,b+mh/2)*Cylinder(od/2,mh))&outer
 lid-=Pos(s*mx,my-hy,b-0.1)*Cylinder(pd/2,dep+0.1,align=(Align.CENTER,Align.CENTER,Align.MIN))
band=(outer-Pos(0,cy+bt,cz)*Rot(0,90,0)*Cylinder(R,w+2))&Pos(0,ey-hy,cz)*Box(bw,20,height)
band+=Pos(0,(ey+d/2)/2-hy,top-bt/2)*Box(bw,d/2-ey,bt)
band+=Pos(0,d/2-hy-bt/2,(top+bs-hz)/2)*Box(bw,bt,top-(bs-hz))
lid-=band
assert len(lid.solids())==1
publish('lid',frame*lid,'等距书页与紧凑圆槽翻盖')