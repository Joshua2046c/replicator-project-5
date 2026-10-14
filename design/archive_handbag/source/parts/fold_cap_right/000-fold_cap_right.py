d=param('cap_diameter',5.8);t=param('thickness',3.4);socket=param('cap_socket_diameter',3.3);depth=param('socket_depth',2.0);r=param('rim_radius',0.3);lead=param('lead_in',0.15)
shape=Cylinder(d/2,t,align=(Align.CENTER,Align.CENTER,Align.MIN))
shape=fillet(shape.edges().filter_by(GeomType.CIRCLE),r)
shape-=Cylinder(socket/2,depth,align=(Align.CENTER,Align.CENTER,Align.MIN))
shape-=Cone(socket/2+lead,socket/2,lead,align=(Align.CENTER,Align.CENTER,Align.MIN))
assert shape.is_valid and len(shape.solids())==1
publish('fold_cap_right',shape,'内折叠铰链右插帽',material='petg')