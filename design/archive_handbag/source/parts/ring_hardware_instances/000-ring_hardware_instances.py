# Exact bound STEP instances; fit metadata is recorded in connections.json because
# runtime requires budget_mm but host rejects that returned field. Not fused geometry.
for side,s in [('left',-1),('right',1)]:
 for level,z in [('low',90.0),('high',110.0)]:
  if side=='right' and level=='low': continue
  oid='ring_bolt_'+side+'_'+level
  xx=param(oid+'_x',s*113.0);yy=param(oid+'_y',46.5);zz=param(oid+'_z',z)
  bolt=asset('design/archive_handbag/source/assets/963db4249b8480e7fc5f042e49771d4560f24e8e0a68dca3f32182957d7d00ef.step')
  publish(oid,Pos(xx,yy,zz)*Rot(0,s*90,0)*bolt,'M4×20 连接环螺栓')
  nid='ring_nut_'+side+'_'+level
  nx=param(nid+'_x',s*98.0);ny=param(nid+'_y',46.5);nz=param(nid+'_z',z)
  nut=asset('design/archive_handbag/source/assets/fc200b5ae3935c689379a698c83428aa651f5d3a401e1ddc2dc04ff80c965c27.step')
  publish(nid,Pos(nx,ny,nz)*Rot(0,-s*90,0)*nut,'M4 六角螺母')
assert all(name in ['left','right'] for name in ['left','right'])