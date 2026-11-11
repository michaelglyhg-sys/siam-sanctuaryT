import bpy,math,json
from mathutils import Vector
from pathlib import Path
ROOT=Path(r'C:/Users/123/Desktop/阿瑜陀耶/temple-sanctuary'); SRC=ROOT/'art-source'; OUT=ROOT/'public/assets'
bpy.ops.wm.read_factory_settings(use_empty=True)
def mat(n,c,metal=.8,rough=.33):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
edge=mat('Hand chased pale gold',(.76,.48,.16));recess=mat('Subtle carved recess',(.27,.135,.035),.7,.5)
def sphere(n,p,sc,m):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=8,ring_count=6,location=p);o=bpy.context.object;o.name=n;o.scale=sc;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m)
 for f in o.data.polygons:f.use_smooth=True
 return o
def line(n,pts,r,m=edge):
 c=bpy.data.curves.new(n,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=0;c.resolution_u=2;s=c.splines.new('POLY');s.points.add(len(pts)-1)
 for v,p in zip(s.points,pts):v.co=(*p,1)
 o=bpy.data.objects.new(n,c);bpy.context.collection.objects.link(o);o.data.materials.append(m);bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');o.select_set(False);return o
names=['buddha','buddha-lod','buddha-meditation','buddha-teaching','buddha-walking','buddha-standing','buddha-reassurance'];report=[];show=[]
for index,name in enumerate(names):
 bpy.ops.object.select_all(action='DESELECT');bpy.ops.import_scene.gltf(filepath=str(OUT/(name+'.glb')));original=list(bpy.context.selected_objects);before=set(bpy.data.objects);standing=name in names[4:];hx=.27 if standing else .355;hy=.23 if standing else .29;hz=.35 if standing else .46;cz=3.14 if standing else 3.05;cy=0 if standing else -.015
 # Contoured lower eyelids, inner corners, nose wings and softly separated lips.
 for side in [-1,1]:
  line('Lower eyelid incision',[(side*x,-hy*math.sqrt(max(.02,1-(x/hx)**2-((z-cz)/hz)**2))+cy-.009,z) for x,z in [(.04,cz+.035),(.085,cz+.022),(.14,cz+.027),(.18 if not standing else .16,cz+.04)]],.005,recess)
  sphere('Sculpted nostril wing',(side*.033 if standing else side*.046,-.254 if standing else -.343,cz-.06),(.018,.017,.018),edge)
  sphere('Nostril cut',(side*.024 if standing else side*.033,-.266 if standing else -.361,cz-.068),(.009,.004,.005),recess)
  ex=side*(.27 if standing else .35);ez=cz-.06
  line('Inner ear helix',[(ex+side*.018*math.sin(a),-.055,ez+.10*math.cos(a)) for a in [j*math.tau/24 for j in range(25)]],.008)
  line('Earlobe recess',[(ex,-.065,ez-.03),(ex+side*.015,-.067,ez-.08),(ex,-.065,ez-.13)],.005,recess)
 mouthz=cz-.11;mouthy=-.24 if standing else -.293
 for sign in [-1,1]:line('Cupid lip ridge',[(-.064,mouthy+.017,mouthz),(-.025,mouthy-.006,mouthz+sign*.01),(0,mouthy-.009,mouthz+sign*.007),(.025,mouthy-.006,mouthz+sign*.01),(.064,mouthy+.017,mouthz)],.006)
 # Individual spiral curl engravings follow the scalp ellipsoid.
 for row in range(5):
  latitude=.7+row*.15
  for j in range(18):
   az=j*math.tau/18+row*.12;center=Vector((hx*math.cos(latitude)*math.cos(az),cy+hy*math.cos(latitude)*math.sin(az),cz+hz*math.sin(latitude)))
   tangent=Vector((-math.sin(az),math.cos(az),0));up=Vector((-math.sin(latitude)*math.cos(az),-math.sin(latitude)*math.sin(az),math.cos(latitude)))
   pts=[tuple(center+tangent*(.021*(1-k/16)*math.cos(k*.64))+up*(.021*(1-k/32)*math.sin(k*.32))) for k in range(13)]
   line('Spiral hair engraving',pts,.0035)
 # Brocade-like robe border, with continuous fine incision rather than random surface noise.
 for k in range(26):
  t=k/25;z=2.50-t*1.05;x=-.43+t*.6;y=-.28-(.015 if not standing else 0)
  line('Robe hem chased leaf',[(x-.015,y,z+.018),(x+.015,y-.004,z),(x-.015,y,z-.018)],.004)
 # Lotus-petal veins and bead moulding around the plinth.
 radius=.75 if standing else 1.43;z=.30 if standing else .35
 for j in range(48):
  a=j*math.tau/48;sphere('Lotus bead moulding',(radius*math.cos(a),radius*math.sin(a),z),(.026,.026,.026),edge)
 for j in range(32):
  a=j*math.tau/32;r=.68 if standing else 1.30
  if standing:line('Lotus plinth chased petal',[(.72*math.cos(a),.72*math.sin(a),.22),(.77*math.cos(a),.77*math.sin(a),.28),(.72*math.cos(a),.72*math.sin(a),.34)],.004)
  else:line('Lotus petal central vein',[(r*math.cos(a),r*math.sin(a),z+.06),((r+.05)*math.cos(a),(r+.05)*math.sin(a),z+.14),(r*math.cos(a),r*math.sin(a),z+.24)],.006)
 added=[o for o in bpy.data.objects if o not in before and o.type=='MESH']
 # Batch all sculpted details by material for a small, fixed draw-call increase.
 merged=[]
 groups=[[o for o in added if o.data.materials[0]==m] for m in [edge,recess]]
 for group in groups:
  bpy.ops.object.select_all(action='DESELECT')
  for o in group:o.select_set(True)
  bpy.context.view_layer.objects.active=group[0];bpy.ops.object.join();merged.append(bpy.context.object)
 objects=original+merged;bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 path=OUT/(name+'-refined.glb');bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,export_yup=True)
 report.append({'asset':name+'-refined','bytes':path.stat().st_size,'triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in objects if o.type=='MESH')})
 for o in objects:o.hide_render=True;o.hide_set(True)
 show.append(objects)
# Render representative detailed seated and standing statues at source scale.
for idx,offset in [(0,-1.7),(4,1.9)]:
 for o in show[idx]:
  o.hide_render=False;o.hide_set(False)
  if o.parent is None:o.location.x+=offset
scene=bpy.context.scene;bpy.ops.object.camera_add(location=(5,-11,5));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,2.1))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=7;scene.camera=cam
for loc,power,size in [((0,-5,7),1200,5),((-5,-2,5),900,4),((3,4,6),1600,4)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,2))-o.location).to_track_quat('-Z','Y').to_euler()
scene.world=bpy.data.worlds.new('Neutral studio');scene.world.use_nodes=True;scene.world.node_tree.nodes.get('Background').inputs[0].default_value=(.18,.21,.24,1);scene.render.engine='CYCLES';scene.cycles.samples=24;scene.render.resolution_x=1400;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
bpy.ops.wm.save_as_mainfile(filepath=str(SRC/'buddha-fine-sculpt.blend'));scene.render.filepath=str(SRC/'buddha-fine-sculpt-preview.png');bpy.ops.render.render(write_still=True)
(SRC/'buddha-fine-sculpt-report.json').write_text(json.dumps(report,indent=2))
