
from math import tan,radians
w=param('width',185.0);h=param('height',49.0);wall=param('wall_thickness',6.0)
top=param('top_from_axis',3.0);inner=param('inner_from_axis',0.15)
old_y=param('lower_axis_y',9.65);old_z=param('lower_axis_z',-46.6)
old_r=param('lower_barrel_radius',3.8);old_bore=param('lower_bore',4.4);mid=param('central_length',58.8)
shape=Pos(0,inner+wall/2,top-h/2)*Box(w,wall,h)
page=param('page_recess',0.25);cover=param('cover_border',4.0)
groove=param('groove_depth',0.45);gw=param('groove_width',1.0);pitch=param('groove_pitch',4.8)
shape-=Pos(0,inner+wall-page/2,top-h/2)*Box(w+2,page,h-2*cover)
for i in range(-4,5):
 shape-=Pos(0,inner+wall-(page+groove)/2,top-h/2+i*pitch)*Box(w+2,page+groove,gw)

for s in [-1,1]:
 shape-=Pos(s*(w/2-page/2),inner+wall/2,top-h/2)*Box(page,wall+2,h-2*cover)
 for i in range(-4,5):
  shape-=Pos(s*(w/2-(page+groove)/2),inner+wall/2,top-h/2+i*pitch)*Box(page+groove,wall+2,gw)
# Preserve the original lower rear hinge and clearance to its body forks.
for s in [-1,1]:
 shape-=Pos(s*90.5,-1.85,top-h/2)*Box(4.6,2.6,h)
 shape-=Pos(s*39.5,old_y,old_z)*Rot(0,90,0)*Cylinder(old_r+0.6,19.8)
 shape-=Pos(s*50.7,old_y,old_z)*Rot(0,90,0)*Cylinder(3.5,2.2)
shape+=Pos(0,(inner+wall/2+old_y)/2,old_z+old_r-0.8)*Box(mid,old_y-inner-wall/2,1.6)
shape+=Pos(0,old_y,old_z)*Rot(0,90,0)*Cylinder(old_r,mid)
shape-=Pos(0,old_y,old_z)*Rot(0,90,0)*Cylinder(old_bore/2,100.4)
# Bottom edge relief and rear strap seat.
relief=param('lower_edge_relief',0.6)
shape-=extrude(Plane.YZ*Polygon((inner+wall-relief,top-h-0.1),(inner+wall+1,top-h-0.1),(inner+wall+1,top-h+relief+1),align=None),amount=w+2,both=True)
bw=param('binding_width',45.0);bd=param('binding_recess',1.0);base=param('binding_base',-40.6)
shape-=Pos(0,inner+wall-bd/2,(top+base)/2)*Box(bw,bd,top-base)
shape-=Pos(0,inner+wall/2,top-bd/2)*Box(bw,wall+2,bd)
# Preserve the user-set R3 rear corners and their continuous page grooves.
cr=param('rear_corner_radius',3.0)
for s in [-1,1]:
 xc=s*(w/2-cr);yc=inner+wall-cr
 def corner_cut(radius,z0,span):
  square=Pos(s*(w/2-cr/2),inner+wall-cr/2,z0)*Box(cr,cr,span,align=(Align.CENTER,Align.CENTER,Align.MIN))
  disk=Pos(xc,yc,z0)*Cylinder(radius,span,align=(Align.CENTER,Align.CENTER,Align.MIN))
  return square-disk
 shape-=corner_cut(cr,top-h-1,h+2)
 shape-=corner_cut(cr-page,top-h+cover,h-2*cover)
 for i in range(-4,5): shape-=corner_cut(cr-page-groove,top-h/2+i*pitch-gw/2,gw)
# Back cover folds inward after the roof has been lifted.
angle=param('opening_relief_deg',30.0)
shape-=extrude(Plane.YZ*Polygon((inner,0),(-20,0),(-20,20),(inner+tan(radians(angle))*20,20),align=None),amount=w+2,both=True)
r=param('knuckle_radius',3.0);bore=param('pin_bore',3.4);outer=param('fork_length',52.0)
cx=mid/2+0.6+outer/2;web=param('web_depth',4.5);wh=param('web_height',3.0)
for s in [-1,1]:
 shape+=Pos(s*cx,web/2,0)*Box(outer,web,wh)
 shape+=Pos(s*cx,0,0)*Rot(0,90,0)*Cylinder(r,outer)
clear=param('knuckle_clearance_radius',3.3);capr=param('cap_clearance_radius',3.2);capx=param('cap_clearance_x',84.9)
shape-=Rot(0,90,0)*Cylinder(clear,mid+1.0)
for s in [-1,1]: shape-=Pos(s*capx,0,0)*Rot(0,90,0)*Cylinder(capr,4.4)
shape-=Rot(0,90,0)*Cylinder(bore/2,w+2)
assert shape.is_valid and len(shape.solids())==1
publish('rear_fold_cover',shape,'后书面内轴折叠板',material='petg')
