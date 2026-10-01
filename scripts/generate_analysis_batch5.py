#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
L=json.loads((R/"scripts"/"analysis_batch5_lyrics.json").read_text(encoding="utf-8"))
MAP={
 "C0181":{
  1:["Em","B7"],2:["Em"],3:["Em","B7"],4:["Em"],5:["G","D"],6:["C","Am","B7"],
  7:["Em","B7","Em"],8:["Em","B7","Em"],19:["B7","Em"],20:["Am","D","G"],21:["Am","B7","C"],22:["B7","Em"]
 },
 "C0182":{
  1:["G","C","G","Am"],2:["D","C","G"],3:["C","G","C"],4:["D","G","Am","D"],5:["C","G"],
  6:["G","Am"],7:["D","C","G"],8:["C","G","C"],9:["G","Am"],10:["D","G"]
 },
 "C0183":{
  1:["C","Em","F"],2:["G","Am","G#","G"],3:["C","Em","F"],4:["G","Am","G#","G"],
  5:["F","C","G#","A#"],6:["F","C","G#","G"],7:["F","C","G#","A#"],8:["F","C","G#","G"],
  9:["F","C","G#","A#"]
 }
}
out={}
for cid,mp in MAP.items():
    lines=L[cid]["letra"].split("\n")
    rendered=[]
    for i,line in enumerate(lines):
        chords=mp.get(i,[])
        rendered.append("".join(f"[{c}]" for c in chords)+line)
    out[cid]="\n".join(rendered)
(R/"scripts"/"analysis_batch5_candidates.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print("OK",len(out))
