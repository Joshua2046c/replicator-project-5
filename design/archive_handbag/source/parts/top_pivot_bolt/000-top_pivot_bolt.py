x=param('top_pivot_bolt_x',-97.0);y=param('top_pivot_bolt_y',49.0);z=param('top_pivot_bolt_z',178.0)
b=asset('design/archive_handbag/source/assets/963db4249b8480e7fc5f042e49771d4560f24e8e0a68dca3f32182957d7d00ef.step')
publish('ring_bolt_left',Pos(x,y,z)*Rot(180,0,0)*b,'顶部M4转环螺栓')