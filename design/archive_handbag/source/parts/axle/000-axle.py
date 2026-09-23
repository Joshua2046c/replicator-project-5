dia=param('axle_diameter',4.0);length=param('axle_length',100.0)
shaft=Rot(0,90,0)*Cylinder(dia/2,length)
publish('axle',shaft,'不锈钢切长转轴')