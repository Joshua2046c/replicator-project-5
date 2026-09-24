# Deliberately custom cold-headed metal hinge pin; final assembled peened state.
dia=param('axle_diameter',4.0);length=param('axle_length',100.0);hd=param('axle_head_diameter',6.0);ht=param('axle_head_thickness',1.4)
shaft=Rot(0,90,0)*Cylinder(dia/2,length)
for s in [-1,1]:shaft+=Pos(s*(length/2+ht/2),0,0)*Rot(0,90,0)*Cylinder(hd/2,ht)
assert len(shaft.solids())==1
publish('axle',shaft,'双铆头金属轴')