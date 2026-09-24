import json, math, struct, sys, hashlib
from pathlib import Path
R=88+1/3
cy=-51+math.sqrt(R*R-32*32)
def sampling(path):
 data=Path(path).read_bytes(); n=struct.unpack_from('<I',data,12)[0]
 doc=json.loads(data[20:20+n]); payload=20+n+8
 def accessor(i):
  a=doc['accessors'][i]; v=doc['bufferViews'][a['bufferView']]
  return [struct.unpack_from('<fff',data,payload+v.get('byteOffset',0)+a.get('byteOffset',0)+k*v.get('byteStride',12)) for k in range(a['count'])]
 result={}
 for name,index,center_z,center_y,lo,hi in [('upper_binding',6,159.3,-51+math.sqrt(R*R-30.7**2),128.6,190),('lower',4,32,cy,4,64),('middle',4,96,cy,64,128),('lower_binding',5,32,cy,4,64),('middle_binding',5,96,cy,64,128),('lid',1,31.3,-51+math.sqrt(R*R-30.7**2)-60.5,.6,62)]:
  points=[]
  for primitive in doc['meshes'][index]['primitives']: points.extend(accessor(primitive['attributes']['POSITION']))
  angles=sorted(set(round(math.degrees(math.atan2(z*1000-center_z,center_y-y*1000)),5) for x,y,z in points if lo-1e-3<=z*1000<=hi+1e-3 and y*1000<center_y and abs(math.hypot(y*1000-center_y,z*1000-center_z)-R)<.002))
  result[name]={'angular_stations':len(angles),'max_step_deg':max(b-a for a,b in zip(angles,angles[1:]))}
 return result

path,revision=sys.argv[1:]
r={'revision':revision,'glb_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'sampling':sampling(path)}
r['passed']=r['sampling']['upper_binding']['max_step_deg']<=r['sampling']['lid']['max_step_deg']+.01
Path('design/archive_handbag/verification/upper-binding-sampling.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2));assert r['passed']
