#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
L=json.loads((R/"scripts"/"analysis_batch30g_lyrics.json").read_text(encoding="utf-8"))
MAP={
"C0220":{
0:["C","Am","F","G7"],1:["C","Am","F","G7"],2:["F","C","D7","G7"],3:["F","C","D7","G7"],
4:["C","G7","Am","D7","G7"],5:["F","C","D7","G7"],6:["F","C","D7","G7"],
7:["C","G7","Am","D7","G7"],8:["C","G7","Am","D7","G7"]
},
"C0221":{
0:["Dm","D7","Gm","Dm"],1:["A7","Dm","A7","Dm"],2:["A7","Dm","A7","Dm"],
3:["Dm","D7","Gm","Dm"],4:["A7","Dm","A7","Dm"],5:["Dm","D7","Gm","Dm"],
6:["A7","Dm","A7","Dm"],7:["Dm","D7","Gm","Dm"],8:["A7","Dm","A7","Dm"]
},
"C0224":{
0:["D","A7","G","A7","D","G"],1:["D","D7","G","D","G","D","A7","D","G"],
2:["D","A7","G","A7","D","G"],3:["D","D7","G","D","G","D","A7","D"],
4:["D","A7","G","A7","D","G"],5:["D","D7","G","D","G","D","A7","D"]
},
"C0225":{
0:["Am","E7","Am","F","G","C","G","C"],1:["F","G","Am","F","E7","Am"],
2:["Am","E7","Am","F","G","C","G","C"],3:["F","G","Am","F","E7","Am"],
4:["Am","C","F"],5:["Dm","G","Am"],6:["Am","C","F"],
7:["Dm","Am","C","F","G","C","C7","F","G","Am"],
8:["Am","E7","Am","F","G","C","G","C"],9:["F","G","Am","F","E7","Am"],
10:["Am","E7","Am","F","G","C","G","C"],11:["F","G","Am","F","E7","Am"]
},
"C0227":{
0:["Dm"],1:["Bb","Gm","C","Dm"],2:["Dm","F"],3:["Bb","A7"],
4:["Dm","F"],5:["Bb","Gm","C","Dm"],6:["Dm"],7:["Bb","Gm","C","Dm"],
8:["Dm","F"],9:["Bb","A7"],10:["Dm","F"],11:["Bb","Gm","C","Dm"]
},
"C0228":{
0:["G","C","G","C","D","G"],1:["Em","C","D"],2:["Em","Bm","C","G"],3:["D","A7","C","D"],
4:["G","C","G","C","D"],5:["G","C","D","C","G","D","G"],
6:["G","C","G","C","D"],7:["C","G","C","D","G"],
8:["G","C","G","C","D","G"],9:["Em","C","D"],10:["Em","Bm","C","G"],11:["D","A7","C","D"]
},
"C0229":{
0:["Am","C","D","F"],1:["Am","C","D","E"],2:["Am","G","F","E"],3:["Am","G","E","Am"],
4:["Am","C","D","F"],5:["Am","C","D","E"],6:["Am","C","D","F"],7:["Am","C","G","Am"],
8:["Am","C","D","F"],9:["Am","C","D","E"],10:["Am","G","F","E"],11:["Am","G","E","Am"]
}
}
out={}
for cid,byline in MAP.items():
    lines=L[cid]["letra"].split("\n")
    rendered=[]
    for i,line in enumerate(lines):
        rendered.append("".join(f"[{c}]" for c in byline.get(i,[]))+line)
    out[cid]="\n".join(rendered)
(R/"scripts"/"analysis_batch30g_candidates.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print("OK",len(out))
