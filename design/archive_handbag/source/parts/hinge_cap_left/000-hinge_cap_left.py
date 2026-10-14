d=param('hinge_cap_left_diameter',7.0)
t=param('hinge_cap_left_thickness',3.4)
socket=param('hinge_cap_left_socket_diameter',4.3)
depth=param('hinge_cap_left_socket_depth',2.0)
r=param('hinge_cap_left_rim_radius',0.3)
lead=param('hinge_cap_left_lead_in',0.15)
shape=Cylinder(d/2,t,align=(Align.CENTER,Align.CENTER,Align.MIN))
shape=fillet(shape.edges().filter_by(GeomType.CIRCLE),r)
shape-=Cylinder(socket/2,depth,align=(Align.CENTER,Align.CENTER,Align.MIN))
shape-=Cone(socket/2+lead,socket/2,lead,align=(Align.CENTER,Align.CENTER,Align.MIN))
assert t-depth>=1.2 and (d-socket)/2>=1.2
assert shape.is_valid and len(shape.solids())==1
shape.color=srgb('#76787a')
publish('hinge_cap_left',shape,'转轴左端插帽',material='petg')
