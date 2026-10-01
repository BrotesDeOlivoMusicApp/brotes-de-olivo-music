#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
L=json.loads((R/"scripts"/"analysis_batch20d_lyrics.json").read_text(encoding="utf-8"))
MAP={
"C0086":{
1:["D","A"],2:["G","Em","A","D"],3:["A","G","D","D7","G","A","D","D7"],4:["G","A","Bm","G","A","D"],5:["D","A"],6:["G","Em","A","D","G","D","G"],7:["A","G","D","D7","G","A","D","D7"],8:["G","A","Bm","G","A","D"]
},
"C0088":{
1:["D","G","D"],2:["G","D","Em","A"],3:["A","D","G"],4:["G","D","Em","A","D"],5:["D","G","A","D"]
},
"C0090":{
1:["G","D","Em"],2:["C","A","D"],3:["G","Em"],4:["C","A","D"],5:["G","Em","C","D","G","B7"],6:["Am","B7","Em","A"],7:["Am","B7","Em"],8:["Am","B7","Em","A"],9:["Am","C","D"]
},
"C0091":{
1:["Cm","G","Cm"],2:["Cm","Fm","Bb","Eb"],3:["C7","Fm","G","Cm"],4:["Ab","G","Cm"],5:["Cm","Fm","Bb","Eb"],6:["Ab","G","C7"],7:["Fm","Bb","Eb"],8:["Ab","G","Cm"],9:["C","G","Cm"],10:["Fm","Bb","Eb"],11:["Ab","G","Cm"],12:["Fm","G","Cm"]
},
"C0092":{
1:["C","G","C","G"],2:["Am","F","Dm","G"],3:["C","G","C","G"],4:["Am","G#","G"],5:["Cm","A#","G#","G"],6:["Fm","Cm","Fm","G"],7:["Cm","A#","Fm","G"],8:["Fm","Cm","G#","G"],9:["E","B","G#m"],10:["E","B","E","F#"],11:["B","F#","B","F#"],12:["E","Em","F#","B"]
},
"C0093":{
1:["C","F","C"],2:["C","F","G"],3:["F","C","F","C"],4:["C","F","G"],5:["C","F","C","G","C"],6:["C","F","E"],7:["F","C","Dm","Am"],8:["F","G","C"],9:["C","F","C"],10:["Em","F","C"],11:["F","C","F","Am"],12:["F","G","C"]
},
"C0094":{
1:["Dm","C"],2:["Bb","C"],3:["Dm","C"],4:["Bb","C","Dm"]
},
"C0095":{
1:["C","F"],2:["G","C"],3:["C","F"],4:["G","C"],5:["F","G","C"],6:["F","G","C"]
},
"C0097":{
1:["G","C","G"],2:["Em","Am","D"],3:["C","D","G"],4:["C","G","Am","D"],5:["C","D","Em"],6:["C","G"],7:["C","G"],8:["C","D","G"]
},
"C0098":{
1:["F","Bb","F"],2:["C","F"],3:["Bb","C","F"],4:["Bb","F"],5:["Bb","C"],6:["Bb","F"],7:["Bb","Gm","C"]
},
"C0099":{
1:["C","Dm","G","C"],2:["C","Em","F","G","C"],3:["G","F","C"],4:["Dm","G","C"],5:["F","G","C"],6:["Am","Dm","G","C"],7:["F","G","C"],8:["G","F","C"]
},
"C0100":{
1:["C","F","C","D","F","G"],2:["Em","F","C","G","C"],3:["C","G","F","C"],4:["C","G","F","C"],5:["F","G","C"],6:["C","G","F","C"]
},
"C0101":{
1:["D","G","D"],2:["G","Em","A"],3:["G","A","D"],4:["G","A","D"]
}
}
out={}
for cid,byline in MAP.items():
    lines=L[cid]["letra"].split("\n")
    rendered=[]
    for i,line in enumerate(lines):
        chords=byline.get(i,[])
        rendered.append("".join(f"[{c}]" for c in chords)+line)
    out[cid]="\n".join(rendered)
(R/"scripts"/"analysis_batch20d_candidates.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print("OK",len(out))
