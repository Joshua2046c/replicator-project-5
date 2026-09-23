# Flexible belt closed-position envelope, with releasable overlap hidden by decorative frame.
w=param('lower_binding_width',30.0);t=param('lower_binding_thickness',1.0)
d=param('binding_loop_depth',116.0);h=param('binding_loop_height',190.0);r=param('binding_corner_radius',2.0);cy=param('binding_center_y',0.0)
seam=param('binding_release_z',100.0);slit=param('binding_release_gap',0.3)
# Outer rounding only: square inside clears roof/floor corners; a fabric bend is not solid penetration.
profile=RectangleRounded(d,h,r)-Rectangle(d-2*t,h-2*t)
band=Pos(-w/2,cy,h/2)*extrude(Plane.YZ*profile,amount=w)
band-=Pos(0,cy-d/2+t/2,seam)*Box(w+1,t+0.2,slit)
publish('central_binding',band,'可拆棕色环绕带')
pw=param('binding_overlap_width',28.0);ph=param('binding_overlap_height',28.0);pt=param('binding_overlap_thickness',0.6)
patch=Pos(0,cy-d/2-pt/2,seam)*Box(pw,pt,ph)
publish('binding_overlap',patch,'隐藏搭接魔术贴包络')