#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
L=json.loads((R/"scripts"/"analysis_batch50h_lyrics.json").read_text(encoding="utf-8"))
MAP={
"C0230":{
0:["Am","G","F","G","Am"],1:["Am","G","F","G","Am"],2:["C","F","G","C"],3:["Am","F","G","Am"],
4:["Am","G","F","G","Am"],5:["Am","G","F","G","Am"],6:["C","F","G","C"],7:["Am","F","G","Am"]
},
"C0231":{
0:["C","Am","F","G"],1:["C","Am","F","G"],2:["F","G","F","G"],3:["F","G","F","G"],
4:["F","G","F","G"],5:["F","G","F","G"],6:["C"],7:["D","G"],8:["F","C","F","C"],9:["F","C","F","G"]
},
"C0232":{
0:["G","D","C","G"],1:["Em","Bm","A","C","D"],2:["G","C","Am","D"],3:["Bm","C","A7","D"],
4:["G","C","G","C","G"],5:["D","C","D"],6:["G","C","G","C","G"],7:["D","C","D","G"],
8:["G","D","C","G"],9:["Em","Bm","A","C","D"],10:["G","C","Am","D"],11:["Bm","C","A7","D"],
12:["G","C","G","C","G"],13:["D","C","D"],14:["G","C","G","C","G"],15:["D","C","D","G"]
},
"C0233":{
0:["Em","A7","Em","A7"],1:["D","C","G","D","C","Em"],2:["C","D","Em"],3:["C","D","Em"],
4:["C","D","Em"],5:["C","D","G","D","E"],6:["Em","A7","Em","A7"],7:["D","C","G","D","C","Em"],
8:["C","D","Em"],9:["C","D","Em"],10:["C","D","Em"],11:["C","D","G","D","E"]
},
"C0234":{
0:["Am","E7","Am","E7","Am","A7"],1:["Dm","Am","Dm","Am","F","E7","Am"],
2:["Am","E7","Am","E7","Am","A7"],3:["Dm","Am","Dm","Am","F","E7","Am"],
4:["E7","Dm","Am"],5:["E7","Dm","Am","F","Dm","E7","Am"],
6:["Am","E7","Am","E7","Am","A7"],7:["Dm","Am","Dm","Am","F","E7","Am"],
8:["Am","E7","Am","E7","Am","A7"],9:["Dm","Am","Dm","Am","F","E7","Am"],10:["Am","E7","Am"]
},
"C0235":{
0:["Am","G","C","E","Am"],1:["C","D","E"],2:["Am","E","Am","E","Am"],3:["Dm","E","F","E"],
4:["Am","Dm"],5:["E","F","E"],6:["Dm","Am"],7:["E","F","E","Am"],
8:["Am","G","C","E","Am"],9:["C","D","E"],10:["Am","E","Am","E","Am"],11:["Dm","E","F","E"]
},
"C0238":{
0:["F","Em","F","Em"],1:["F","E","Am","F","G","C"],2:["F","Em","F","Em"],3:["Dm","E","Am","F","G","C"],
4:["Am","G","Dm","C","E"],5:["Am","G","F","G","Am"],6:["Am","G","Dm","C","E"],7:["Am","G","F","E","Am"],
8:["F","C","Dm","Am"],9:["G","F","E","Am"],10:["F","C","Dm","Am"],11:["G","F","E","Am"],
12:["F","C","Dm","Am"],13:["G","F","E","Am"],14:["F","C","Dm","Am"],15:["G","F","E","Am","F","C","Dm","Am"]
}
}
out={}
for cid,byline in MAP.items():
    lines=L[cid]["letra"].split("\n")
    out[cid]="\n".join("".join(f"[{c}]" for c in byline.get(i,[]))+line for i,line in enumerate(lines))
(R/"scripts"/"analysis_batch50h_cp30_candidates.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print("OK",len(out))
