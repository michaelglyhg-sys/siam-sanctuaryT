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
  bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);merged.append(o)
 bpy.ops.object.select_all(action='DESELECT')
 for o in merged:o.select_set(True)
 bpy.ops.export_scene.gltf(filepath=OUT+'/'+name+'.glb',export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_materials='EXPORT')
 print('ASSET',name,len(merged),sum(len(o.data.polygons) for o in merged))
 for o in merged:o.hide_render=True;o.hide_set(True)
 return merged

# Main temple: layered roofs, generous open colonnade, gilded gables.
for z,w,l,h in [(0.13,20,24,.26),(.4,19.5,23.5,.28),(.73,19,23,.38)]:cube('Stepped stone terrace',(0,0,z),(w,l,h),stone,.055)
cube('Polished floor',(0,0,.91),(18.7,22.7,.08),white,.02)
for i in range(5):cube('Entrance stair',(0,-12-i*.48,.82-i*.16),(6.5,.52,.18),white,.035)
for x in [-7.6,7.6]:
 for y in [-9.4,-5.65,-1.9,1.9,5.65,9.4]:
  cube('Column footing',(x,y,1.14),(1.12,1.12,.46),white,.07)
  for zz,rr,hh in [(1.42,.5,.18),(1.59,.42,.15),(5.9,.45,.2),(6.11,.55,.22)]:cyl('Gilded column ring',(x,y,zz),rr,hh,gold,n=16)
  cyl('Ivory fluted column',(x,y,3.75),.34,4.25,white,r2=.29,n=16)
  for k in range(8):
   a=k*math.tau/8; tube('Column gold inlay',[(x+.342*math.cos(a),y+.342*math.sin(a),1.8),(x+.295*math.cos(a),y+.295*math.sin(a),5.7)],.015,gold,5)
  cube('Abacus',(x,y,6.35),(1.04,1.04,.22),palegold,.03)
 for y in [-9.4,9.4]:cube('Entablature',(0,y,6.5),(16.2,.6,.55),wood,.04)
 cube('Long decorated beam',(x,0,6.5),(.6,20,.55),wood,.04)
 for y in [-7.5,-3.8,0,3.8,7.5]:
  cube('Side balustrade',(x,y,1.55),(.35,2.9,1.2),white,.05)
  cube('Golden rail',(x,y,2.2),(.43,3.05,.12),gold,.02)
# back wall and central inner decorative frames
cube('Rear sanctuary wall',(0,10.5,3.6),(15,.28,5.3),wood,.04)
for x in [-5,-2.5,0,2.5,5]:
 cube('Rear inset',(x,10.32,3.6),(2.15,.1,4.5),dark,.03)
 for dx in [-1.12,1.12]:cube('Gilded frame',(x+dx,10.18,3.6),(.1,.14,4.7),gold,.02)
 for zz in [1.25,5.95]:cube('Gilded frame',(x,10.18,zz),(2.35,.14,.1),gold,.02)
# ceiling grid
for y in range(-9,11,2):cube('Teak ceiling beam',(0,y,6.6),(15.5,.2,.25),wood)

