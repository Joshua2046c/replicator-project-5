# Exact second instances of the catalog ISO10642 M3x10 and ISO4032 M3 assets; no synthetic screw or nut.
x=param('side_lock_right_head_x',109.75);y=param('side_lock_right_axis_y',-46.5);z=param('side_lock_right_axis_z',100.0)
nx=param('side_lock_nut_right_face_x',103.0)
publish('side_lock_right',Pos(x,y,z)*Rot(0,90,0)*asset('design/archive_handbag/source/assets/9fa7931862d1cd1789a68ae9e629a221bfbab099d1d208e2085e86618fd52d30.step'),'右侧板防拔螺钉')
publish('side_lock_nut_right',Pos(nx,y,z)*Rot(0,-90,0)*asset('design/archive_handbag/source/assets/810e7ff4380f9546cacf2df5d8900504c6a5340aa1d46cbc3f54e5bc349d0795.step'),'右侧板防拔螺母')