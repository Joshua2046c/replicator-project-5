"""Check 165mm case, mating locations, lid motion and side extraction on exported STEP."""
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path
from build123d import Axis, Box, Plane, Pos, Vertex, import_step, mirror

path, revision = sys.argv[1:]
assembly = import_step(path)
p = {s.label: s.clean() for s in assembly.children}

def vol(s):
    if not s:
        return 0.0
    return abs(s.volume) if hasattr(s, 'volume') else sum(abs(x.volume) for x in s)

def overlap(a, b):
    aa, bb = a.bounding_box(), b.bounding_box()
    if not all(tuple(aa.max)[i] > tuple(bb.min)[i]+1e-7 and
               tuple(bb.max)[i] > tuple(aa.min)[i]+1e-7 for i in range(3)):
        return 0.0
    return vol(a & b)

closed = []
for a, b in combinations(p, 2):
    v = overlap(p[a], p[b])
    if v > 1e-5:
        closed.append(dict(a=a, b=b, volume_mm3=v))
print('closed collisions', closed, flush=True)

dimensions = []
def expect(label, actual, expected, tolerance=1e-5):
    dimensions.append(dict(label=label, actual=actual, expected=expected,
                           passed=abs(actual-expected) <= tolerance))

for name in ['body', 'lid', 'blue_spine', 'bottom_panel']:
    expect(name+' X span', p[name].bounding_box().size.X, 165)
for name, x in [('side_left', -80.5), ('side_right', 80.5), ('nameplate', -47.5)]:
    expect(name+' X center', p[name].bounding_box().center().X, x)
expect('nameplate X span', p['nameplate'].bounding_box().size.X, 200/9)
expect('nameplate Y span', p['nameplate'].bounding_box().size.Y, 60)
expect('nameplate top', p['nameplate'].bounding_box().max.Z, 190)
expect('nameplate pocket minimum clearance', p['nameplate'].distance_to(p['lid']), .1)
expect('buckle width', p['buckle'].bounding_box().size.X, 55)
for name in ['central_binding', 'upper_binding']:
    expect(name+' width', p[name].bounding_box().size.X, 45)
for name in ['side_left', 'side_right']:
    expect(name+' front lap clearance', p[name].distance_to(p['blue_spine']), .3)
ref = mirror(p['side_right'], about=Plane.YZ)
expect('side mirror volume difference', vol(p['side_left']-ref)+vol(ref-p['side_left']), 0)
for stem in ['body_magnet', 'lid_magnet']:
    for side, x in [('left', -44.5), ('right', 44.5)]:
        expect(stem+'_'+side+' X', p[stem+'_'+side].bounding_box().center().X, x)
for x in [-60, -30, 30, 60]:
    for y, mate in [(-47, 'blue_spine'), (52, 'body')]:
        probe = Pos(x, y, 7)*Box(3.8, 3.8, .2)
        expect(f'peg {x},{y} material', overlap(probe, p['bottom_panel']), 3.8*3.8*.2)
        expect(f'socket {x},{y} clearance', overlap(probe, p[mate]), 0)

moving = ['lid','upper_binding','pink_marks','nameplate','lid_magnet_left','lid_magnet_right']
axis = Axis((0,60.5,128),(1,0,0))
opening = []
for deg in range(0,101,5):
    for name in moving:
        a = p[name].rotate(axis, -deg)
        for fixed in [n for n in p if n not in moving]:
            v = overlap(a, p[fixed])
            if v > 1e-5:
                opening.append(dict(angle_deg=deg, moving=name, fixed=fixed, volume_mm3=v))
    print('opening', deg, 'collisions', len(opening), flush=True)

removed = ('thumb_screw_', 'eye_', 'pivot_', 'ring_nut_', 'backplate_')
opened = {n:(s.rotate(axis,-100) if n in moving else s) for n,s in p.items()
          if not n.startswith(removed)}
extraction = []
for name in ['side_left','side_right']:
    for dz in [0,.4,1,5,20,50,100,125,150,185,200]:
        a = Pos(0,0,dz)*p[name]
        for fixed,s in opened.items():
            if fixed == name:
                continue
            v = overlap(a,s)
            if v > 1e-5:
                extraction.append(dict(panel=name, lift_mm=dz, fixed=fixed, volume_mm3=v))

r = dict(revision=revision, step_sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),
         all_valid=all(s.is_valid for s in p.values()), objects=len(p), solids=len(assembly.solids()),
         pairs_screened=len(p)*(len(p)-1)//2, closed_collisions=closed, dimensions=dimensions,
         opening_angles_deg=list(range(0,101,5)), opening_collisions=opening,
         extraction_collisions=extraction, assembled_envelope_mm=list(assembly.bounding_box().size),
         scope='Exact B-rep closed pose and discrete motion; no continuous sweep or physical load certification.')
r['passed'] = r['all_valid'] and not closed and not opening and not extraction and all(q['passed'] for q in dimensions)
Path('design/archive_handbag/verification/shortened-case-check.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2),flush=True)
assert r['passed']
