import bpy
from mathutils import Vector
ROOT=r'C:/Users/123/Desktop/阿瑜陀耶/temple-sanctuary'
bpy.ops.wm.open_mainfile(filepath=ROOT+'/art-source/sanctuary-assets.blend')
for o in bpy.data.objects:
 if o.type=='MESH':
  o.hide_render=not o.name.startswith('buddha')
  if o.name.startswith('buddha'):o.location=(0,0,0)
cam=bpy.context.scene.camera;cam.location=(5,-8,4.4);cam.rotation_euler=(Vector((0,0,2.15))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=60
scene=bpy.context.scene;scene.render.resolution_x=900;scene.render.resolution_y=1000;scene.render.filepath=ROOT+'/art-source/buddha-preview.png';bpy.ops.render.render(write_still=True)
