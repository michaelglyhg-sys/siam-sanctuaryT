import bpy, math, random, os
from mathutils import Vector
random.seed(71)
ROOT=r'C:/Users/123/Desktop/阿瑜陀耶/temple-sanctuary'
OUT=ROOT+'/public/assets'; SRC=ROOT+'/art-source'
os.makedirs(OUT,exist_ok=True); os.makedirs(SRC,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)

def mat(name,c,metal=0,rough=.5,emission=None):
 m=bpy.data.materials.new(name); m.diffuse_color=(*c,1); m.use_nodes=True
 p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'); p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 if emission:p.inputs['Emission Color'].default_value=(*c,1);p.inputs['Emission Strength'].default_value=emission
 return m
gold=mat('Antique warm gold',(.83,.46,.105),.8,.27); palegold=mat('Raised gold ornament',(.98,.69,.23),.75,.24)
white=mat('Warm carved limestone',(.76,.70,.59),0,.72); stone=mat('Sandstone plinth',(.43,.35,.25),0,.85); wood=mat('Dark carved teak',(.12,.034,.017),0,.42)
roofm=[mat('Fired terracotta %02d'%i,(.35+i*.025,.052+i*.007,.012+i*.004),.1,.35) for i in range(5)]
leafm=[mat('Palm leaf %02d'%i,(.035+i*.012,.12+i*.018,.032+i*.008),0,.67) for i in range(3)]
bark=mat('Ringed palm bark',(.22,.16,.092),0,.95); dark=mat('Deep ornamental recess',(.035,.026,.017),.4,.5);glow=mat('Amber lantern glass',(.99,.43,.085),.1,.25,1.8)
current=[]
def mesh(name,vs,fs,m,smooth=False):
 d=bpy.data.meshes.new(name);d.from_pydata(vs,[],fs);d.update();o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);o.data.materials.append(m);current.append(o)
 if smooth:
  for p in d.polygons:p.use_smooth=True
 return o

def cube(name,loc,scale,m,bevel=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);current.append(o)
 if bevel:
  mod=o.modifiers.new('Crafted edges','BEVEL');mod.width=bevel;mod.segments=2;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
 return o

def sphere(name,loc,scale,m,seg=24,rings=16):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=rings,radius=1,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);current.append(o)
 for p in o.data.polygons:p.use_smooth=True
 return o

def cyl(name,loc,r,depth,m,r2=None,n=32):
 bpy.ops.mesh.primitive_cone_add(vertices=n,radius1=r,radius2=r if r2 is None else r2,depth=depth,location=loc);o=bpy.context.object;o.name=name;o.data.materials.append(m);current.append(o)
 for p in o.data.polygons:p.use_smooth=True
 return o

def tube(name,pts,r,m,n=8):
 if name=='Draped arm':
  orig=[Vector(p) for p in pts];rr=r;new=[];rnew=[]
  for k in range(len(orig)-1):
   a=orig[max(0,k-1)];b=orig[k];c=orig[k+1];d=orig[min(len(orig)-1,k+2)]
   for q in range(7):
    t=q/7;new.append(tuple(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t)))
    rnew.append(rr[k]*(1-t)+rr[k+1]*t)
  new.append(tuple(orig[-1]));rnew.append(rr[-1]);pts=new;r=rnew
 vs=[];fs=[]
 for i,p in enumerate(pts):
  t=(Vector(pts[min(i+1,len(pts)-1)])-Vector(pts[max(0,i-1)])).normalized(); ref=Vector((0,0,1)) if abs(t.z)<.9 else Vector((1,0,0));a=t.cross(ref).normalized();b=t.cross(a).normalized()
  rad=r[i] if isinstance(r,list) else r
  for j in range(n):vs.append(tuple(Vector(p)+rad*(a*math.cos(j*math.tau/n)+b*math.sin(j*math.tau/n))))
 for i in range(len(pts)-1):
  for j in range(n):a=i*n+j;b=i*n+(j+1)%n;fs.append((a,b,b+n,a+n))
 fs.extend([tuple(range(n-1,-1,-1)),tuple((len(pts)-1)*n+j for j in range(n))]);return mesh(name,vs,fs,m,True)

def flame(name,x,y,z,size,m=palegold):
 pts=[]
 for j in range(14):
  t=j/13;pts.append((x+size*.26*math.sin(t*math.pi*1.4),y,z+size*t))
 tube(name,pts,[size*.14*(1-j/14)**1.35+.004 for j in range(14)],m)

