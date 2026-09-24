from math import sqrt
w=param('bottom_panel_width',220.0);d=param('bottom_panel_depth',114.0);t=param('bottom_panel_thickness',4.0);channel=param('bottom_panel_band_width',30.0);recess=param('bottom_panel_band_recess',1.0)
xs=param('bottom_panel_joint_half_span',80.0);ix=param('bottom_panel_joint_inner_x',40.0)
fy=param('bottom_panel_peg_front_y',-47.0);ry=param('bottom_panel_peg_rear_y',52.0);ps=param('bottom_panel_peg_width',4.0);ph=param('bottom_panel_peg_height',6.0);lead=param('bottom_panel_peg_leadin',0.4)
front=param('bottom_panel_front_edge_y',-51.0);R=param('spine_common_radius',88.33333333333333);hh=param('bottom_panel_spine_height',64.0);cz=param('bottom_panel_spine_center_z',32.0)
c=param('bottom_panel_outer_chamfer',0.4)
cy=front+sqrt(R*R-hh*hh/4)
outer=Pos(0,cy,cz)*Rot(0,90,0)*Cylinder(R,w)
p=Pos(0,(front-8+d/2)/2,t/2)*Box(w,d/2-front+8,t)&outer
# Four bottom perimeter regions, including the curved front boundary.
for xx,sg in [(-w/2,-1),(w/2,1)]:
 p-=extrude(Plane.XZ*Polygon((xx-sg*c,0),(xx+sg*2,0),(xx+sg*2,c+2),align=None),amount=d+20,both=True)
for yy,sg in [(front,-1),(d/2,1)]:
 p-=extrude(Plane.YZ*Polygon((yy-sg*c,0),(yy+sg*2,0),(yy+sg*2,c+2),align=None),amount=w+2,both=True)
# End treatment continues the two front vertical arcs and two rear corners.
taper=Pos(0,cy,cz)*Rot(0,90,0)*Cylinder(R,w-2*c)
taper+=Pos(-w/2+c/2,cy,cz)*Rot(0,90,0)*Cone(R-c,R,c)
taper+=Pos(w/2-c/2,cy,cz)*Rot(0,90,0)*Cone(R,R-c,c)
p-=outer-taper
# Continue R3 down to the base, with the existing bottom perimeter bevel.
cr=param('bottom_panel_rear_corner_radius',3.0)
assert cr>c
for sg in [-1,1]:
 xc=sg*(w/2-cr);yc=d/2-cr
 square=Pos(sg*(w/2-cr/2),d/2-cr/2,-1)*Box(cr,cr,t+2,align=(Align.CENTER,Align.CENTER,Align.MIN))
 disk=Pos(xc,yc,-1)*Cylinder(cr,t+2,align=(Align.CENTER,Align.CENTER,Align.MIN))
 p-=square-disk
 bottom_corner=Pos(sg*(w/2-cr/2),d/2-cr/2,0)*Box(cr,cr,c,align=(Align.CENTER,Align.CENTER,Align.MIN))
 cone=Pos(xc,yc,0)*Cone(cr-c,cr,c,align=(Align.CENTER,Align.CENTER,Align.MIN))
 p-=bottom_corner-cone
p-=Pos(0,0,recess/2)*Box(channel,d+20,recess)
band=(outer-Pos(0,cy+recess,cz)*Rot(0,90,0)*Cylinder(R,w+2))&Pos(0,front,t/2)*Box(channel,20,t)
p-=band
p-=Pos(0,d/2-recess/2,t/2)*Box(channel,recess,t)
for y in [fy,ry]:
 for x in [-xs,-ix,ix,xs]:
  peg=Pos(x,y,t+ph/2)*Box(ps,ps,ph)
  peg=chamfer(peg.edges().group_by(Axis.Z)[-1],length=lead)
  p+=peg
assert len(p.solids())==1
publish('bottom_panel',p,'外边小倒角方桩底板')