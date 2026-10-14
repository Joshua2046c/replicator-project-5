"""Read-only checks against the exported STEP; no CAD authority is changed."""
import hashlib
import json
import sys
from pathlib import Path
from build123d import Axis, Plane, Pos, mirror, import_step

path, revision = sys.argv[1:3]
step_hash = hashlib.sha256(Path(path).read_bytes()).hexdigest()
assembly = import_step(path)
p = {s.label: s.clean() for s in assembly.children}
new = [k for k in p if k.startswith('strap_')]
checks, collisions = [], []
def vol(s):
    if not s: return 0.0
    return abs(s.volume) if hasattr(s, 'volume') else sum(abs(x.volume) for x in s)
def overlap(a,b):
    aa,bb=a.bounding_box(),b.bounding_box()
    if not all(tuple(aa.max)[i]>tuple(bb.min)[i]+1e-7 and tuple(bb.max)[i]>tuple(aa.min)[i]+1e-7 for i in range(3)): return 0.0
    return vol(a & b)
def expect(name,actual,expected,tol=1e-5):
    checks.append(dict(name=name,actual=actual,expected=expected,passed=abs(actual-expected)<=tol))
def collision(mode,angle,a,b,sa,sb):
    v=overlap(sa,sb)
    if v>1e-5: collisions.append(dict(mode=mode,step=angle,a=a,b=b,volume_mm3=v))
expect('new separate objects',len(new),8)
expect('all assembly objects',len(p),22)
for k in new:
    expect(k+' valid single solid',int(p[k].is_valid and len(p[k].solids())==1),1)
for axis,expected in enumerate([200,131.3,171]):
    expect('assembly extent '+str(axis),tuple(assembly.bounding_box().size)[axis],expected)
for side in ['left','right']:
    eye=p['strap_eye_'+side];pin=p['strap_pin_'+side];panel=p['side_'+side]
    expect(side+' eye width',eye.bounding_box().size.Y,36)
    expect(side+' eye height',eye.bounding_box().size.Z,44)
    expect(side+' eye thickness',eye.bounding_box().size.X,4)
    expect(side+' pin length',pin.bounding_box().size.X,12.3)
    expect(side+' pin diameter',pin.bounding_box().size.Y,4.1)
    expect(side+' pin to panel radial gap',pin.distance_to(panel),.2)
    expect(side+' pin to eye radial gap',pin.distance_to(eye),.2)
    for which,mate in [('inner',panel),('outer',eye)]:
        cap=p[f'strap_cap_{side}_{which}']
        expect(side+' '+which+' cap contact gap',cap.distance_to(mate),.2)
        expect(side+' '+which+' radial glue gap',cap.distance_to(pin),.15)
        expect(side+' '+which+' cap thickness',cap.bounding_box().size.X,3)
    expect(side+' eye panel stand off',eye.distance_to(panel),.3)
for right in [k for k in new if 'right' in k]:
    left=right.replace('right','left');ref=mirror(p[right],about=Plane.YZ)
    expect(right+' exact mirrored counterpart',vol(ref-p[left])+vol(p[left]-ref),0)
print('dimensional checks',len(checks),'failures',[x for x in checks if not x['passed']],flush=True)
moving=['lid','upper_binding','pink_marks','nameplate']
axis=Axis((0,63,102.4),(1,0,0))
for angle in range(0,101,5):
    for name in moving:
        s=p[name].rotate(axis,-angle)
        for fixed in new:collision('lid opening',angle,name,fixed,s,p[fixed])
print('lid opening checked; collisions',collisions,flush=True)
for side,x in [('right',90.5),('left',-90.5)]:
    name='strap_eye_'+side
    for angle in range(0,360,15):
        s=p[name].rotate(Axis((x,0,136),(1,0,0)),angle)
        for fixed in p:
            # Coaxial pin and circular caps are rotationally invariant. Their
            # positive closed-state clearances above prove them at every angle.
            if fixed!=name and not fixed.startswith(('strap_pin_','strap_cap_')):
                collision('eye rotation',angle,name,fixed,s,p[fixed])
    pin='strap_pin_'+side;sgn=1 if side=='right' else -1
    for offset in range(0,17,2):
        s=Pos(sgn*offset,0,0)*p[pin]
        for fixed in p:
            if fixed==pin or fixed.startswith('strap_cap_'):continue
            collision('pin insertion without caps',offset,pin,fixed,s,p[fixed])
print('rotation and insertion checked; collisions',collisions,flush=True)
result=dict(revision=revision,step_sha256=step_hash,checks=checks,collisions=collisions,
            limitation='Discrete geometry checks only: lid 5 degree steps, ring 15 degree steps. No physical adhesive, load or fatigue test. Existing side/bottom pullout limitation remains.')
dest=Path(__file__).with_name('strap-pin-joint-check.json')
dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
failed=[x for x in checks if not x['passed']]
print(json.dumps({'checks':len(checks),'failed':failed,'collisions':collisions},ensure_ascii=False),flush=True)
assert not failed and not collisions
