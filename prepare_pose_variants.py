from pathlib import Path
p=Path('art-source/generate_supplemental.py').read_text(encoding='utf-8')
prefix=p.split('# Seated Buddha')[0]
seated=p[p.index('# Seated Buddha'):p.index('# Flowing standing/walking')]
start=seated.index('# Both palms')
end=seated.index('# Sculpt anatomical')
seated=seated[:start]+'''# Teaching gesture: left palm in lap, right hand before chest.
tube('Draped arm',[(-.54,0,2.42),(-.77,-.04,2.02),(-.75,-.25,1.63),(-.38,-.47,1.38),(-.06,-.5,1.4)],[.2,.18,.14,.10,.07],gold,14)
sphere('Meditation palm',(-.09,-.5,1.4),(.2,.12,.065),palegold)
tube('Draped arm',[(.54,0,2.42),(.78,-.05,2.07),(.68,-.38,1.92),(.45,-.54,2.21)],[.2,.16,.13,.08],gold,14)
sphere('Teaching palm',(.44,-.55,2.31),(.12,.06,.13),palegold)
# Thumb and index form a visible circle; three fingers rise beside it.
tube('Teaching finger circle',[(.39+.066*math.cos(t),-.58,2.43+.066*math.sin(t)) for t in [i*math.tau/20 for i in range(21)]],.018,palegold,8)
for j in range(3):tube('Teaching raised fingers',[(.46+j*.045,-.55,2.35),(.48+j*.045,-.56,2.58-j*.025)],.018,palegold,8)
''' + seated[end:]
seated=seated.replace("meditation=export('buddha-meditation'","teaching=export('buddha-teaching'")
walking=p[p.index('# Flowing standing/walking'):p.index('# Guardian yaksha')]
walking=walking.replace('y=-.19 if side<0 else .13','y=0')
reassurance=walking.replace("walking=export('buddha-walking'","reassurance=export('buddha-reassurance'")
standing=walking
start=standing.index("tube('Draped arm',[(.45")
end=standing.index('for j in range(13)',start)
standing=standing[:start]+'''tube('Draped arm',[(.45,0,2.6),(.62,-.05,2.2),(.6,-.13,1.79)],[.14,.12,.07],gold,14)
sphere('Lowered hand',(.6,-.13,1.66),(.08,.06,.16),palegold)
'''+standing[end:]
standing=standing.replace("walking=export('buddha-walking'","standing=export('buddha-standing'")
preview=p[p.index('for group in [meditation,walking,guardian]'):]
preview=preview.replace('[meditation,walking,guardian]','[teaching,reassurance,standing]').replace('for o in meditation:','for o in teaching:').replace('for o in guardian:','for o in standing:').replace('supplemental-sculptures','buddha-pose-variants')
Path('art-source/generate_pose_variants.py').write_text(prefix+seated+reassurance+standing+preview,encoding='utf-8')
