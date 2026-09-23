x=param('pivot_bolt_left_x',-128.0);y=param('pivot_bolt_left_y',49.0);z=param('pivot_bolt_left_z',188.0)
b=asset('design/archive_handbag/source/assets/c857efadcb1f1edee90de544b54b5f97185fd727b9ce5ca786b264b3f2d027e0.step')
publish('pivot_bolt_left',Pos(x,y,z)*Rot(180,0,0)*b,'左转环M4螺栓')