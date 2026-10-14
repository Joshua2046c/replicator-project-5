"""Read-only verification of independent hinge shaft/caps from committed export."""
import hashlib,json,sys
from pathlib import Path
from build123d import Axis,Box,Cylinder,Plane,Pos,Rot,import_step,mirror
path,revision=sys.argv[1:3]
sha=hashlib.sha256(Path(path).read_bytes()).hexdigest()
assembly=import_step(path)
p={s.label:s.clean() for s in assembly.children}
checks=[];collisions=[]
def volume(s):
 if not s:return 0.0
 return abs(s.volume) if hasattr(s,'volume') else sum(abs(x.volume) for x in s)
def expect(n,a,b,tol=1e-5):checks.append(dict(name=n,actual=a,expected=b,passed=abs(a-b)<=tol))
def overlap(a,b):
 aa,bb=a.bounding_box(),b.bounding_box()
 if not all(tuple(aa.max)[i]>tuple(bb.min)[i]+1e-7 and tuple(bb.max)[i]>tuple(aa.min)[i]+1e-7 for i in range(3)):return 0.0
 return volume(a&b)
expect('assembly object count',len(p),24)
expect('shaft length',p['axle'].bounding_box().size.X,103.6)
expect('shaft diameter',p['axle'].bounding_box().size.Y,4)
axis=Axis((0,63,102.4),(1,0,0))
for name in ['axle','hinge_cap_left','hinge_cap_right']:
 shape=p[name]
 expect(name+' single valid solid',int(shape.is_valid and len(shape.solids())==1),1)
 expect(name+' common axis Y',shape.bounding_box().center().Y,63)
 expect(name+' common axis Z',shape.bounding_box().center().Z,102.4)
 # Exact source consists only of coaxial circles, cones and circular fillets.
 # Test an arbitrary rotation as a regression check of rotational invariance.
 turned=shape.rotate(axis,37)
 expect(name+' rotational invariance',volume(shape-turned)+volume(turned-shape),0)
for side,sgn in [('left',-1),('right',1)]:
 cap=p['hinge_cap_'+side]
 expect(side+' cap diameter',cap.bounding_box().size.Y,6.8)
 expect(side+' cap thickness',cap.bounding_box().size.X,3.4)
 expect(side+' radial adhesive gap',cap.distance_to(p['axle']),.15)
 # Probe the closed floor and the blind cavity rather than only its bbox.
 floor=Pos(sgn*52.7,63,102.4)*Box(.2,1,1)
 cavity=Pos(sgn*51,63,102.4)*Box(.2,1,1)
 expect(side+' closed cap floor',overlap(cap,floor),.2)
 expect(side+' blind socket empty',overlap(cap,cavity),0)
 expect(side+' cap to rear panel clearance',cap.distance_to(p['body']),.1)
 expect(side+' axial endplay',sgn*(cap.bounding_box().min.X if sgn>0 else cap.bounding_box().max.X)-49,1)
ref=mirror(p['hinge_cap_right'],about=Plane.YZ)
expect('left right cap mirror',volume(ref-p['hinge_cap_left'])+volume(p['hinge_cap_left']-ref),0)
print('dimensions',len(checks),'failed',[c for c in checks if not c['passed']],flush=True)
# The complete straight pin insertion sweep, not discrete insertion positions.
# Shaft is inserted from the right by 103.6mm, then both caps are fitted.
sweep=Pos(51.8,63,102.4)*Rot(0,90,0)*Cylinder(2,207.2)
for name,shape in p.items():
 if name in ['axle','hinge_cap_left','hinge_cap_right']:continue
 v=overlap(sweep,shape)
 if v>1e-5:collisions.append(dict(mode='continuous bare pin insertion',object=name,volume_mm3=v))
print('insertion sweep',collisions,flush=True)
# With a common axis, the invariant shaft and caps have the same clearance to
# a rigidly rotating lid at every angle. Check the closed clearance and a 100deg endpoint.
for name in ['axle','hinge_cap_left','hinge_cap_right']:
 for angle in [0,100]:
  v=overlap(p[name],p['lid'].rotate(axis,-angle))
  if v>1e-5:collisions.append(dict(mode='lid rotation',part=name,angle=angle,volume_mm3=v))
result=dict(revision=revision,step_sha256=sha,checks=checks,collisions=collisions,
 motion_method='Continuous cylindrical shaft insertion envelope; axisymmetric shaft/caps and coaxial lid imply angle-invariant clearance, checked additionally at 0 and 100 degrees.',
 limitation='Geometry only. Adhesive compatibility and retention strength require physical testing.')
Path(__file__).with_name('hinge-cap-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
failed=[c for c in checks if not c['passed']]
print(json.dumps(dict(checks=len(checks),failed=failed,collisions=collisions)),flush=True)
assert not failed and not collisions
