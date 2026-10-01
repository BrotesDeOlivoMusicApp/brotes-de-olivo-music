#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
L=json.loads((R/"scripts"/"analysis_batch50i_cp10_lyrics.json").read_text(encoding="utf-8"))
MAP={
"C0262":{
0:["Dm","C","Gm","A7","Dm"],1:["F","C","Bb","Am","Dm"],2:["Bb","A7","Dm"],3:["Gm","A7","Dm"],
4:["F","C","F","C"],5:["Bb","A7","Dm"],6:["Dm","A7","Dm","A7"],7:["F","C","Gm","A7"],
8:["Dm","A7","Dm","A7"],9:["F","C","Gm","A7"],10:["Dm","A7","Dm","A7"],11:["F","C","Bb","A7"],
12:["Dm","C","F","Bb","Am","Dm"],13:["Bb","A7","Gm","Dm"],14:["Bb","Gm","A7","Dm"],15:["Dm","C","F","C"],16:["Bb","Gm","A7","Dm"],17:["Bb","Gm","A7","Dm"]
},
"C0264":{
0:["C","Am"],1:["C","Am"],2:["Dm","E7","Am"],3:["F","C","D","Am","G"],4:["C","Am"],5:["C","Am","C","Em","F"],
6:["C","Dm"],7:["Em","Am","F","G"],8:["C","Dm"],9:["Em","Am","F","G","F","G"],
10:["C","Dm"],11:["Em","Am","F","G"],12:["C","Dm"],13:["Em","Am","F","G","F","G"]
},
"C0266":{
0:["Cm","G","Cm","G","Cm","Eb"],1:["Bb","Cm","Bb","Cm","G","Cm"],2:["Cm","G","Cm","G","Cm","Eb"],3:["Bb","Cm","Bb","Cm","G","Cm"],
4:["Cm","Bb","Cm","Bb","Cm","C7"],5:["Fm","Cm","G","Cm"],
6:["Cm","G","Cm","G","Cm","Eb"],7:["Bb","Cm","Bb","Cm","G","Cm"],8:["Cm","G","Cm","G","Cm","Eb"],9:["Bb","Cm","Bb","Cm","G","Cm"]
},
"C0267":{
10:["G","C","D","G","C","D","G"],11:["G","C","D","G","C","D","G"]
}
}
out={}
for cid,byline in MAP.items():
    lines=L[cid]["letra"].split("\n")
    out[cid]="\n".join("".join(f"[{c}]" for c in byline.get(i,[]))+line for i,line in enumerate(lines))
(R/"scripts"/"analysis_batch50i_cp10_candidates.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print("OK",len(out))
