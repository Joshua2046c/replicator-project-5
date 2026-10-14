d=param('left_strap_pin_diameter',4.1)
length=param('left_strap_pin_length',12.3)
lead=param('left_strap_pin_chamfer',0.25)
shape=Cylinder(d/2,length,align=(Align.CENTER,Align.CENTER,Align.MIN))
shape=chamfer(shape.edges().filter_by(GeomType.CIRCLE),lead)
assert shape.is_valid and len(shape.solids())==1
shape.color=srgb('#76787a')
publish('strap_pin_left',shape,'左侧圆形插销',material='petg')