def export(name,objects):
 bpy.ops.object.select_all(action='DESELECT')
 # merge objects by material; export with transforms applied
 groups={}
 for o in objects:
  if o.type=='MESH':groups.setdefault(o.data.materials[0].name,[]).append(o)
 merged=[]
 for material,group in groups.items():
  bpy.ops.object.select_all(action='DESELECT')
  for o in group:o.select_set(True)
  bpy.context.view_layer.objects.active=group[0];bpy.ops.object.join();o=bpy.context.object;o.name=name+' / '+material
  bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);mod=o.modifiers.new('Web surface reduction','DECIMATE');mod.ratio=.42;bpy.ops.object.modifier_apply(modifier=mod.name);merged.append(o)
 bpy.ops.object.select_all(action='DESELECT')
 for o in merged:o.select_set(True)
 bpy.ops.export_scene.gltf(filepath=OUT+'/'+name+'.glb',export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_materials='EXPORT')
 print('ASSET',name,len(merged),sum(len(o.data.polygons) for o in merged))
 for o in merged:o.hide_render=True;o.hide_set(True)
 return merged

# Seated Buddha with sculpted face, robe, lotus throne.
for z,r,h in [(.12,1.6,.24),(.34,1.45,.2),(.58,1.3,.25)]:cyl('Lotus pedestal',(0,0,z),r,h,gold,n=64)
for j in range(32):
 a=j*math.tau/32;o=sphere('Lotus throne petal',(1.3*math.cos(a),1.3*math.sin(a),.56),(.17,.09,.32),palegold,12,8);o.rotation_euler=(0,.4,a)
# cross-legged base
for s in [-1,1]:
 o=sphere('Folded knee',(s*.67,-.12,.97),(.74,.5,.34),gold);o.rotation_euler[2]=s*.22
 o=sphere('Crossed shin',(s*.23,-.52,.91),(.68,.22,.2),gold);o.rotation_euler[2]=-s*.28
 sphere('Resting foot',(s*.56,-.59,1.06),(.34,.17,.16),palegold)
# shaped elliptical torso profile
vs=[];fs=[]
profile=[(1.04,.5,.28),(1.2,.58,.31),(1.45,.5,.27),(1.8,.51,.3),(2.1,.59,.31),(2.37,.66,.3),(2.51,.58,.24),(2.59,.28,.2)]
for z,rx,ry in profile:
 for j in range(48):
  a=j*math.tau/48;vs.append((rx*math.cos(a),ry*math.sin(a),z))
for k in range(len(profile)-1):
 for j in range(48):a=k*48+j;b=k*48+(j+1)%48;fs.append((a,b,b+48,a+48))
fs.extend([tuple(range(47,-1,-1)),tuple((len(profile)-1)*48+j for j in range(48))]);mesh('Sculpted robe torso',vs,fs,gold,True)
cyl('Neck',(0,0,2.67),.19,.3,gold,n=32)
sphere('Serene head',(0,-.015,3.05),(.355,.29,.46),palegold,40,28)
sphere('Cranial topknot',(0,.02,3.49),(.23,.21,.24),gold,24,16)
flame('Ushnisha flame',0,0,3.61,.65)
# close eyes and brows, low relief face towards -Y
for s in [-1,1]:
 sphere('Long earlobe',(s*.35,.005,2.94),(.075,.09,.28),palegold,20,12)
 tube('Peaceful eyelid',[(s*.055,-.292,3.105),(s*.13,-.303,3.09),(s*.215,-.263,3.105)],.018,gold,8)
 tube('Eyebrow',[(s*.04,-.282,3.2),(s*.13,-.296,3.23),(s*.23,-.245,3.21)],.018,gold,8)
sphere('Nose',(0,-.31,3.035),(.052,.074,.13),palegold,16,12)
tube('Quiet smile',[(-.1,-.283,2.91),(0,-.311,2.899),(.1,-.283,2.91)],.018,gold,8)
# Both palms rest together in the lap, dhyana pose.
for side in [-1,1]:
 tube('Draped arm',[(side*.54,0,2.42),(side*.77,-.04,2.02),(side*.75,-.25,1.63),(side*.38,-.47,1.38),(side*.06,-.5,1.4)],[.2,.18,.14,.10,.07],gold,14)
 sphere('Meditation palm',(side*.09,-.5,1.4+side*.035),(.2,.12,.065),palegold)
