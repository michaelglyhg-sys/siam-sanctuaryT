from pathlib import Path
root=Path(r'C:/Users/123/Desktop/阿瑜陀耶/temple-sanctuary')
s=(root/'art-source/generate_assets.py').read_text(encoding='utf-8-sig')
prefix=s[:s.index('# Main temple:')]
prefix=prefix.replace("bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);merged.append(o)","bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);mod=o.modifiers.new('Web surface reduction','DECIMATE');mod.ratio=.42;bpy.ops.object.modifier_apply(modifier=mod.name);merged.append(o)")
seated=s[s.index('# Seated Buddha'):s.index('# Original coconut')]
a=seated.index('# arms gesture');b=seated.index('# Sculpt anatomical')
seated=seated[:a]+'''# Both palms rest together in the lap, dhyana pose.
for side in [-1,1]:
 tube('Draped arm',[(side*.54,0,2.42),(side*.77,-.04,2.02),(side*.75,-.25,1.63),(side*.38,-.47,1.38),(side*.06,-.5,1.4)],[.2,.18,.14,.10,.07],gold,14)
 sphere('Meditation palm',(side*.09,-.5,1.4+side*.035),(.2,.12,.065),palegold)
''' +seated[b:]
seated=seated.replace("buddha=export('buddha',current)","meditation=export('buddha-meditation',current)")
walking='''
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
'''
end='''
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
'''
(root/'art-source/generate_supplemental.py').write_text(prefix+seated+walking+end,encoding='utf8')
