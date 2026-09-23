from screwjoint import make_screw_joint_v1
w=param('lid_width',220.0); d=param('lid_depth',114.0); height=param('lid_height',60.4); roof=param('lid_roof_thickness',2.2); wall=param('lid_wall',6.0)
hy=param('lid_hinge_y',54.0); hz=param('lid_hinge_z',132.0); seam=param('lid_seam_z',128.6)
side_open=param('lid_side_opening',87.8); r=param('lid_barrel_radius',3.8); bore=param('lid_bore',4.4); barrel_l=param('lid_barrel_length',58.8)
rear_inset=param('lid_rear_inset',6.0);side_recess=param('lid_side_recess',5.0)
mx=param('lid_magnet_x',72.0); my=param('lid_magnet_y',-47.0)
b=seam-hz; top=b+height
# The full-width roof caps stationary full-height page panels; moving cheeks stay inboard.
lid=Pos(0,-hy,top-roof)*Box(w,d,roof,align=(Align.CENTER,Align.CENTER,Align.MIN))
lid+=Pos(0,-hy-d/2+wall/2,b)*Box(w-2*side_recess,wall,height,align=(Align.CENTER,Align.CENTER,Align.MIN))
lid+=Pos(0,d/2-hy-rear_inset-wall/2,b)*Box(w-2*side_recess,wall,height,align=(Align.CENTER,Align.CENTER,Align.MIN))
for s in [-1,1]:
 lid-=Pos(s*47.5,-3,b-1)*Box(36.2,15,11.2,align=(Align.CENTER,Align.CENTER,Align.MIN))
lid+=Rot(0,90,0)*Cylinder(r,barrel_l)
lid-=Rot(0,90,0)*Cylinder(bore/2,barrel_l+1)
for s,side in [(-1,'left'),(1,'right')]:
 cid='lid_mag_cap_'+side
 cw=param(cid+'_width',22.0); cd=param(cid+'_depth',14.0); ct=param(cid+'_edge_thickness',2.6); mem=param(cid+'_membrane',0.6); pitch=param(cid+'_screw_half_pitch',8.0)
 lid+=Pos(s*mx,my-hy,b)*Box(28,18,12,align=(Align.CENTER,Align.CENTER,Align.MIN))
 lid-=Pos(s*mx,my-hy,b-0.1)*Cylinder(7.3/2,3.9,align=(Align.CENTER,Align.CENTER,Align.MIN))
 lid-=Pos(s*mx,my-hy,b-0.1)*Box(cw+0.4,cd+0.4,ct+0.1,align=(Align.CENTER,Align.CENTER,Align.MIN))
 cap=Pos(s*mx,my-hy,b+ct/2)*Box(cw,cd,ct)
 cap-=Pos(s*mx,my-hy,b+mem)*Cylinder(4.1,ct-mem+0.1,align=(Align.CENTER,Align.CENTER,Align.MIN))
 for j,dx in enumerate([-pitch,pitch]):
  cap-=Pos(s*mx+dx,my-hy,b-0.1)*Cylinder(2.1,2.1,align=(Align.CENTER,Align.CENTER,Align.MIN))
  joint=make_screw_joint_v1(size='M2',at=Location((s*mx+dx,my-hy,b+2),(180,0,0)),through=[(cap,ct-2)],into=lid,engage_depth=5.4,material='PETG',label=cid+str(j))
  cap-=joint.through_cuts[0];lid=lid+joint.bosses-joint.engage_cuts
  publish(cid+'_screw_'+str(j),joint.hardware,'盖内 M2 螺钉')
 publish(cid,cap,'翻盖磁铁防脱盖')
lid.color=Color(0.91,0.10,0.43)
assert len(lid.solids())==1
publish('lid',lid,'粉色书本翻盖')