import bpy,os,json,math
import numpy as np
ROOT=r'C:/Users/123/Desktop/阿瑜陀耶/temple-sanctuary'
bpy.ops.wm.open_mainfile(filepath=ROOT+'/art-source/sanctuary-assets.blend')
# Original deterministic terracotta PBR atlas for mobile roof surfaces.
N=512; yy,xx=np.mgrid[0:N,0:N];u=(xx%32)/32;v=(yy%32)/32
rng=np.random.default_rng(74);patch=rng.random((16,16))[yy//32,xx//32]
seam=(u<.04)|(v<.055);ridge=np.sin(u*np.pi)**1.7
h=.12*ridge-.09*seam+.035*(v>.93)
noise=rng.normal(0,.009,(N,N));base=np.empty((N,N,4),dtype=np.float32)
for ch,c in enumerate([.58,.18,.047]):base[:,:,ch]=c*(.84+.22*patch+.1*ridge)+noise
base[seam,:3]*=.55;base[:,:,3]=1
normal=np.ones((N,N,4),dtype=np.float32);dy,dx=np.gradient(h);vec=np.dstack((-dx*16,-dy*16,np.ones_like(h)));vec/=np.linalg.norm(vec,axis=2,keepdims=True);normal[:,:,:3]=vec*.5+.5
roofmat=bpy.data.materials.new('Mobile terracotta tiled PBR');roofmat.use_nodes=True;p=next(n for n in roofmat.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Roughness'].default_value=.42
for name,pixels,kind in [('roof_tile_base',base,'base'),('roof_tile_normal',normal,'normal')]:
 image=bpy.data.images.new(name,width=N,height=N,alpha=True);image.colorspace_settings.name='sRGB' if kind=='base' else 'Non-Color';image.pixels.foreach_set(pixels.ravel());image.filepath_raw=ROOT+'/art-source/'+name+'.png';image.file_format='PNG';image.save();image.pack()
 tex=roofmat.node_tree.nodes.new('ShaderNodeTexImage');tex.image=image
 if kind=='base':roofmat.node_tree.links.new(tex.outputs['Color'],p.inputs['Base Color'])
 else:
  nm=roofmat.node_tree.nodes.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.7;roofmat.node_tree.links.new(tex.outputs['Color'],nm.inputs['Color']);roofmat.node_tree.links.new(nm.outputs['Normal'],p.inputs['Normal'])
results=[]
for asset,ratio in [('temple',.31),('buddha',.16),('palm',.34)]:
 bpy.ops.object.select_all(action='DESELECT');selected=[]
 for original in list(bpy.data.objects):
  if original.type=='MESH' and original.name.startswith(asset+' / ') and not original.name.endswith('.001') and not (asset=='temple' and original.data.materials[0].name.startswith('Fired terracotta')):
   o=original.copy();o.data=original.data.copy();bpy.context.collection.objects.link(o);o.hide_render=False;o.hide_set(False);o.location=(0,0,0);o.select_set(True);bpy.context.view_layer.objects.active=o
   if len(o.data.polygons)>150:
    mod=o.modifiers.new('Mobile silhouette LOD','DECIMATE');mod.ratio=ratio;mod.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=mod.name)
   o.data.validate(verbose=False);o.data.update();o.name=asset+' LOD / '+o.data.materials[0].name;selected.append(o)
 if asset=='temple':
  vs=[];fs=[];uvs=[]
  for w,l,eave,peak in [(9.6,23.4,6.75,12.4),(7.6,19.1,9.1,14.2),(5.35,14.5,11.65,15.8)]:
   for side in [-1,1]:
    start=len(vs)
    for k in range(33):
     u=k/32;z=peak-(peak-eave)*u**.82+.35*u**8
     for y in [-l/2,l/2]:vs.append((side*w*u,y,z));uvs.append((y/8,w*u/8))
    for k in range(32):
     quad=(start+k*2,start+k*2+1,start+k*2+3,start+k*2+2);fs.append(quad if side<0 else tuple(reversed(quad)))
  d=bpy.data.meshes.new('Mobile tiled roof');d.from_pydata(vs,[],fs);d.update();o=bpy.data.objects.new('temple LOD / Mobile tiled roof',d);bpy.context.collection.objects.link(o);d.materials.append(roofmat)
  uv=d.uv_layers.new(name='UVMap')
  for poly in d.polygons:
   poly.use_smooth=True
   for li in poly.loop_indices:uv.data[li].uv=uvs[d.loops[li].vertex_index]
  selected.append(o)
 bpy.ops.object.select_all(action='DESELECT')
 for o in selected:o.select_set(True)
 bpy.ops.export_scene.gltf(filepath=ROOT+'/public/assets/'+asset+'-lod.glb',export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_materials='EXPORT')
 tris=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in selected)
 results.append({'name':asset+'-lod','triangles':tris,'meshes':len(selected)})
 for o in selected:bpy.data.objects.remove(o,do_unlink=True)
print(json.dumps(results))
open(ROOT+'/art-source/mobile-lod-report.json','w').write(json.dumps(results,indent=2))