# tile meshes grouped by material avoid individual objects
for layer,(w,l,eave,peak) in enumerate([(9.6,23.4,6.75,12.4),(7.6,19.1,9.1,14.2),(5.35,14.5,11.65,15.8)]):
 def roofz(u):return peak-(peak-eave)*u**.82+.35*u**8
 # Continuous roof deck prevents tile seams or LOD simplification from opening the roof.
 for side in [-1,1]:
  vs=[];fs=[]
  for k in range(33):
   u=k/32
   for yy in [-l/2,l/2]:vs.append((side*w*u,yy,roofz(u)-.035))
  for k in range(32):fs.append((k*2,k*2+1,k*2+3,k*2+2))
  mesh('Continuous terracotta roof deck',vs,fs,roofm[0])
 # each slope's subdivided barrel tile faces
 for side in [-1,1]:
  tilevs=[[] for _ in roofm];tilefs=[[] for _ in roofm]
  nx=22;ny=58 if layer==0 else 46 if layer==1 else 36
  for ix in range(nx):
   for iy in range(ny):
    mi=random.randrange(len(roofm));vs=tilevs[mi];fs=tilefs[mi];base=len(vs)
    for a in range(2):
     u=(ix+a*1.035)/nx
     for b in range(4):
      yy=-l/2+(iy+b/3*.97)*l/ny
      vs.append((side*w*u,yy,roofz(u)+.055*math.sin(b/3*math.pi)))
    fs.extend([(base+j,base+j+1,base+j+5,base+j+4) for j in range(3)])
  for i,m in enumerate(roofm):mesh('Glazed overlapping roof tiles',tilevs[i],tilefs[i],m)
  for yy in [-l/2,l/2]:
   pts=[(side*w*j/32,yy,roofz(j/32)+.08) for j in range(33)]
   tube('Golden naga bargeboard',pts,.13,gold,8)
   tube('Bargeboard highlight',[(x,yy-.08,z+.17) for x,y,z in pts],.055,palegold,6)
   # regular flame ornaments tracing the roof edge
   for j in range(2,32,2):
    x=side*w*j/32;z=roofz(j/32);flame('Naga scales',x,yy,z+.16,.34)
   tube('Naga eave flourish',[(side*w,yy,eave+.4),(side*(w+.35),yy,eave+.55),(side*(w+.7),yy,eave+1.1),(side*(w+.73),yy,eave+1.9)], [.17,.13,.085,.003],palegold)
  tube('Eave gilding',[(side*w,-l/2,eave+.35),(side*w,l/2,eave+.35)],.12,gold)
 tube('Golden ridge',[(0,-l/2-.2,peak+.12),(0,l/2+.2,peak+.12)],.13,palegold,10)
 for yy,sgn in [(-l/2,-1),(l/2,1)]:
  tube('Chofa finial',[(0,yy,peak),(0,yy+sgn*.25,peak+.6),(0,yy+sgn*.65,peak+1.45),(0,yy+sgn*.45,peak+2.15)], [.18,.16,.08,.006],palegold,10)
 # front decorative gable below front roof, solid triangle only above beam
 gy=-l/2+.12
 vs=[(-w*.86,gy,eave+.45),(w*.86,gy,eave+.45),(0,gy,peak-.12)]
 mesh('Carved teak gable',vs,[(0,1,2)],wood)
 # mandala relief with scrolling golden stems within triangle
 gz=eave+.8;gh=peak-eave-1.2
 for ring in [0.38,.7,1.0]:
  pts=[]
  for j in range(49):
   a=j*math.tau/48;pts.append((math.sin(a)*ring*.7,gy-.06,gz+gh*.47+math.cos(a)*ring*gh*.34))
  tube('Gable lotus medallion',pts,.035,palegold,6)
 for sign in [-1,1]:
  for row in range(5):
   zz=gz+row*gh*.15;span=w*.76*(1-row*.16)
   pts=[]
   for j in range(30):
    t=j/29;pts.append((sign*(.2+t*span),gy-.08,zz+.35*math.sin(t*math.pi*3)))
   tube('Gable filigree',pts,.035,gold,6)
   for k in range(1,6):flame('Gable flame',sign*(.2+k*span/6),gy-.1,zz+.2,.25)
# low entrance naga rail sculptures (serpentine silhouettes)
for x in [-3.5,3.5]:
 pts=[(x,-10.9,1.65),(x,-11.7,1.55),(x,-12.6,1.1),(x,-13.5,.6),(x,-14.1,.75),(x,-14.3,1.4)]
 tube('Stair naga guardian',pts,[.16,.18,.2,.23,.2,.06],gold,12)
 for j in range(10):flame('Naga crest',x,-11-j*.31,1.75-j*.1,.26)
temple=export('temple',current);current=[]

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
# arms gesture
for side,pts in [(-1,[(-.54,0,2.42),(-.76,-.04,2.08),(-.8,-.23,1.61),(-.42,-.45,1.38),(0,-.43,1.35)]),(1,[(.54,0,2.42),(.77,-.05,2.02),(.85,-.22,1.52),(.76,-.47,1.03)])]:
 tube('Draped arm',pts,[.2,.18,.16,.1,.07] if side<0 else [.2,.18,.13,.085],gold,14)
 if side>0:
  sphere('Earth touching hand',(.74,-.5,.98),(.12,.06,.21),palegold,20,12)
  for k in range(4):tube('Fingers',[(.67+k*.042,-.544,.99),(.67+k*.042,-.55,.8+(k%2)*.02)],.016,gold,6)
 else:sphere('Meditation palm',(-.05,-.45,1.36),(.22,.13,.06),palegold)
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
buddha=export('buddha',current);current=[]

# Original coconut palm with feathered fronds and detailed ringed trunk.
pts=[(.55*math.sin(i/14*1.5),.08*math.sin(i/14*3),i/14*10.8) for i in range(15)]
tube('Curved palm trunk',pts,[.3*(1-i/30) for i in range(15)],bark,14)
for i in range(48):
 t=i/48;z=t*10.6; x=.55*math.sin(z/10.8*1.5); y=.08*math.sin(z/10.8*3)
 cyl('Trunk growth ring',(x,y,z),.304*(1-z/21.6),.035,stone,n=14)
