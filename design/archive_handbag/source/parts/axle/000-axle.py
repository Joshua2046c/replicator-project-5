# Custom straight metal hinge pin, no integral heads. Caps are separate parts.
dia=param('axle_diameter',4.0)
length=param('axle_length',100.0)
lead=param('axle_end_chamfer',0.2)
shaft=Rot(0,90,0)*Cylinder(dia/2,length)
shaft=chamfer(shaft.edges().filter_by(GeomType.CIRCLE),lead)
assert shaft.is_valid and len(shaft.solids())==1
publish('axle',shaft,'独立直圆转轴',material='stainless_steel')
