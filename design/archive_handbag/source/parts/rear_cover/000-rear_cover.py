w=param('rear_cover_width',216.0);h=param('rear_cover_height',121.0);t=param('rear_cover_thickness',3.0);r=param('rear_cover_corner_radius',3.0)
cover=extrude(RectangleRounded(w,h,r),amount=t)
cover.color=Color(0.12,0.10,0.09);publish('rear_cover',cover,'背部装饰封面')