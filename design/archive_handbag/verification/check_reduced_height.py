"""Verify152mm case height assembly, unchanged interfaces and discrete assembly motion."""
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path
from build123d import Axis, Box, Plane, Pos, Vertex, import_step, mirror

path, revision = sys.argv[1:3]
width = float(sys.argv[3]) if len(sys.argv) > 3 else 165.0
side_x = width / 2 - 2
label_x = 35 - width / 2
magnet_x = width / 2 - 38
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
    expect(name+' X span', p[name].bounding_box().size.X, width)
for name, x in [('side_left', -side_x), ('side_right', side_x), ('nameplate', label_x)]:
    expect(name+' X center', p[name].bounding_box().center().X, x)
expect('nameplate X span', p['nameplate'].bounding_box().size.X, 200/9)
expect('nameplate Y span', p['nameplate'].bounding_box().size.Y, 60)
expect('nameplate top', p['nameplate'].bounding_box().max.Z, 152)
expect('nameplate pocket minimum clearance', p['nameplate'].distance_to(p['lid']), .1)
expect('buckle width', p['buckle'].bounding_box().size.X, 55)
for name in ['central_binding', 'upper_binding']:
    expect(name+' width', p[name].bounding_box().size.X, 45)
for name in ['side_left', 'side_right']:
    expect(name+' front lap clearance', p[name].distance_to(p['blue_spine']), .3)
ref = mirror(p['side_right'], about=Plane.YZ)
expect('side mirror volume difference', vol(p['side_left']-ref)+vol(ref-p['side_left']), 0)
for stem in ['body_magnet', 'lid_magnet']:
    for side, x in [('left', -magnet_x), ('right', magnet_x)]:
        expect(stem+'_'+side+' X', p[stem+'_'+side].bounding_box().center().X, x)
for x in [-60, -30, 30, 60]:
    for y, mate in [(-49.5, 'blue_spine'), (54.5, 'body')]:
        probe = Pos(x, y, 7)*Box(3.8, 3.8, .2)
        expect(f'peg {x},{y} material', overlap(probe, p['bottom_panel']), 3.8*3.8*.2)
        expect(f'socket {x},{y} clearance', overlap(probe, p[mate]), 0)

expect('rear outside Y',p['body'].bounding_box().max.Y,66.8)
expect('side panel front Y',p['side_right'].bounding_box().min.Y,-49.7)
expect('side panel rear Y',p['side_right'].bounding_box().max.Y,52.5)
expect('side panel wall thickness',p['side_right'].bounding_box().size.X,4)
expect('axle center Y',p['axle'].bounding_box().center().Y,63)
expect('front spine min Y',p['blue_spine'].bounding_box().min.Y,-59.5)
expect('base rear face Y',p['bottom_panel'].bounding_box().max.Y,59.5)
expect('buckle tongue back contact',p['buckle'].distance_to(p['central_binding']),0)
for stem in ['body_magnet','lid_magnet']:
    for side in ['left','right']:
        expect(stem+'_'+side+' Y',p[stem+'_'+side].bounding_box().center().Y,-48.3)
# Sample concealed peg stem and corresponding void in spine/binding.
probe=Pos(0,-58.5,76.8)*Box(2.8,.2,2.8)
expect('hidden peg material',overlap(probe,p['buckle']),2.8*.2*2.8)
expect('hidden peg spine socket',overlap(probe,p['blue_spine']),0)
expect('hidden peg strap socket',overlap(probe,p['central_binding']),0)

expect('lid case top',p['lid'].bounding_box().max.Z,152)
expect('front lower two books top',p['blue_spine'].bounding_box().max.Z,102.4)
expect('side height',p['side_right'].bounding_box().size.Z,145.4)
expect('buckle height',p['buckle'].bounding_box().size.Z,35.2)
expect('top binding peak',p['upper_binding'].bounding_box().max.Z,157)
expect('nameplate thickness',p['nameplate'].bounding_box().size.Z,.9)
for stem in ['body_magnet','lid_magnet']:
 for side in ['left','right']:
  expect(stem+'_'+side+' thickness',p[stem+'_'+side].bounding_box().size.Z,3)
for name in ['green_marks','blue_marks','pink_marks']:
 expect(name+' height',p[name].bounding_box().size.Z,20)
for side in ['left','right']:
 expect('eye_'+side+' height',p['eye_'+side].bounding_box().size.Z,44)
 expect('thumb_screw_'+side+' axis Z',p['thumb_screw_'+side].bounding_box().center().Z,136)

for axis_index,(label,value) in enumerate([('overall X',203),('overall Y',131.3),('overall Z with rings',172)]):
 expect(label,list(assembly.bounding_box().size)[axis_index],value)

moving = ['lid','upper_binding','pink_marks','nameplate','lid_magnet_left','lid_magnet_right']
axis = Axis((0,63,102.4),(1,0,0))
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

r = dict(revision=revision, requested_body_length_mm=width, nominal_depth_mm=125, nominal_height_mm=152, height_reduction_fraction=.2, step_sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),
         all_valid=all(s.is_valid for s in p.values()), objects=len(p), solids=len(assembly.solids()),
         pairs_screened=len(p)*(len(p)-1)//2, closed_collisions=closed, dimensions=dimensions,
         opening_angles_deg=list(range(0,101,5)), opening_collisions=opening,
         extraction_collisions=extraction, assembled_envelope_mm=list(assembly.bounding_box().size),
         scope='Exact B-rep closed pose and discrete motion; no continuous sweep or physical load certification.')
r['passed'] = r['all_valid'] and not closed and not opening and not extraction and all(q['passed'] for q in dimensions)
Path('design/archive_handbag/verification/reduced-height-check.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2),flush=True)
assert r['passed']
