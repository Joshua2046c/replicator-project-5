# Exact second instance of the already bound ISO4032 M4-0.7 catalog STEP; no generated nut geometry.
x=param('ring_nut_right_x',100.0);y=param('ring_nut_right_y',0.0);z=param('ring_nut_right_z',174.0)
publish('ring_nut_right',Pos(x,y,z)*Rot(0,-90,0)*asset('design/archive_handbag/source/assets/fc200b5ae3935c689379a698c83428aa651f5d3a401e1ddc2dc04ff80c965c27.step'),'盖下内侧M4螺母')