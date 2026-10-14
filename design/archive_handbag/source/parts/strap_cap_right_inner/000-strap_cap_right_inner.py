# Independent adhesive socket cap: hole opens at local Z=0, closed top.
d=param('strap_cap_right_inner_diameter',12.0)
t=param('strap_cap_right_inner_thickness',3.0)
hole=param('strap_cap_right_inner_socket_diameter',4.4)
depth=param('strap_cap_right_inner_socket_depth',2.0)
r=param('strap_cap_right_inner_rim_radius',0.6)
lead=param('strap_cap_right_inner_socket_leadin',0.2)
shape=Cylinder(d/2,t,align=(Align.CENTER,Align.CENTER,Align.MIN))
shape=fillet(shape.edges().filter_by(GeomType.CIRCLE),r)
shape-=Cylinder(hole/2,depth,align=(Align.CENTER,Align.CENTER,Align.MIN))
shape-=Cone(hole/2+lead,hole/2,lead,align=(Align.CENTER,Align.CENTER,Align.MIN))
assert t-depth>=1.0 and shape.is_valid and len(shape.solids())==1
shape.color=srgb('#76787a')
publish('strap_cap_right_inner',shape,'右侧内插销帽',material='petg')
