from pathlib import Path
p=Path('art-source/generate_reference_visitors.py').read_text(encoding='utf-8')
pre='''import bpy,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(r'C:/Users/123/Desktop/阿瑜陀耶/temple-sanctuary');SRC=ROOT/'art-source'
bpy.ops.wm.read_factory_settings(use_empty=True)
report=[]
for name,x in [('visitor-male',-.42),('visitor-female',.42)]:
 bpy.ops.import_scene.gltf(filepath=str(ROOT/'public/assets'/f'{name}.glb'))
 objects=list(bpy.context.selected_objects)
 points=[o.matrix_world@Vector(c) for o in objects if o.type=='MESH' for c in o.bound_box]
 report.append({'asset':name,'height':max(p.z for p in points)-min(p.z for p in points),'min_z':min(p.z for p in points),'triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in objects if o.type=='MESH')})
 for o in objects:
  if o.parent is None:o.location.x=x
 for o in objects:o.name=name+'_'+o.name
(SRC/'reference-visitors-report.json').write_text(json.dumps(report,indent=2))
'''
render=p[p.index('scene=bpy.context.scene'):].replace("bpy.ops.wm.save_as_mainfile(filepath=str(SRC/'reference-visitors.blend'));",'').replace('reference-visitors-preview.png','reference-visitors-glb-verified.png')
Path('art-source/verify_reference_visitors.py').write_text(pre+render,encoding='utf-8')