# Sculpt anatomical masses as one gently smoothed form to avoid intersecting primitives.
for ss in [-1,1]:sphere('Shoulder joint',(ss*.53,0,2.39),(.24,.24,.24),gold,24,16)
body_names=['Folded knee','Crossed shin','Resting foot','Sculpted robe torso','Neck','Serene head','Long earlobe','Nose','Draped arm','Earth touching hand','Meditation palm','Shoulder joint']
body=[o for o in current if any(o.name.startswith(n) for n in body_names)]
bpy.ops.object.select_all(action='DESELECT')
for o in body:o.select_set(True)
bpy.context.view_layer.objects.active=body[0];bpy.ops.object.join();o=bpy.context.object;o.name='Unified gilded figure'
mod=o.modifiers.new('Sculpted union','REMESH');mod.mode='VOXEL';mod.voxel_size=.035;bpy.ops.object.modifier_apply(modifier=mod.name)
mod=o.modifiers.new('Hand finished surface','SMOOTH');mod.factor=.8;mod.iterations=4;bpy.ops.object.modifier_apply(modifier=mod.name)
for p in o.data.polygons:p.use_smooth=True
current=[v for v in current if v not in body]+[o]
# Spiral hair curls, modest relief around the top of the head.
for row in range(6):
 a=.63+row*.13
 for j in range(20):
  t=j*math.tau/20+row*.15
  sphere('Sculpted hair curl',(.35*math.cos(a)*math.cos(t),-.015+.29*math.cos(a)*math.sin(t),3.05+.46*math.sin(a)),(.035,.035,.035),gold,8,6)
# robe sculpted hems crossing left shoulder diagonally
for j in range(14):
 t=j/13
 pts=[(-.55+t*.03,-.13,2.45-t*.04),(-.35+t*.25,-.3,2.1-t*.1),(.1+t*.25,-.31,1.7-t*.16),(.42+t*.09,-.25,1.24-t*.08)]
 tube('Fine robe fold',pts,.009 if j%3 else .018,palegold,5)
# large flame mandorla at the back, open ring
pts=[(1.2*math.sin(a),.42,2.25+1.75*math.cos(a)) for a in [math.pi*.48+i*math.pi*1.04/64 for i in range(65)]]
# complete pointed arch rather than enclosing the figure
pts=[(-1.1,.42,.9),(-1.3,.42,2.0),(-.96,.42,3.2),(0,.42,4.65),(.96,.42,3.2),(1.3,.42,2.0),(1.1,.42,.9)]
tube('Flame aureole',pts,.065,gold,10)
for s in [-1,1]:
 for j in range(10):
  t=j/10;x=s*(1.27*(1-t)+.05*t);z=2.1+2.45*t;flame('Aureole flame',x,.43,z,.29)
meditation=export('buddha-meditation',current);current=[]


# Flowing standing/walking figure, gently advanced left leg, raised reassurance hand.
for z,r,h in [(.12,.85,.24),(.32,.72,.16)]:cyl('Walking lotus base',(0,0,z),r,h,gold,n=48)
for side in [-1,1]:
 y=-.19 if side<0 else .13
 tube('Walking leg',[(side*.19,0,1.74),(side*.2,y,.98),(side*.2,y-.03,.48)],[.18,.14,.09],gold,16)
 sphere('Walking foot',(side*.2,y-.17,.46),(.13,.28,.09),palegold)
# continuous robe volume
vs=[];fs=[]
for z,rx,ry in [(1.0,.32,.22),(1.5,.4,.25),(1.9,.39,.24),(2.25,.43,.25),(2.6,.5,.24),(2.73,.22,.16)]:
 for j in range(36):
  a=j*math.tau/36;vs.append((rx*math.cos(a),ry*math.sin(a),z))
for i in range(5):
 for j in range(36):a=i*36+j;b=i*36+(j+1)%36;fs.append((a,b,b+36,a+36))
mesh('Flowing robe',vs,fs,gold,True)
cyl('Neck',(0,0,2.84),.14,.27,gold,n=24)
sphere('Serene head',(0,0,3.14),(.27,.23,.35),palegold,32,20)
for side in [-1,1]:
 sphere('Elongated earlobe',(side*.27,0,3.06),(.055,.065,.2),palegold,16,10)
 tube('Lowered eyelid',[(side*.04,-.225,3.18),(side*.1,-.235,3.17),(side*.17,-.20,3.18)],.012,gold)
 sphere('Brow',(side*.1,-.21,3.25),(.1,.024,.017),gold,16,8)
