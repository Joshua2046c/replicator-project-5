
# Overall height drives the existing 190mm design basis; stock thickness and hardware stay unchanged.
height_ratio=param('case_height',152.0)/190.0
# cell: side_right
from math import sqrt
t=param('side_right_thickness',4.0);d=param('side_right_depth',100.0);h=param('side_right_height',183.4)
g=param('side_right_groove_depth',0.45);gw=param('side_right_groove_width',1.0)
b1=param('side_right_book_boundary1',60.0);b2=param('side_right_book_boundary2',124.0)
pitch=param('side_right_page_pitch',6.0);margin=param('side_right_page_margin',0.0);page=param('side_right_page_recess',0.25);cover=param('side_right_cover_band',4.0)
by=param('side_right_bolt_y',0.0);bz=param('side_right_bolt_z',170.0);bd=param('side_right_bolt_diameter',4.5)
rr=param('side_right_relief_radius',108.9);ry=param('side_right_relief_axis_y',60.5);rz=param('side_right_relief_axis_z',124.0);start=param('side_right_relief_start_z',124.3)
upperbase=param('side_right_upper_book_base',124.6);uppertop=param('side_right_upper_book_top',186.0)
R=param('spine_common_radius',88.33333333333333);ey=param('side_right_spine_end_y',-51.0);c=param('side_right_outer_chamfer',0.4)
lap=param('spine_lap_rear_y',-47.5)
gap=param('side_right_front_clearance',0.3)

# Preserve the existing spine sag while shortening its chord.
sag_basis=R-sqrt(R*R-32.0**2)
R=(32.0*height_ratio)**2/(2*sag_basis)+sag_basis/2
h=190.0*height_ratio-(190.0-h)
bz=190.0*height_ratio-(190.0-(bz+4))-4
b1=(b1+4)*height_ratio-4;b2=(b2+4)*height_ratio-4
start=(rz+4)*height_ratio-4+(start-rz)
rz=(rz+4)*height_ratio-4
upperbase=(128.0*height_ratio+0.6-4)+(upperbase-124.6)
uppertop=190.0*height_ratio-4+(uppertop-186)
pitch*=height_ratio
front=lap+gap
# Straight front edge permits upward withdrawal behind the full-width curved spine.
panel=Pos(0,(front+d/2)/2,0)*Box(t,d/2-front,h,align=(Align.CENTER,Align.CENTER,Align.MIN))
edge=[e for e in panel.edges().filter_by(Axis.Z) if abs(e.center().X-t/2)<1e-6 and abs(e.center().Y-front)<1e-6]
panel=chamfer(edge,c)
corner=Pos(0,0,(start+h)/2)*Box(t+2,d+2,h-start)
safe=Pos(0,ry,rz)*Rot(0,90,0)*Cylinder(rr,t+4)
panel-=corner-safe
for lo,hi in [(-4,b1),(b1,b2),(upperbase,uppertop)]:
 center=(lo+hi)/2
 panel-=Pos(t/2-page/2,-R/2,center)*Box(page,d+R-2*margin,hi-lo-2*cover)
 for i in range(-4,5):panel-=Pos(t/2-(page+g)/2,-R/2,center+i*pitch)*Box(page+g,d+R-2*margin,gw)
for z in [b1,b2]:panel-=Pos(t/2-g/2,-R/2,z)*Box(g,d+R-2*margin,0.6)
panel-=Pos(0,by,bz)*Rot(0,90,0)*Cylinder(bd/2,t+2)
assert len(panel.solids())==1
# The front edge is now straight; no circular-spine subdivision is needed here.
assert panel.is_valid
publish('side_right',panel,'内收下插右书页板')