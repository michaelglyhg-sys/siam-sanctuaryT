from pathlib import Path
p=Path('art-source/generate_reference_visitors.py').read_text(encoding='utf-8')
details=''' # Close-view sculpting: facial contours, textile relief and chased ornaments.
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
'''
p=p.replace(' # Merge detail meshes by parent/material',details+' # Merge detail meshes by parent/material')
p=p.replace("name='visitor-female' if female else 'visitor-male'","name='visitor-female-refined' if female else 'visitor-male-refined'")
p=p.replace('reference-visitors.blend','reference-visitors-refined.blend').replace('reference-visitors-preview.png','reference-visitors-refined-preview.png')
p += "\ncam.location=(0,-6,1.55);cam.rotation_euler=(Vector((0,0,1.48))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.35;scene.render.filepath=str(SRC/'reference-visitors-refined-closeup.png');bpy.ops.render.render(write_still=True)\n"
Path('art-source/generate_refined_visitors.py').write_text(p,encoding='utf-8')