origin=Vector(pts[-1])
for j in range(13):
 angle=j*math.tau/13; length=3.7+random.random()*1.3; arch=1.3+random.random()*.6;dir=Vector((math.cos(angle),math.sin(angle),0));cross=Vector((-dir.y,dir.x,0))
 def pos(t):return origin+dir*(length*t)+Vector((0,0,arch*math.sin(t*math.pi)-1.3*t))
 tube('Palm frond stem',[pos(k/20) for k in range(21)],[.052*(1-k/22) for k in range(21)],leafm[0],6)
 vs=[];fs=[]
 for k in range(1,30):
  t=k/31;center=pos(t);width=.78*(math.sin(t*math.pi)**.65)
  for s in [-1,1]:
   tip=center+cross*(s*width)+dir*.32+Vector((0,0,-.2-.2*t))
   mid=(center+tip)/2+Vector((0,0,.065));b=len(vs)
   vs.extend([tuple(center-dir*.055),tuple(mid-dir*.055),tuple(tip),tuple(mid+dir*.045),tuple(center+dir*.045)])
   fs.extend([(b,b+1,b+2,b+3,b+4)])
 mesh('Feathered palm leaves',vs,fs,leafm[j%3])
for j in range(6):
 a=j*math.tau/6;sphere('Coconut',tuple(origin+Vector((.3*math.cos(a),.3*math.sin(a),-.1))),(.18,.18,.23),leafm[0],12,8)
palm=export('palm',current);current=[]

# Garden lantern.
for z,w,h in [(.1,.8,.2),(.3,.6,.2),(1.25,.62,.13)]:cube('Lantern stone',(0,0,z),(w,w,h),white,.035)
cyl('Lantern stem',(0,0,.78),.16,.9,stone,r2=.13,n=8)
cube('Warm glass',(0,0,1.62),(.39,.39,.64),glow,.02)
for x in [-.25,.25]:
 for y in [-.25,.25]:cube('Lantern frame',(x,y,1.62),(.05,.05,.77),gold,.01)
for z in [1.3,1.93]:cube('Lantern lid',(0,0,z),(.64,.64,.1),gold,.02)
bpy.ops.mesh.primitive_cone_add(vertices=4,radius1=.53,radius2=0,depth=.4,location=(0,0,2.17),rotation=(0,0,math.pi/4));o=bpy.context.object;o.data.materials.append(gold);current.append(o)
flame('Lantern finial',0,0,2.36,.33)
lantern=export('lantern',current);current=[]

# Arrange a studio preview while keeping each exported model grounded at its origin.
for arr in [temple,buddha,palm,lantern]:
 for o in arr:o.hide_render=False;o.hide_set(False)
for o in buddha:o.location=(0,5,.96)
for o in palm:o.location=(-14,3,0)
for o in lantern:o.location=(-4,-15,0)
# duplicates purely for preview
for arr,loc in [(palm,(14,4,0)),(lantern,(4,-15,0))]:
 for o in arr:
  n=o.copy();n.data=o.data;bpy.context.collection.objects.link(n);n.location=loc
floor=mat('Preview ground',(.18,.21,.15),0,.95)
cube('Preview ground',(0,0,-.12),(120,120,.15),floor)
world=bpy.data.worlds.new('Warm sky');bpy.context.scene.world=world;world.use_nodes=True
world.node_tree.nodes.get('Background').inputs[0].default_value=(.36,.43,.55,1);world.node_tree.nodes.get('Background').inputs[1].default_value=.55
bpy.ops.object.light_add(type='AREA',location=(10,-15,25));bpy.context.object.data.energy=4500;bpy.context.object.data.shape='DISK';bpy.context.object.data.size=15
bpy.ops.object.light_add(type='SUN',location=(15,-15,20));bpy.context.object.rotation_euler=(.4,-.6,-.4);bpy.context.object.data.energy=3;bpy.context.object.data.angle=.15
bpy.ops.object.camera_add(location=(28,-38,19));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,7))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=42;bpy.context.scene.camera=cam
scene=bpy.context.scene
try:scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True
except:pass
scene.render.resolution_x=1400;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.filepath=SRC+'/temple-preview.png'
bpy.ops.wm.save_as_mainfile(filepath=SRC+'/sanctuary-assets.blend')
bpy.ops.render.render(write_still=True)
print('ALL_COMPLETE')


