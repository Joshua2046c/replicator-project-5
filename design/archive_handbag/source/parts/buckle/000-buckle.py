w=param('buckle_width',42.0);h=param('buckle_height',44.0);t=param('buckle_thickness',1.0);rim=param('buckle_rim',5.0);r=param('buckle_corner_radius',5.0)
shape=extrude(RectangleRounded(w,h,r)-RectangleRounded(w-2*rim,h-2*rim,3),amount=t)
shape.color=Color(0.68,0.68,0.70);publish('buckle',shape,'方形装饰扣')