"""Read-only dimensional and sampled kinematic checks on exported STEP."""
import hashlib, json, sys
from pathlib import Path
from build123d import Axis, Box, Cylinder, Pos, Rot, import_step
path, revision = sys.argv[1:3]
sha = hashlib.sha256(Path(path).read_bytes()).hexdigest()
p = {s.label: s.clean() for s in import_step(path).children}
# Detach the STEP hierarchy so rotations copy only the part, not the assembly.
for shape in p.values(): shape.parent=None
checks, collisions = [], []
def volume(s):
    if not s: return 0.0
    return abs(s.volume) if hasattr(s, 'volume') else sum(abs(x.volume) for x in s)
bbox_cache={}
def cached_bbox(s):
    key=id(s)
    if key not in bbox_cache: bbox_cache[key]=(s,s.bounding_box())
    return bbox_cache[key][1]
def overlap(a,b):
    aa,bb=cached_bbox(a),cached_bbox(b)
    if not all(tuple(aa.max)[i]>tuple(bb.min)[i]+1e-7 and tuple(bb.max)[i]>tuple(aa.min)[i]+1e-7 for i in range(3)): return 0.0
    return volume(a & b)
def expect(name,actual,expected,tol=1e-5):
    checks.append(dict(name=name,actual=actual,expected=expected,passed=abs(actual-expected)<=tol))
rear=Axis((0,63,102.4),(1,0,0)); front=Axis((0,-49.85,149.0),(1,0,0))
roof_names=['lid','upper_binding','nameplate','fold_axle','fold_cap_left','fold_cap_right','rear_fold_axle','rear_fold_cap_left','rear_fold_cap_right']
rear_names=['rear_fold_cover','rear_fold_binding']
upper_rear=Axis((0,53.35,149),(1,0,0))
front_names=['fold_spine','fold_binding','pink_marks']
fixed={n:s for n,s in p.items() if n not in roof_names+front_names+rear_names}
base_shape_ids={id(s) for s in p.values()}
expect('fold pin length',p['fold_axle'].bounding_box().size.X,169.6)
expect('fold pin diameter',p['fold_axle'].bounding_box().size.Y,3)
for n in ['lid','fold_spine','fold_axle','fold_cap_left','fold_cap_right']:
    expect(n+' single valid solid',int(p[n].is_valid and len(p[n].solids())==1),1)
for n in ['side_left','side_right']:
    b=p[n].bounding_box()
    expect(n+' square front Y',b.min.Y,-49.7)
    expect(n+' full height',b.max.Z,149.4)
    probe=Pos(b.center().X,-48,145)*Box(2,2,2)
    expect(n+' restored upper front corner',overlap(probe,p[n]),8)
for n in ['fold_cap_left','fold_cap_right']:
    expect(n+' cap diameter',p[n].bounding_box().size.Y,5.8)
    expect(n+' cap thickness',p[n].bounding_box().size.X,3.4)
    expect(n+' radial glue gap',p[n].distance_to(p['fold_axle']),.15)
    sign=-1 if n.endswith('left') else 1
    expect(n+' blind floor',overlap(p[n],Pos(sign*85.7,-49.85,149.0)*Box(.2,1,1)),.2)
    expect(n+' socket clear',overlap(p[n],Pos(sign*84,-49.85,149.0)*Box(.2,1,1)),0)
expect('binding split gap at least 0.3',int(p['fold_binding'].distance_to(p['upper_binding'])>=.3-1e-5),1)
for n in ['rear_fold_cover','rear_fold_axle','rear_fold_cap_left','rear_fold_cap_right']:
    expect(n+' single solid',int(p[n].is_valid and len(p[n].solids())==1),1)
expect('equal front and rear upper pin lengths',p['rear_fold_axle'].bounding_box().size.X,p['fold_axle'].bounding_box().size.X)
print('dimensions',len(checks),'failed',[c for c in checks if not c['passed']],flush=True)
closed_pairs=0
items=list(p.items())
for i,(n,a) in enumerate(items):
    for q,b in items[i+1:]:
        v=overlap(a,b);closed_pairs+=1
        if v>1e-5:collisions.append(dict(mode='closed assembly',a=n,b=q,volume_mm3=v))
