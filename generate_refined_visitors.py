import bpy, math, json
from mathutils import Vector
from pathlib import Path
ROOT=Path(r'C:/Users/123/Desktop/阿瑜陀耶/temple-sanctuary');OUT=ROOT/'public/assets';SRC=ROOT/'art-source'
bpy.ops.wm.read_factory_settings(use_empty=True)
def mat(n,c,metal=0,rough=.5):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
skin=mat('Warm porcelain skin',(.72,.405,.27),0,.52);ivory=mat('Ivory silk',(.9,.83,.68),0,.6);gold=mat('Embossed gold',(.73,.42,.09),.65,.3);hair=mat('Ink brown hair',(.035,.018,.018),0,.46);white=mat('Eye whites',(.98,.96,.9),0,.36);iris=mat('Amber brown iris',(.23,.085,.025),0,.3);black=mat('Pupil and lash',(.008,.004,.006),0,.35);lip=mat('Soft rose lip',(.51,.13,.12),0,.55);blue=mat('Midnight blue silk',(.025,.06,.15),0,.62);red=mat('Burgundy silk',(.28,.025,.05),0,.6);shoe=mat('Cream shoes',(.43,.3,.19),0,.75)
current=[];nodes={}
def bind(o,p):
 bpy.context.view_layer.update();w=o.matrix_world.copy();o.parent=p;o.matrix_world=w;current.append(o);return o
def node(n,pos,parent=None):
 o=bpy.data.objects.new(n,None);bpy.context.collection.objects.link(o);o.location=pos
 if parent:
  bpy.context.view_layer.update();w=o.matrix_world.copy();o.parent=parent;o.matrix_world=w
 current.append(o);nodes[n]=o;return o
def uv(n,pos,sc,m,p,seg=20,rings=12):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=rings,location=pos);o=bpy.context.object;o.name=n;o.scale=sc;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m)
 for f in o.data.polygons:f.use_smooth=True
 return bind(o,p)
def mesh(n,v,f,m,p):
 d=bpy.data.meshes.new(n);d.from_pydata(v,[],f);d.update();o=bpy.data.objects.new(n,d);bpy.context.collection.objects.link(o);o.data.materials.append(m)
 for q in d.polygons:q.use_smooth=True
 return bind(o,p)
def tube(n,pts,r,m,p,s=8):
 v=[];f=[]
 for i,pt in enumerate(pts):
  t=(Vector(pts[min(i+1,len(pts)-1)])-Vector(pts[max(i-1,0)])).normalized();a=t.cross(Vector((0,1,0))).normalized();b=t.cross(a).normalized();rr=r[i] if isinstance(r,list) else r
  for j in range(s):v.append(tuple(Vector(pt)+rr*(a*math.cos(j*math.tau/s)+b*math.sin(j*math.tau/s))))
 for i in range(len(pts)-1):
  for j in range(s):a=i*s+j;b=i*s+(j+1)%s;f.append((a,b,b+s,a+s))
 f+=[tuple(range(s-1,-1,-1)),tuple((len(pts)-1)*s+j for j in range(s))];return mesh(n,v,f,m,p)
def body(n,rings,m,p,segments=32,start=0,end=math.tau):
 v=[];f=[]
 for z,rx,ry in rings:
  for i in range(segments+1):
   a=start+(end-start)*i/segments;v.append((rx*math.cos(a),ry*math.sin(a),z))
 for k in range(len(rings)-1):
  for i in range(segments):a=k*(segments+1)+i;f.append((a,a+1,a+segments+2,a+segments+1))
 f += [tuple(range(segments,-1,-1)),tuple((len(rings)-1)*(segments+1)+j for j in range(segments+1))];return mesh(n,v,f,m,p)
