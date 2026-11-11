from pathlib import Path
p=Path('art-source/generate_reference_visitors.py');s=p.read_text(encoding='utf-8-sig')
s=s.replace("uv('Back hair',(0,.043,1.65),(.184,.128,.175),hair,head,28,18)","""# Continuous cap with a shaped forehead hairline, instead of intersecting locks.
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
   x=side*(.035+j*.025);tube('Swept fringe',[(side*.01,-.075,1.774),(x*.7,-.12,1.755),(x,-.123+j*.006,1.715-j*.009)],[.018,.021,.012],hair,head,8)""")
s=s.replace("  uv('Hair swept lock',(side*.105,-.045,1.737),(.09,.105,.067),hair,head,24,16).rotation_euler[1]=side*.35\n",'')
s=s.replace("(.047,.018,.035)","(.047,.012,.035)").replace("-.159,1.592","-.154,1.592").replace("-.166,1.594","-.161,1.594").replace("-.17,1.608","-.165,1.608")
p.write_text(s,encoding='utf-8')
