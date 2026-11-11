import bpy
from mathutils import Vector
ROOT=r'C:/Users/123/Desktop/阿瑜陀耶/temple-sanctuary'
bpy.ops.wm.open_mainfile(filepath=ROOT+'/art-source/sanctuary-showcase.blend')
for o in bpy.data.objects:
 if o.name=='Preview ground':o.scale=(20,20,1)
 if o.type=='MESH' and o.location.x>18 and o.location.y<-20:o.location.x+=10
 if o.type=='LIGHT' and o.data.type=='AREA' and o.data.energy>1000:o.data.energy=1800
scene=bpy.context.scene;scene.world.node_tree.nodes.get('Background').inputs[1].default_value=.08
cam=scene.camera;cam.location=(22,-48,17);cam.rotation_euler=(Vector((0,-6,6))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=39
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/art-source/sanctuary-showcase.blend');bpy.ops.render.render(write_still=True)
