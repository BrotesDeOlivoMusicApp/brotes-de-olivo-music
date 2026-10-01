#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
L=json.loads((R/"scripts"/"analysis_batch50h_lyrics.json").read_text(encoding="utf-8"))
MAP={
"C0240":{
0:["Am","E7","Am","F","C","E","A7"],1:["Dm","G","C","Am","Dm","E7","Am","E"],
2:["Am","A7","Dm","G"],3:["C","Dm","F","E7"],4:["Am","A7","Dm","E7","Am","E"],
5:["Am","E7","Am"],6:["F","C","E","A7"],7:["Dm","G","C","Am","Dm","E7","Am","E"]
},
"C0242":{
0:["Am","C","Am"],1:["F","G","Am"],2:["Am"],3:["F","G","Am"],
4:["Am"],5:["A"],6:["Am"],7:["A"],
8:["Dm","Em","F"],9:["Em"],10:["Dm","Em","F"],11:["G","Em","Am"],
12:["Am"],13:["A"],14:["Am"],15:["A"],16:["Dm","Em","F"],17:["G","Dm"]
},
"C0244":{
0:["D","D9","G"],1:["D","D9","G","D","G"],2:["Bm","A","D"],3:["C#dim","B","A","B"],
4:["D","D9","G"],5:["D","D9","G"],6:["D","D9","G"],7:["D","D9","G"],
8:["D","D9","G"],9:["D","D9","G"],10:["D","F#m","G"]
},
"C0246":{
0:["D","A","Bm","G","Em","A"],1:["D","A","Bm","G","Em","A"],2:["G","A","D","G","Em","A"],3:["G","A","D","Bm","G","A","D"],
4:["D","A","Bm","G","A","D","B7","Em"],5:["G","A","Em","A"],6:["D","A","Bm","G","A","D","B7","Em"],7:["G","A","D","Bm","A","D"],
8:["D","A","Bm","G","Em","A"],9:["D","A","Bm","G","Em","A"],10:["G","A","D","G","Em","A"],11:["G","A","D","Bm","G","A","D"],
12:["D","A","Bm","G","A","D","B7","Em"],13:["G","A","Em","A","F#m","G","A"],14:["D","A","Bm","G","A","D","B7","Em"],15:["G","A","F#m","Bm","Em","A","D","G","A"],
16:["F#m","Bm","Em","A","D","G","Em","A"],17:["F#m","Bm","G","A","F#m","Bm","G","A"],18:["D","Bm","Em","A","D","G","Em","A"],19:["F#m","Bm","G","A","D","Bm","Em","A"]
},
"C0248":{
0:["Am","G","F","E"],1:["Am","G","F","Am"],2:["Dm","E","Am","G"],3:["F","E","Dm","Am","A7"]
}
}
out={}
for cid,byline in MAP.items():
    lines=L[cid]["letra"].split("\n")
    out[cid]="\n".join("".join(f"[{c}]" for c in byline.get(i,[]))+line for i,line in enumerate(lines))
(R/"scripts"/"analysis_batch50h_cp40_candidates.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print("OK",len(out))