sphere('Sculpted nose',(0,-.25,3.12),(.037,.05,.095),palegold,16,10)
tube('Subtle smile',[(-.07,-.218,3.04),(0,-.24,3.03),(.07,-.218,3.04)],.012,gold)
sphere('Topknot',(0,0,3.47),(.15,.14,.17),gold)
flame('Crown flame',0,0,3.57,.48)
tube('Draped arm',[(-.45,0,2.6),(-.62,-.05,2.2),(-.6,-.13,1.79)],[.14,.12,.07],gold,14)
sphere('Lowered hand',(-.6,-.13,1.66),(.08,.06,.16),palegold)
tube('Draped arm',[(.45,0,2.6),(.62,-.02,2.26),(.77,-.2,2.58)],[.14,.12,.07],gold,14)
sphere('Raised palm',(.78,-.22,2.74),(.09,.045,.14),palegold)
for j in range(4):tube('Raised fingers',[(.72+j*.04,-.22,2.81),(.72+j*.04,-.22,2.96-abs(j-1.5)*.025)],.017,palegold,6)
for j in range(13):
 t=j/12;tube('Robe fold',[(-.42+t*.07,-.11,2.61),(-.2+t*.25,-.26,2.28),(.13+t*.14,-.25,1.85),(.19+t*.1,-.21,1.12)],.01,palegold,5)
walking=export('buddha-walking',current);current=[]
# Guardian yaksha, carved sandstone and gold ceremonial armor.
rock=mat('Guardian carved warm sandstone',(.32,.36,.31),0,.8)
cube('Guardian base',(0,0,.15),(1.1,.9,.3),stone,.06)
for side in [-1,1]:
 sphere('Guardian foot',(side*.24,-.15,.4),(.19,.3,.13),rock)
 tube('Guardian leg',[(side*.25,0,.45),(side*.26,0,1.05),(side*.24,0,1.4)],[.16,.19,.21],rock,14)
sphere('Armored torso',(0,0,1.58),(.48,.3,.55),rock)
for z in [1.2,1.34,1.48]:cyl('Armor waist ring',(0,0,z),.44,.07,gold,n=20)
for side in [-1,1]:
 sphere('Shoulder armor',(side*.45,0,1.91),(.22,.29,.19),gold)
 tube('Guarding arm',[(side*.45,0,1.9),(side*.58,-.05,1.59),(side*.2,-.35,1.4)],[.17,.15,.1],rock,12)
 sphere('Gripping fist',(side*.13,-.37,1.42),(.13,.12,.13),rock)
cyl('Ceremonial club',(0,-.43,1.15),.085,1.65,wood,n=16)
sphere('Club pommel',(0,-.43,1.9),(.14,.14,.2),gold)
sphere('Yaksha face',(0,0,2.24),(.33,.27,.32),rock,32,20)
for side in [-1,1]:
 sphere('Guardian eye',(side*.13,-.24,2.28),(.095,.06,.065),white,16,10)
 sphere('Guardian pupil',(side*.13,-.29,2.28),(.024,.015,.035),dark,12,8)
 tube('Carved eyebrow',[(side*.04,-.25,2.38),(side*.13,-.28,2.4),(side*.24,-.2,2.36)],.035,rock)
 tube('Ivory tusk',[(side*.15,-.25,2.06),(side*.18,-.31,2.14),(side*.16,-.31,2.22)],[.045,.025,.002],white,10)
 sphere('Guard ear',(side*.34,0,2.25),(.09,.08,.16),rock)
sphere('Broad nose',(0,-.28,2.23),(.1,.08,.09),rock)
tube('Carved mouth',[(-.17,-.25,2.12),(0,-.3,2.09),(.17,-.25,2.12)],.025,dark)
for i in range(5):cyl('Tiered crown',(0,0,2.55+i*.13),.36-i*.065,.16,gold,r2=.31-i*.065,n=16)
guardian=export('guardian',current);current=[]

for group in [meditation,walking,guardian]:
 for o in group:o.hide_render=False;o.hide_set(False)
for o in meditation:o.location.x=-3.5
for o in guardian:o.location.x=3.5
scene=bpy.context.scene
bpy.ops.object.camera_add(location=(9,-16,8));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,2))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=12;scene.camera=cam
for loc,power,size in [((0,-7,10),1800,8),((-6,2,7),1400,6),((6,0,6),900,5)]:
 bpy.ops.object.light_add(type='AREA',location=loc);light=bpy.context.object;light.data.energy=power;light.data.shape='DISK';light.data.size=size;light.rotation_euler=(Vector((0,0,2))-light.location).to_track_quat('-Z','Y').to_euler()
scene.world=bpy.data.worlds.new('Neutral preview');scene.world.use_nodes=True;next(n for n in scene.world.node_tree.nodes if n.type=='BACKGROUND').inputs[0].default_value=(.15,.18,.21,1)
scene.render.engine='CYCLES';scene.cycles.samples=24;scene.render.resolution_x=1400;scene.render.resolution_y=800;scene.render.resolution_percentage=100
bpy.ops.wm.save_as_mainfile(filepath=SRC+'/supplemental-sculptures.blend');scene.render.filepath=SRC+'/supplemental-sculptures-preview.png';bpy.ops.render.render(write_still=True)
