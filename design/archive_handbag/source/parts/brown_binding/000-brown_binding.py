from math import sqrt
R=param('spine_common_radius',88.33333333333333)
w=param('lower_binding_width',30.0);t=param('lower_binding_thickness',1.0)
front=param('lower_binding_front_y',-51.0);rear=param('lower_binding_rear_y',57.0);bottom=param('lower_binding_base_z',0.0);backtop=param('lower_binding_back_top',123.5)
cy=front+sqrt(R*R-32.0**2)
band=Pos(0,(front-8+rear)/2,bottom+t/2)*Box(w,rear-front+8,t)&Pos(0,cy,32)*Rot(0,90,0)*Cylinder(R,w)
band+=Pos(0,rear-t/2,backtop/2)*Box(w,t,backtop)
for z,h in [(32.0,64.0),(96.0,64.0)]:
 cy=front+sqrt(R*R-h*h/4)
 strip=(Pos(0,cy,z)*Rot(0,90,0)*Cylinder(R,w)-Pos(0,cy+t,z)*Rot(0,90,0)*Cylinder(R,w+2))&Pos(0,front,z)*Box(w,20,h)
 band+=strip
# Small external base-perimeter bevel, not a mating edge.
c=param('central_binding_outer_chamfer',0.4)
for yy,sg in [(front,-1),(rear,1)]:
 cutter=extrude(Plane.YZ*Polygon((yy-sg*c,bottom),(yy+sg*2,bottom),(yy+sg*2,bottom+c+2),align=None),amount=w+2,both=True)
 band-=cutter
assert len(band.solids())==1
publish('central_binding',band,'连续圆弧贴面带')
w2=param('upper_binding_width',30.0);t2=param('upper_binding_thickness',1.0);seam=param('upper_binding_front_base',128.6);top=param('upper_binding_top_z',190.0);backbase=param('upper_binding_back_base',134.0);ey=param('upper_binding_front_y',-51.0);ry=param('upper_binding_rear_y',57.0)
h=top-seam;z=(top+seam)/2;cy=ey+sqrt(R*R-h*h/4)
strip=(Pos(0,cy,z)*Rot(0,90,0)*Cylinder(R,w2)-Pos(0,cy+t2,z)*Rot(0,90,0)*Cylinder(R,w2+2))&Pos(0,ey,z)*Box(w2,20,h)
strip+=Pos(0,(ey+ry)/2,top-t2/2)*Box(w2,ry-ey,t2)
strip+=Pos(0,ry-t2/2,(top+backbase)/2)*Box(w2,t2,top-backbase)
c2=param('upper_binding_outer_chamfer',0.4)
for yy,sg in [(ey,-1),(ry,1)]:
 cutter=extrude(Plane.YZ*Polygon((yy-sg*c2,top),(yy+sg*2,top),(yy+sg*2,top-c2-2),align=None),amount=w2+2,both=True)
 strip-=cutter
rise=param('upper_binding_crown_radius',3.0);peak=param('upper_binding_crown_y',10.0);start=param('upper_binding_transition_front_y',-40.0)
# Side profile: tangent Bezier forward fade into circular crown; solid decorative relief.
a=(0,start,top);b=(0,peak,top+rise);end=(0,peak+rise,top)
e1=Edge.make_bezier(a,(0,start+(peak-start)*0.45,top),(0,peak-(peak-start)*0.25,top+rise),b)
e2=Edge.make_three_point_arc(b,(0,peak+rise/sqrt(2),top+rise/sqrt(2)),end)
e3=Edge.make_line(end,(0,peak+rise,top-t2/2));e4=Edge.make_line((0,peak+rise,top-t2/2),(0,start,top-t2/2));e5=Edge.make_line((0,start,top-t2/2),a)
crown=Pos(-w2/2,0,0)*extrude(Face(Wire([e1,e2,e3,e4,e5])),amount=w2,dir=(1,0,0))
strip+=crown
assert len(strip.solids())==1
publish('upper_binding',strip,'圆弧隆起渐变顶带')