def band(n,z,rx,ry,thick,m,p):return body(n,[(z-thick/2,rx,ry),(z+thick/2,rx,ry)],m,p)
def diamond(n,x,y,z,size,p):tube(n,[(x,y,z+size),(x+size*.55,y,z),(x,y,z-size),(x-size*.55,y,z),(x,y,z+size)],.0025,gold,p,5)
def make(female):
 global current,nodes
 current=[];nodes={};name='visitor-female-refined' if female else 'visitor-male-refined';root=node('Visitor',(0,0,0));upper=node('Upper',(0,0,.91),root);head=node('Head',(0,0,1.40),upper)
 uv('Neck',(0,0,1.395),(.065,.066,.105),skin,upper)
 body('Tailored silk jacket',[(.88,.175,.12),(1.0,.155,.115),(1.16,.18,.125),(1.29,.205,.12),(1.34,.15,.09),(1.38,.065,.065)],ivory,upper)
 band('Gold standing collar',1.38,.071,.071,.035,gold,upper)
 band('Waist belt',.93,.182,.128,.045,gold,upper)
 uv('Lotus buckle',(0,-.137,.93),(.043,.015,.042),gold,upper,16,10)
 for side in [-1,1]:
  tube('Diagonal silk embroidery',[(side*.16,-.091,1.32),(side*.075,-.13,1.15),(0,-.123,.96)],.008,gold,upper)
  for j in range(5):diamond('Brocade diamond',side*(.04+(j%2)*.055),-.127,1.02+j*.055,.015,upper)
 # Smooth oval face, large inset eyes; dark hair shell stays behind forehead.
 uv('Face',(0,-.012,1.57),(.178,.147,.205),skin,head,32,24)
 # Continuous cap with a shaped forehead hairline, instead of intersecting locks.
 hv=[];hf=[]
 for row in range(14):
  for j in range(40):
   a=j*math.tau/40;front=max(0,-math.sin(a));back=max(0,math.sin(a));limit=1.50-.50*front+.48*back;theta=.025+(limit-.025)*row/13
   hv.append((.185*math.sin(theta)*math.cos(a),.015+.151*math.sin(theta)*math.sin(a),1.59+.205*math.cos(theta)))
 for row in range(13):
  for j in range(40):a=row*40+j;b=row*40+(j+1)%40;hf.append((a,b,b+40,a+40))
 mesh('Sculpted swept hair cap',hv,hf,hair,head)
 for side in [-1,1]:
  for j in range(5):
   x=side*(.035+j*.025);tube('Swept fringe',[(side*.01,-.075,1.774),(x*.7,-.12,1.755),(x,-.123+j*.006,1.715-j*.009)],[.018,.021,.012],hair,head,8)
 for side in [-1,1]:
  uv('Ear',(side*.176,-.005,1.56),(.033,.029,.054),skin,head)
  uv('Eye white',(side*.069,-.143,1.593),(.047,.012,.035),white,head)
  uv('Amber iris',(side*.069,-.154,1.592),(.024,.008,.03),iris,head)
  uv('Pupil',(side*.069,-.161,1.594),(.012,.004,.022),black,head,16,12)
  uv('Eye sparkle',(side*.063,-.165,1.608),(.007,.003,.008),white,head,12,8)
  tube('Upper lashes',[(side*.025,-.151,1.604),(side*.065,-.162,1.628),(side*.108,-.145,1.61)],.0045,black,head)
  tube('Soft eyebrow',[(side*.026,-.14,1.656),(side*.066,-.15,1.666),(side*.107,-.132,1.65)],.007,hair,head)
  uv('Earring',(side*.185,-.016,1.515),(.013,.014,.014),gold,head,12,8)
  if female:
   tube('Pendant earring',[(side*.185,-.016,1.51),(side*.19,-.02,1.46),(side*.185,-.016,1.43)],[.008,.018,.001],gold,head)
 uv('Small nose',(0,-.161,1.553),(.019,.023,.027),skin,head)
 tube('Soft smile',[(-.035,-.149,1.505),(0,-.159,1.497),(.035,-.149,1.505)],.004,lip,head)
 if female:
  uv('High braided bun',(0,.043,1.817),(.105,.096,.095),hair,head,28,18)
  band('Bun gold circlet',1.80,.116,.104,.023,gold,head)
  uv('Forehead jewel',(0,-.098,1.816),(.017,.012,.026),gold,head,16,10)
 else:
  for z,r in [(1.805,.098),(1.834,.083),(1.86,.065)]:band('Tiered crown',z,r,r,.018,gold,head)
  body('Crown spire',[(1.86,.055,.055),(1.90,.036,.036),(2.025,.002,.002)],gold,head,20)
  for j in range(8):
   a=j*math.tau/8;tube('Crown petal',[(.08*math.cos(a),.08*math.sin(a),1.83),(.085*math.cos(a),.085*math.sin(a),1.89),(.047*math.cos(a),.047*math.sin(a),1.865)],[.009,.002,.005],gold,head)
 # Relaxed arms, downward local axes. Character left = +X in glTF.
 for side,suffix in [(-1,'L'),(1,'R')]:
  shoulder=(side*.203,0,1.29);elbow=(side*.263,-.008,1.075);wrist=(side*.275,-.025,.875)
  arm=node('Arm'+suffix,shoulder,upper);fore=node('Forearm'+suffix,elbow,arm);hand=node('Hand'+suffix,wrist,fore)
  uv('Rounded shoulder',shoulder,(.072,.076,.078),ivory,arm)
  tube('Sleeve',[(side*.203,0,1.29),(side*.24,-.005,1.16),(side*.257,-.007,1.10)],[.069,.061,.052],ivory,arm,16)
  tube('Sleeve gold hem',[(side*.252,-.007,1.12),(side*.257,-.007,1.10)],[.058,.056],gold,arm,16)
  uv('Elbow joint',elbow,(.048,.048,.05),ivory if female else skin,fore)
  tube('Forearm',[(side*.263,-.008,1.075),(side*.272,-.02,.94),wrist],[.048,.038,.031],ivory if female else skin,fore,16)
  tube('Gold wrist cuff',[(side*.274,-.024,.903),wrist],[.036,.034],gold,fore,16)
  uv('Palm',(side*.277,-.028,.833),(.037,.023,.047),skin,hand)
  for j in range(4):
   x=side*(.251+j*.017);tube('Finger',[(x,-.028,.82),(x,-.031,.765+abs(j-1.5)*.009)],[.009,.006],skin,hand,8)
  tube('Thumb',[(side*.249,-.029,.846),(side*.231,-.043,.807)],[.012,.008],skin,hand,10)
  hip=node('Hip'+suffix,(side*.086,0,.88),root);knee=node('Knee'+suffix,(side*.086,0,.48),hip)
  tube('Upper leg',[(side*.086,0,.86),(side*.086,0,.48)],[.065,.049],skin,hip,12)
  tube('Lower leg',[(side*.086,0,.48),(side*.086,0,.105)],[.049,.035],skin,knee,12)
  uv('Shoe',(side*.086,-.044,.055),(.061,.117,.055),ivory if female else shoe,knee)
  tube('Shoe gold piping',[(side*.13,-.10,.09),(side*.086,-.13,.092),(side*.043,-.10,.09)],.004,gold,knee)
 skirt=node('Skirt',(0,0,.9),root)
 body('Woven wrap skirt',[(.16,.175,.125),(.36,.178,.13),(.68,.184,.14),(.9,.176,.13)],red if female else blue,skirt,40)
 if not female:body('Ivory wrap panel',[(.18,.178,.129),(.68,.188,.145),(.9,.18,.134)],ivory,skirt,18,math.pi,math.pi*1.5)
 for z in [.18,.205,.245,.29]:band('Hem gold woven band',z,.18,.132,.009,gold,skirt)
 # Repeating woven diamond relief, deliberately low geometry cost.
 for k in range(6):
  z=.34+k*.083
  for j in range(12):
   a=j*math.tau/12;rx=.184;ry=.143;x=rx*math.cos(a);y=ry*math.sin(a)
   pts=[]
   for da,dz in [(0,.027),(.08,0),(0,-.027),(-.08,0),(0,.027)]:pts.append((rx*math.cos(a+da),ry*math.sin(a+da),z+dz))
   tube('Woven diamond',pts,.0018,gold,skirt,4)
 # Decorative central fabric strip.
 mesh('Front sash',[(-.027,-.148,.88),(.027,-.148,.88),(.032,-.148,.34),(-.032,-.148,.34)],[(0,1,2,3)],ivory,skirt)
 for z in [.39+i*.055 for i in range(9)]:diamond('Sash motif',0,-.151,z,.02,skirt)
 # Close-view sculpting: facial contours, textile relief and chased ornaments.
 for side in [-1,1]:
  # Upper/lower skin rims surround the whites and soften the inset eye.
  for top in [True,False]:
   pts=[]
   for j in range(13):
    t=j*math.pi/12;x=side*.069+.047*math.cos(t);z=1.593+(.036 if top else -.030)*math.sin(t);y=-.146-.010*math.sin(t)
    pts.append((x,y,z))
   tube('Sculpted eyelid rim',pts,.0038,skin,head,6)
  tube('Lower lid crease',[(side*.03,-.144,1.557),(side*.065,-.154,1.551),(side*.103,-.139,1.560)],.0018,skin,head,6)
  # Ear helix with a distinct internal fold, attached to original head node.
  pts=[(side*(.177+.020*math.cos(t)),-.027-.007*math.sin(t),1.56+.043*math.sin(t)) for t in [j*math.tau/20 for j in range(21)]]
  tube('Outer ear helix',pts,.006,skin,head,7)
  tube('Ear antihelix',[(side*.182,-.033,1.586),(side*.169,-.038,1.571),(side*.184,-.035,1.544)],.004,skin,head,6)
  uv('Nose wing',(side*.015,-.169,1.54),(.012,.012,.009),skin,head,14,8)
  tube('Nostril contour',[(side*.009,-.179,1.534),(side*.017,-.178,1.533),(side*.023,-.17,1.536)],.0015,lip,head,5)
 # Cupid bow and fuller lower lip, with a quiet smile.
 tube('Upper lip cupid bow',[(-.035,-.151,1.505),(-.015,-.159,1.507),(0,-.16,1.503),(.015,-.159,1.507),(.035,-.151,1.505)],.0035,lip,head,7)
 tube('Lower lip plane',[(-.03,-.153,1.501),(0,-.162,1.494),(.03,-.153,1.501)],.004,lip,head,7)
 # Long swept hair strands follow the continuous hair cap, using subtle relief.
 for j in range(32):
  a=j*math.tau/32;front=max(0,-math.sin(a));back=max(0,math.sin(a));limit=1.50-.50*front+.48*back;pts=[]
  for k in range(10):
   theta=.16+(limit-.16)*k/9;aa=a+.12*(1-k/9)
   pts.append((.187*math.sin(theta)*math.cos(aa),.015+.153*math.sin(theta)*math.sin(aa),1.59+.207*math.cos(theta)))
  tube('Fine swept hair ridge',pts,.0019,hair,head,5)
 if female:
  for j in range(22):
   a=j*math.tau/22;pts=[]
   for k in range(12):
    t=.12+(math.pi-.24)*k/11;aa=a+.18*math.sin(t);pts.append((.106*math.sin(t)*math.cos(aa),.043+.097*math.sin(t)*math.sin(aa),1.817+.095*math.cos(t)))
   tube('Coiled bun strand',pts,.002,hair,head,5)
 # Fine standing collar piping and chased leaf motif.
 for z in [1.367,1.393]:band('Collar beaded edge',z,.074,.074,.0035,gold,upper)
 for j in range(14):
  a=j*math.tau/14;pts=[(.074*math.cos(a+da),.074*math.sin(a+da),1.38+dz) for da,dz in [(0,.009),(.09,0),(0,-.009),(-.09,0),(0,.009)]]
  tube('Collar chased leaf',pts,.0018,ivory,upper,5)
 for side,suffix in [(-1,'L'),(1,'R')]:
  arm=nodes['Arm'+suffix];fore=nodes['Forearm'+suffix];hand=nodes['Hand'+suffix]
  for j in range(4):
   # Narrow silk folds with taper, same material to keep draw count unchanged.
   x=side*(.212+j*.012)
   tube('Sleeve gathered fold',[(x,-.066,1.275),(x+side*.016,-.064,1.22),(x+side*.026,-.057,1.14)],[.002,.003,.001],ivory,arm,5)
  if female:
   for j in range(3):
    tube('Wrist silk gathering',[(side*(.25+j*.013),-.052,1.04),(side*(.255+j*.013),-.052,.97),(side*(.258+j*.013),-.05,.915)],[.002,.003,.001],ivory,fore,5)
  for j in range(4):
   x=side*(.251+j*.017);z=.792+abs(j-1.5)*.005
   tube('Finger knuckle crease',[(x-.006,-.037,z),(x,-.039,z-.001),(x+.006,-.037,z)],.0012,skin,hand,5)
   uv('Finger nail',(x,-.036,.773+abs(j-1.5)*.009),(.0047,.001,.006),skin,hand,10,6)
  # Chest seam and softly gathered waist.
  for j in range(4):
   x=side*(.06+j*.024)
   tube('Waist fabric pleat',[(x,-.119,.958),(x+side*.008,-.123,1.015),(x+side*.015,-.118,1.08)],[.001,.003,.001],ivory,upper,5)
 # Filigree rosette on belt, embossed concentric petal loops.
 for j in range(10):
  a=j*math.tau/10;pts=[]
  for k in range(9):
   t=k*math.tau/8;r=.018+.009*math.cos(t);aa=a+.17*math.sin(t);pts.append((r*math.cos(aa),-.154,.93+r*math.sin(aa)))
  tube('Buckle filigree petal',pts,.0018,ivory,upper,5)
 uv('Buckle central jewel',(0,-.154,.93),(.009,.005,.009),gold,upper,14,8)
 # Fine embossed hem lattice between existing gold bands.
 for j in range(36):
  a=j*math.tau/36
  for center,size in [(.223,.014),(.267,.017)]:
   pts=[(.181*math.cos(a+da),.134*math.sin(a+da),center+dz) for da,dz in [(0,size),(.04,0),(0,-size),(-.04,0),(0,size)]]
   tube('Woven hem lattice',pts,.0015,gold,skirt,4)
 for j in range(16):
  a=j*math.tau/16;pts=[]
  for k in range(9):
   z=.32+k*.065;rx=.179+.006*math.sin(k*math.pi/8);ry=.134+.009*math.sin(k*math.pi/8)
   pts.append((rx*math.cos(a),ry*math.sin(a),z))
  tube('Silk vertical fold',pts,[.001,.002,.0025,.003,.003,.0025,.002,.0015,.001],red if female else blue,skirt,5)
 # Merge detail meshes by parent/material, preserving every articulation pivot.
 for parent in list(nodes.values()):
  groups={}
  for o in list(bpy.data.objects):
   if o.type=='MESH' and o.parent==parent:groups.setdefault(o.data.materials[0].name,[]).append(o)
  for material,group in groups.items():
   bpy.ops.object.select_all(action='DESELECT')
   for o in group:o.select_set(True)
   bpy.context.view_layer.objects.active=group[0];bpy.ops.object.join();o=bpy.context.object;o.name=parent.name+' '+material
 bpy.ops.object.select_all(action='DESELECT')
 def select_tree(o):
  o.select_set(True)
  for c in o.children:select_tree(c)
 select_tree(root)
 bpy.ops.export_scene.gltf(filepath=str(OUT/(name+'.glb')),export_format='GLB',use_selection=True,export_yup=True)
 return root
male=make(False)
# Hide first figure during creation, avoid automatic numerical suffixes for joint names.
for o in bpy.data.objects:o.name='MalePreview_'+o.name
female=make(True)
male.location.x=-.42;female.location.x=.42
scene=bpy.context.scene
bpy.ops.object.camera_add(location=(3,-7,2.7));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,1.02))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=2.8;scene.camera=cam
for loc,power,size in [((0,-4,5),550,4),((-3,-1,3),350,3),((2,2,4),650,3)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
scene.world=bpy.data.worlds.new('Warm studio');scene.world.use_nodes=True;scene.world.node_tree.nodes.get('Background').inputs[0].default_value=(.22,.25,.3,1)
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=1200;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
bpy.ops.wm.save_as_mainfile(filepath=str(SRC/'reference-visitors-refined.blend'));scene.render.filepath=str(SRC/'reference-visitors-refined-preview.png');bpy.ops.render.render(write_still=True)


cam.location=(0,-6,1.55);cam.rotation_euler=(Vector((0,0,1.48))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.35;scene.render.filepath=str(SRC/'reference-visitors-refined-closeup.png');bpy.ops.render.render(write_still=True)
