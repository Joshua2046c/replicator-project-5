from math import sqrt
R=param('spine_common_radius',88.33333333333333)
w=param('lower_binding_width',30.0);t=param('lower_binding_thickness',1.0)
front=param('lower_binding_front_y',-51.0);rear=param('lower_binding_rear_y',57.0);bottom=param('lower_binding_base_z',0.0);backtop=param('lower_binding_back_top',123.5)
cy=front+sqrt(R*R-32.0**2)
# Bottom horizontal return follows the same curved boundary, through the lowest4mm.
band=Pos(0,(front-8+rear)/2,bottom+t/2)*Box(w,rear-front+8,t)&Pos(0,cy,32)*Rot(0,90,0)*Cylinder(R,w)
band+=Pos(0,rear-t/2,backtop/2)*Box(w,t,backtop)
for z,h in [(32.0,64.0),(96.0,64.0)]:
 cy=front+sqrt(R*R-h*h/4)
 strip=(Pos(0,cy,z)*Rot(0,90,0)*Cylinder(R,w)-Pos(0,cy+t,z)*Rot(0,90,0)*Cylinder(R,w+2))&Pos(0,front,z)*Box(w,20,h)
 band+=strip
assert len(band.solids())==1
publish('central_binding',band,'连续圆弧贴面带')
w2=param('upper_binding_width',30.0);t2=param('upper_binding_thickness',1.0);seam=param('upper_binding_front_base',128.6);top=param('upper_binding_top_z',190.0);backbase=param('upper_binding_back_base',134.0);ey=param('upper_binding_front_y',-51.0);ry=param('upper_binding_rear_y',57.0)
h=top-seam;z=(top+seam)/2;cy=ey+sqrt(R*R-h*h/4)
strip=(Pos(0,cy,z)*Rot(0,90,0)*Cylinder(R,w2)-Pos(0,cy+t2,z)*Rot(0,90,0)*Cylinder(R,w2+2))&Pos(0,ey,z)*Box(w2,20,h)
strip+=Pos(0,(ey+ry)/2,top-t2/2)*Box(w2,ry-ey,t2)
strip+=Pos(0,ry-t2/2,(top+backbase)/2)*Box(w2,t2,top-backbase)
assert len(strip.solids())==1
publish('upper_binding',strip,'统一圆弧盖装饰带')