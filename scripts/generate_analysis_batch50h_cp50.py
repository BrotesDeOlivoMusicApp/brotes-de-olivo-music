#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
L=json.loads((R/"scripts"/"analysis_batch50h_lyrics.json").read_text(encoding="utf-8"))
MAP={
"C0250":{
0:["Am","G","D","F"],1:["Am","G","D","F"],2:["Am","G","D","F"],3:["Am","G","D","F"],
4:["F","G","Em","Am"],5:["F","G","Em","Am"],6:["F","G","Em","Am"],7:["F","G","Em","D"],
8:["Am","G","D","F"],9:["Am","G","D","F"],10:["Am","G","D","F"],11:["Am","G","D","F"],
12:["F","G","Em","Am"],13:["F","G","Em","Am"],14:["F","G","Em","Am"],15:["F","G","Em","Am"]
},
"C0252":{
0:["F","C","Em","Am"],1:["Em","Am","D","G","F"],2:["C","F","Dm","A7","Dm"],3:["C","F","G","C","F"],
4:["F","C","Em","Am"],5:["Em","Am","D","G","F"],6:["C","F","Dm","A7","Dm"],7:["Dm","C","F","G","C","F"],
8:["A#","Am","Em","Am"],9:["A#","Am","Em","Am"],10:["A#","F","Em","Am"],11:["Em","F","Dm","G","C"],
12:["F","C","Em","Am","Em"],13:["Am","Em","D","G","C","F","C"],14:["F","Dm","Em","A7","Dm"],15:["C","F","G","C","F"]
},
"C0254":{
0:["Am","A7","Dm","Am","E","Am"],1:["A7","Dm","Am","E","Am"],2:["E","Am","Dm7","G","C"],3:["E","Am","G","F","E","Am"],
4:["Am","A7","Dm","Am","E","Am"],5:[],6:["Am","A7","Dm","Am","E","Am"],7:["E","Am","Dm7","G","C"],8:["E","Am","G","F","E","Am"],
9:["Am","A7","Dm","Am","E","Am"],10:["A7","Dm","Am","E","Am"],11:["E","Am","Dm7","G","C"],12:["E","Am","G","F","E","Am"],13:["E","Am","Dm7","G","C"],14:["E","Am","G","F","E","Am"]
},
"C0256":{
0:["Em","Am","Em","Am"],1:["C","G","C","D"],2:["Em","Am","Em","Am"],3:["C","G","C","D"],
4:["F","Em","B7","Em"],5:["F","Em","B7","Em"],6:["F","Em","B7","C"],7:["F","Em","B7","Em","Am","B7","Em"],
8:["Em","Am","Em","Am"],9:["C","G","C","D"],10:["Em","Am","Em","Am"],11:["C","G","C","D"],
12:["F","Em","B7","Em"],13:["F","Em","B7","Em"],14:["F","Em","B7","Em"],15:["F","Em","B7","Em"]
},
"C0258":{
0:["Am","D","Am","F","G","Em","Am"],1:[],2:["Am","D","Am","F","G","Em","Am"],3:["F","G","Em","Am"],4:["F","G","Am"],
5:["C","A#","C","F","Dm","Em","F","G"],6:["C","Dm","C","Am","Em","F","G"],7:["C","F","C","F","G","C","F","E"],
8:["Am","F","G","C","G","Am","G","F","G","C"]
}
}
out={}
for cid,byline in MAP.items():
    lines=L[cid]["letra"].split("\n")
    out[cid]="\n".join("".join(f"[{c}]" for c in byline.get(i,[]))+line for i,line in enumerate(lines))
(R/"scripts"/"analysis_batch50h_cp50_candidates.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print("OK",len(out))
