from screwjoint import make_screw_joint_v1
w=param('lid_width',220.0);d=param('lid_depth',114.0);height=param('lid_height',60.4);roof=param('lid_roof_thickness',2.2);wall=param('lid_wall',6.0)
hy=param('lid_hinge_y',55.0);hz=param('lid_hinge_z',128.0);seam=param('lid_seam_z',128.6)
r=param('lid_barrel_radius',3.8);bore=param('lid_bore',4.4);barrel_l=param('lid_barrel_length',58.8);recess=param('lid_side_recess',5.0)
rw=param('lid_rear_width',176.0);sag=param('lid_spine_sag',6.0);ft=param('lid_spine_thickness',3.5);ey=param('lid_spine_end_y',-51.0)
mx=param('lid_magnet_x',72.0);my=param('lid_magnet_y',-39.0)
relief=param('lid_rear_bottom_relief',4.0);cheek=param('lid_end_cheek_thickness',2.0)
g=param('lid_page_groove_depth',0.45);gw=param('lid_page_groove_width',1.0);wrap=param('lid_corner_groove_depth',1.45)
b=seam-hz;top=b+height
lid=Pos(0,-hy,top-roof)*Box(w,d,roof,align=(Align.CENTER,Align.CENTER,Align.MIN))
rear=Pos(0,d/2-hy-wall/2,b)*Box(rw,wall,height,align=(Align.CENTER,Align.CENTER,Align.MIN))
cut=extrude(Plane.YZ*Polygon((d/2-hy-relief,b-0.1),(d/2-hy+1,b-0.1),(d/2-hy+1,b+relief+1),align=None),amount=rw+2,both=True)
rear-=cut;lid+=rear
R=(height*height/4+sag*sag)/(2*sag);cy=ey+R-sag-hy;cz=b+height/2
curve=(Pos(0,cy,cz)*Rot(0,90,0)*Cylinder(R,w-2*recess)-Pos(0,cy+ft,cz)*Rot(0,90,0)*Cylinder(R,w-2*recess+1))&Pos(0,ey-hy-sag/2+ft,cz)*Box(w-2*recess,2*(sag+ft+1),height)
lid+=curve
for s in [-1,1]:
 cap=Pos(s*(w/2-recess-cheek/2),cy,cz)*Rot(0,90,0)*Cylinder(R,cheek)
 cap &= Pos(s*(w/2-recess-cheek/2),ey-hy-sag/2,cz)*Box(cheek,2*sag,height)
 lid+=cap
 lid-=Pos(s*47.5,-3,b-1)*Box(36.2,18,11.2,align=(Align.CENTER,Align.CENTER,Align.MIN))
lid+=Rot(0,90,0)*Cylinder(r,barrel_l);lid-=Rot(0,90,0)*Cylinder(bore/2,barrel_l+1)
# Full-width grooves, extended across the rear corner to meet side-panel grooves.
for zz in range(134,182,6):
 lid-=Pos(0,d/2-g/2-hy,zz-hz)*Box(rw+2,g,gw)
 for s in [-1,1]:lid-=Pos(s*(rw/2-wrap/2),d/2-wall/2-hy,zz-hz)*Box(wrap,wall+0.1,gw)
for s,side in [(-1,'left'),(1,'right')]:
 cid='lid_mag_cap_'+side
 cw=param(cid+'_width',22.0);cd=param(cid+'_depth',14.0);ct=param(cid+'_edge_thickness',2.6);mem=param(cid+'_membrane',0.6);pitch=param(cid+'_screw_half_pitch',8.0)
 lid+=Pos(s*mx,my-hy-3,b)*Box(28,24,12,align=(Align.CENTER,Align.CENTER,Align.MIN))
 lid-=Pos(s*mx,my-hy,b-0.1)*Cylinder(7.3/2,3.9,align=(Align.CENTER,Align.CENTER,Align.MIN))
 lid-=Pos(s*mx,my-hy,b-0.1)*Box(cw+0.4,cd+0.4,ct+0.1,align=(Align.CENTER,Align.CENTER,Align.MIN))
 cap=Pos(s*mx,my-hy,b+ct/2)*Box(cw,cd,ct);cap-=Pos(s*mx,my-hy,b+mem)*Cylinder(4.1,ct-mem+0.1,align=(Align.CENTER,Align.CENTER,Align.MIN))
 for j,dx in enumerate([-pitch,pitch]):
  cap-=Pos(s*mx+dx,my-hy,b-0.1)*Cylinder(2.1,2.1,align=(Align.CENTER,Align.CENTER,Align.MIN))
  joint=make_screw_joint_v1(size='M2',at=Location((s*mx+dx,my-hy,b+2),(180,0,0)),through=[(cap,ct-2)],into=lid,engage_depth=5.4,material='PETG',label=cid+str(j))
  cap-=joint.through_cuts[0];lid=lid+joint.bosses-joint.engage_cuts;publish(cid+'_screw_'+str(j),joint.hardware,'盖内M2螺钉')
 publish(cid,cap,'翻盖磁铁防脱盖')
assert len(lid.solids())==1
publish('lid',lid,'整幅背板翻盖')