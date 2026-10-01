#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
L=json.loads((R/"scripts"/"analysis_batch50i_cp20_lyrics.json").read_text(encoding="utf-8"))
MAP={
"C0273":{
0:["D","A7"],1:["D"],2:["D","G"],3:["D","A7","D"],4:["D","G","D"],5:["A7","D","D7"],
6:["D","A7"],7:["D"],8:["D","G"],9:["D","A7","D"]
},
"C0274":{
0:["C","G7","C"],1:["C","G7","C"],2:["C","G7","C","G7","C"],3:["F","G7","F","G7"],4:["C","G7","C"]
},
"C0275":{
0:["C","F","G7"],1:["C","G7","C"],2:["C","F","G7","C"],3:["C","G7"],4:["C","G7","C"],5:["C","G7"],6:["C","G7","C"],
7:["C","G7","C"],8:["G7","C"],9:["C","F","G7"],10:["C","G7","C"],11:["C","G7"],12:["C","G7","C"],13:["C","G7"],14:["C","G7","C"],15:["G7","C"],16:["G7","C"]
},
"C0277":{
0:["C","G7","C","G7","C"],1:["F","G7","C","F","G7","C"],2:["F","C"],3:["G7","C"],4:["C","G7"],5:["C"],7:["C","G7","C","G7"],8:["F","G7","C"],9:["C","G7","C","G7"],10:["F","G7","C"],11:["G7"],12:["G7","C"]
},
"C0278":{
0:["E","B7","E"],1:["A","B7","E"],2:["E","A","B7","E"],3:["A","B7","E"],6:["E","B7","E"],7:["A","B7","E"],8:["E","A","B7","E"],9:["A","B7","E"]
}
}
out={}
for cid,byline in MAP.items():
    lines=L[cid]["letra"].split("\n")
    out[cid]="\n".join("".join(f"[{c}]" for c in byline.get(i,[]))+line for i,line in enumerate(lines))
(R/"scripts"/"analysis_batch50i_cp20_candidates.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print("OK",len(out))
