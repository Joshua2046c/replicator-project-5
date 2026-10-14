
# Roof between two independently folding covers; axes remain inside the case.
w=param('lid_width',185.0);d=param('lid_depth',119.0)
z=param('case_height',152.0);t=param('lid_roof_thickness',2.2)
front=param('fold_axis_y',-49.85);back=param('rear_fold_axis_y',53.35)
az=param('inner_hinge_axis_z',149.0);gap=param('fold_seam_gap',0.3)
r=param('inner_hinge_radius',3.0);bore=param('inner_hinge_bore',3.4)
mid=param('fold_central_barrel_length',58.8)
clear=param('inner_fork_clearance_radius',3.3)
shape=Pos(0,(front+back)/2,z-t/2)*Box(w,back-front-gap,t)
bw=param('lid_band_width',45.0);bt=param('lid_band_recess',1.0)
shape-=Pos(0,(front+back)/2,z-bt/2)*Box(bw,back-front,bt)
# A single constant cross-section along the entire edge removes all separator
# tabs and cap notches. Central barrels join through inward underside webs.
web_t=param('hinge_web_thickness',1.2)
web_reach=param('hinge_web_reach',4.3)
for y,sign in [(front,1),(back,-1)]:
 shape-=Pos(0,y,az)*Rot(0,90,0)*Cylinder(clear,w+2)
 web=Pos(0,y+sign*web_reach/2,z-t+web_t/2)*Box(mid,web_reach,web_t)
 shape+=web
 shape+=Pos(0,y,az)*Rot(0,90,0)*Cylinder(r,mid)
 shape-=Pos(0,y,az)*Rot(0,90,0)*Cylinder(bore/2,w+2)
nw=param('nameplate_width',22.2222222222222);nl=param('nameplate_length',60.0)
nx=param('nameplate_x',-57.5);ny=param('nameplate_y',4.0)
nd=param('nameplate_pocket_depth',1.0);nc=param('nameplate_clearance',0.15);nr=param('nameplate_corner_radius',3.0)
shape-=Pos(nx,ny,z-nd)*extrude(RectangleRounded(nw+2*nc,nl+2*nc,nr+nc),amount=nd+1)
assert shape.is_valid and len(shape.solids())==1
publish('lid',Pos(0,-55,-128)*shape,'双内轴折叠顶盖',material='petg')
