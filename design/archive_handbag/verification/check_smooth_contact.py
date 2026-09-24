"""Read-only verification of exported STEP geometry and derived preview sampling."""
import json, math, struct, sys, hashlib
from pathlib import Path
from itertools import combinations
from build123d import import_step, Vertex

baseline, current, old_glb, new_glb, revision = sys.argv[1:]
old={x.label:x for x in import_step(baseline).children}
assembly=import_step(current)
parts={x.label:x for x in assembly.children}
report={'revision':revision,'step_sha256':hashlib.sha256(Path(current).read_bytes()).hexdigest(),'baseline_step_sha256':hashlib.sha256(Path(baseline).read_bytes()).hexdigest(),'objects':len(parts),'solids':len(assembly.solids()),'all_valid':all(x.is_valid for x in parts.values()),'envelope_mm':list(assembly.bounding_box().size)}
R=88+1/3
cy=-51+math.sqrt(R*R-32*32)
report['tongue_back_contact']=[]
for z in range(84,101):
 p=Vertex(0,cy-math.sqrt(R*R-(z-96)**2),z)
 report['tongue_back_contact'].append({'z':z,'strap_distance_mm':parts['central_binding'].distance_to(p),'metal_distance_mm':parts['buckle'].distance_to(p)})
report['refinement_equivalence']=[]
for name in ['blue_spine','side_left','side_right','central_binding']:
 # Unify coplanar/tangent analytic patches in memory for an economical exact comparison.
 a=old[name].clean(); b=parts[name].clean()
 removed=a-b; added=b-a
 delta=(abs(removed.volume) if removed else 0)+(abs(added.volume) if added else 0)
 report['refinement_equivalence'].append({'object':name,'symmetric_difference_mm3':delta,'passed':delta<1e-5})
report['key_clearances_mm']={name:parts[name].distance_to(parts['blue_spine']) for name in ['side_left','side_right']}
report['buckle_strap_intersection_mm3']=0
intersection=parts['buckle'].clean() & parts['central_binding'].clean()
if intersection: report['buckle_strap_intersection_mm3']=abs(intersection.volume)

def sampling(path):
 data=Path(path).read_bytes(); n=struct.unpack_from('<I',data,12)[0]
 doc=json.loads(data[20:20+n]); payload=20+n+8
 def accessor(i):
  a=doc['accessors'][i]; v=doc['bufferViews'][a['bufferView']]
  return [struct.unpack_from('<fff',data,payload+v.get('byteOffset',0)+a.get('byteOffset',0)+k*v.get('byteStride',12)) for k in range(a['count'])]
 result={}
 for name,index,center_z,center_y,lo,hi in [('lower',4,32,cy,4,64),('middle',4,96,cy,64,128),('lower_binding',5,32,cy,4,64),('middle_binding',5,96,cy,64,128),('lid',1,31.3,-51+math.sqrt(R*R-30.7**2)-60.5,.6,62)]:
  points=[]
  for primitive in doc['meshes'][index]['primitives']: points.extend(accessor(primitive['attributes']['POSITION']))
  angles=sorted(set(round(math.degrees(math.atan2(z*1000-center_z,center_y-y*1000)),5) for x,y,z in points if lo-1e-3<=z*1000<=hi+1e-3 and y*1000<center_y and abs(math.hypot(y*1000-center_y,z*1000-center_z)-R)<.002))
  result[name]={'angular_stations':len(angles),'max_step_deg':max(b-a for a,b in zip(angles,angles[1:]))}
 return result
report['preview_sampling_before']=sampling(old_glb)
report['preview_sampling_after']=sampling(new_glb)
report['passed']=report['all_valid'] and report['solids']==33 and all(x['passed'] for x in report['refinement_equivalence']) and all(max(x['strap_distance_mm'],x['metal_distance_mm'])<1e-5 for x in report['tongue_back_contact']) and report['buckle_strap_intersection_mm3']<1e-5 and all(report['preview_sampling_after'][n]['max_step_deg']<min(2.01,report['preview_sampling_after']['lid']['max_step_deg']) for n in ['lower','middle','lower_binding','middle_binding'])
Path('design/archive_handbag/verification/smooth-contact-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert report['passed']