print('closed pairs',closed_pairs,'collisions',collisions,flush=True)
# Assemble front joint before fitting the lid to the body: side panels would
# obstruct the axial insertion path in the fully closed assembled case.
sweep=Pos(84.8,-49.85,149.0)*Rot(0,90,0)*Cylinder(1.5,339.2)
for n in ['lid','fold_spine','fold_binding','upper_binding','pink_marks','nameplate']:
    v=overlap(sweep,p[n])
    if v>1e-5: collisions.append(dict(mode='continuous pin insertion in detached lid',object=n,volume_mm3=v))
# Rear pin insertion through the detached roof/back subassembly.
rear_sweep=Pos(84.8,53.35,149)*Rot(0,90,0)*Cylinder(1.5,339.2)
for n in ['lid','rear_fold_cover','upper_binding','rear_fold_binding','nameplate']:
    v=overlap(rear_sweep,p[n])
    expect('rear continuous shaft insertion '+n,v,0)
samples=0
def pose_check(stage,fold_angle,rear_angle,upper_angle=0):
    global samples
    moving={n:p[n].rotate(upper_rear,upper_angle).rotate(rear,-rear_angle) for n in roof_names}
    moving.update({n:p[n].rotate(front,-fold_angle).rotate(upper_rear,upper_angle).rotate(rear,-rear_angle) for n in front_names})
    moving.update({n:p[n].rotate(rear,-rear_angle) for n in rear_names})
    for n,s in moving.items():
        for q,t in fixed.items():
            v=overlap(s,t)
            if v>1e-5:collisions.append(dict(stage=stage,fold=fold_angle,rear=rear_angle,a=n,b=q,volume_mm3=v))
    if True:
        for n in front_names:
            for q in roof_names+rear_names:
                v=overlap(moving[n],moving[q])
                if v>1e-5:collisions.append(dict(stage=stage,fold=fold_angle,rear=rear_angle,a=n,b=q,volume_mm3=v))
    for n in roof_names:
        for q in rear_names:
            v=overlap(moving[n],moving[q])
            if v>1e-5: collisions.append(dict(stage=stage,upper=upper_angle,a=n,b=q,volume_mm3=v))
    samples+=1
    for key in list(bbox_cache):
        if key not in base_shape_ids: del bbox_cache[key]
    print(stage,fold_angle,rear_angle,upper_angle,'collisions',len(collisions),flush=True)
    if collisions:
        print(json.dumps(collisions),flush=True)
        raise RuntimeError('Motion collision; repair before further sampling')
for a in list(range(0,31,5)): pose_check('initial outward release',a,0)
for a in range(5,36,5): pose_check('lift lid clear of sides',30,a)
for a in [25,20,15,10,5,0]+list(range(-5,-81,-5)): pose_check('fold spine under lifted roof',a,35)
for a in range(40,101,5): pose_check('open folded lid',-80,a)
for a in range(105,161,5): pose_check('lift rear behind case',-80,a)
for a in range(5,81,5): pose_check('fold rear cover joint',-80,160,a)
result=dict(revision=revision,step_sha256=sha,checks=checks,collisions=collisions,
    poses_checked=samples,closed_pairs=closed_pairs,opening_sequence='Outward release30deg, rear lift35deg, front fold inward80deg, lower rear open160deg, upper rear fold80deg; sampled at5deg, not a continuous swept-volume proof.',
    insertion='Continuous cylinder envelope on detached lid subassembly, caps installed afterward.',
    limitation='Sampled geometry only; printing fit, adhesive retention and service strength untested.')
Path(__file__).with_name('dual-folding-lid-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(checks=len(checks),failed=[c for c in checks if not c['passed']],collisions=collisions,poses=samples)),flush=True)
assert all(c['passed'] for c in checks) and not collisions
