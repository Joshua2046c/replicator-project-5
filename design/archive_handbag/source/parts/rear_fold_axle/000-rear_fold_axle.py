dia=param('pin_diameter',3.0);length=param('length',169.6);lead=param('end_chamfer',0.2)
shaft=Rot(0,90,0)*Cylinder(dia/2,length)
shaft=chamfer(shaft.edges().filter_by(GeomType.CIRCLE),lead)
publish('rear_fold_axle',shaft,'后折叠独立圆销',material='stainless_steel')