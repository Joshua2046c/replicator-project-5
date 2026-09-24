# 贴面嵌槽装饰，开口及铰轴处物理断开；不是束紧包的带材。
w=param('lower_binding_width',30.0);t=param('lower_binding_thickness',1.0)
front=param('lower_binding_front_y',-51.0);rear=param('lower_binding_rear_y',57.0);bottom=param('lower_binding_base_z',0.0);backtop=param('lower_binding_back_top',123.5)
# Matching front interface from the two book profiles.
band=Pos(0,(front+rear)/2,bottom+t/2)*Box(w,rear-front,t)
band+=Pos(0,front+t/2,2)*Box(w,t,4)
band+=Pos(0,rear-t/2,backtop/2)*Box(w,t,backtop)
for z,h in [(34.0,60.0),(96.0,64.0)]:
 sag=6.0;R=(h*h/4+sag*sag)/(2*sag);cy=front+R-sag
 strip=(Pos(0,cy,z)*Rot(0,90,0)*Cylinder(R,w)-Pos(0,cy+t,z)*Rot(0,90,0)*Cylinder(R,w+2))&Pos(0,front, z)*Box(w,20,h)
 band+=strip
assert len(band.solids())==1
publish('central_binding',band,'下半贴面装饰带')
w2=param('upper_binding_width',30.0);t2=param('upper_binding_thickness',1.0);seam=param('upper_binding_front_base',128.6);top=param('upper_binding_top_z',189.0);backbase=param('upper_binding_back_base',134.0);ey=param('upper_binding_front_y',-51.0);ry=param('upper_binding_rear_y',57.0);sag=param('upper_binding_spine_sag',6.0)
h=top-seam;z=(top+seam)/2;R=(h*h/4+sag*sag)/(2*sag);cy=ey+R-sag
strip=(Pos(0,cy,z)*Rot(0,90,0)*Cylinder(R,w2)-Pos(0,cy+t2,z)*Rot(0,90,0)*Cylinder(R,w2+2))&Pos(0,ey,z)*Box(w2,20,h)
strip+=Pos(0,(ey+ry)/2,top-t2/2)*Box(w2,ry-ey,t2)
strip+=Pos(0,ry-t2/2,(top+backbase)/2)*Box(w2,t2,top-backbase)
assert len(strip.solids())==1
publish('upper_binding',strip,'随盖贴面装饰带')