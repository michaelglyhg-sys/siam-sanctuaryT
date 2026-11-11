import bpy,math,random
from mathutils import Vector
ROOT=r'C:/Users/123/Desktop/阿瑜陀耶/temple-sanctuary'
bpy.ops.wm.open_mainfile(filepath=ROOT+'/art-source/sanctuary-assets.blend')
random.seed(811)
# Compare mobile temple in the same validated viewpoint.
for o in bpy.data.objects:
 if o.type=='MESH' and (o.name.startswith('temple /') or o.name.startswith('buddha /') or o.name.startswith('palm /')):o.hide_render=True
for asset in ['temple','buddha','palm']:
 before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=ROOT+'/public/assets/'+asset+'-lod.glb')
 for o in set(bpy.data.objects)-before:
  if asset=='buddha':o.location=(0,5,.96)
  if asset=='palm':o.location=(-14,3,0)
scene=bpy.context.scene;scene.render.resolution_x=1400;scene.render.resolution_y=1000;scene.render.filepath=ROOT+'/art-source/mobile-lod-preview.png';bpy.ops.render.render(write_still=True)
# Restore full originals for final source render.
bpy.ops.wm.open_mainfile(filepath=ROOT+'/art-source/sanctuary-assets.blend')
def material(name,c,rough=.5,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True;p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;return m
paving=material('Source render sandstone',(.29,.245,.18),.67)
leaf=material('Source render lotus leaf',(.045,.16,.075),.62)
petal=material('Source render lotus petal',(.73,.22,.36),.4)
water=material('Source render pool water',(.035,.12,.105),.15,.55)
p=next(n for n in water.node_tree.nodes if n.type=='BSDF_PRINCIPLED');noise=water.node_tree.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=22;noise.inputs['Detail'].default_value=3;bump=water.node_tree.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.16;bump.inputs['Distance'].default_value=.12;water.node_tree.links.new(noise.outputs['Fac'],bump.inputs['Height']);water.node_tree.links.new(bump.outputs['Normal'],p.inputs['Normal'])
def cube(name,loc,size,mat):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat);return o
for x in [-10.1,10.1]:
 cube('Reflecting lotus pond',(x,-24,.035),(12.2,17,.1),water)
 for xx in [x-6.2,x+6.2]:cube('Pool stone border',(xx,-24,.17),(.26,17.5,.35),paving)
 for yy in [-32.7,-15.3]:cube('Pool stone border',(x,yy,.17),(12.7,.26,.35),paving)
 for j in range(34):
  lx=x+random.uniform(-5.6,5.6);ly=-24+random.uniform(-7.9,7.9)
  bpy.ops.mesh.primitive_circle_add(vertices=18,radius=random.uniform(.18,.42),fill_type='NGON',location=(lx,ly,.11));bpy.context.object.data.materials.append(leaf)
  if j%3==0:
   for a in range(7):
    ang=a*math.tau/7;bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=6,radius=1,location=(lx+.13*math.cos(ang),ly+.13*math.sin(ang),.17));o=bpy.context.object;o.scale=(.06,.19,.08);o.rotation_euler=(.3,0,ang-math.pi/2);o.data.materials.append(petal)
for x in range(-2,3):
 for j in range(27):cube('Processional sandstone paving',(x*1.17,-14.6-j*.79,.06),(1.145,.765,.12),paving)
originals=[o for o in bpy.data.objects if o.name.startswith('palm / ') and not o.name.endswith('.001')]
for px,py,sz in [(-17,-12,.95),(17,-12,1.05),(-19,-31,1.2),(19,-29,1.1),(-15,15,.85),(15,15,1.05)]:
 for original in originals:
  o=original.copy();o.data=original.data;bpy.context.collection.objects.link(o);o.location=(px,py,0);o.scale=(sz,sz,sz)
originals=[o for o in bpy.data.objects if o.name.startswith('lantern / ') and not o.name.endswith('.001')]
for lx in [-3.5,3.5]:
 for ly in [-20,-26,-32]:
  for original in originals:
   o=original.copy();o.data=original.data;bpy.context.collection.objects.link(o);o.location=(lx,ly,0)
world=bpy.context.scene.world;nodes=world.node_tree.nodes;sky=nodes.new('ShaderNodeTexSky');sky.sky_type=next(i.identifier for i in sky.bl_rna.properties['sky_type'].enum_items if i.identifier=='MULTIPLE_SCATTERING');sky.sun_elevation=.18;sky.sun_rotation=2.3;sky.altitude=.2;sky.air_density=1.3;sky.aerosol_density=2;world.node_tree.links.new(sky.outputs['Color'],nodes.get('Background').inputs[0]);nodes.get('Background').inputs[1].default_value=.19
for o in bpy.data.objects:
 if o.type=='LIGHT' and o.data.type=='SUN':o.data.energy=1.4;o.data.color=(1,.65,.38);o.rotation_euler=(.2,-.8,-.6)
bpy.ops.object.light_add(type='AREA',location=(0,-1,5));bpy.context.object.data.energy=550;bpy.context.object.data.color=(1,.65,.23);bpy.context.object.data.size=5
scene=bpy.context.scene;cam=scene.camera;cam.location=(25,-43,14);cam.rotation_euler=(Vector((0,-6,5.5))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=37
scene.cycles.samples=64;scene.render.resolution_x=1600;scene.render.resolution_y=1000;scene.render.filepath=ROOT+'/art-source/sanctuary-showcase.png'
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/art-source/sanctuary-showcase.blend')
bpy.ops.render.render(write_still=True)
