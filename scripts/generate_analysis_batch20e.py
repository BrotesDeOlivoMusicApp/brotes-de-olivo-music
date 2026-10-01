#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
L=json.loads((R/"scripts"/"analysis_batch20e_lyrics.json").read_text(encoding="utf-8"))
MAP={
"C0102":{1:["C"],2:["G","C"],3:["G","C"],4:["Dm","G"],5:["C","G"],6:["F","G"],7:["C","G"],8:["F","G","C"]},
"C0104":{1:["Am","E","Am"],2:["F","E","Am","F","E"],3:["G","C"],4:["F","E","Am"],5:["F","E","Am","Dm","G"],6:["F","C"],7:["F","E","Am"],8:["F","Dm"],9:["F","E","Am"],14:["F","E","Am","E","Am"],15:["G","E","Am"],16:["E","Am","E","Am"],17:["E","Am"],18:["G","C"],19:["E","Am","E","Am"]},
"C0106":{1:["C","G","C","D","G"],2:["B7","Em","C","A7","D"],3:["C","D","G","C","D","G"]},
"C0107":{1:["D","G","D","G","A"],2:["Em","G","Em","G","A"],3:["D","D7","G","D","A","D"]},
"C0108":{1:["C","G"],2:["Em","F","Fm"],3:["C","G"],4:["Em","F"],5:["Am","F7"],6:["Am","Em","F"],7:["Dm"],8:["F","G"]},
"C0109":{1:["F","E","F","E"],2:["Am","G","F","E"],3:["Dm","G"],4:["E","Am"],5:["Dm","Em"],6:["F","E"]},
"C0110":{1:["D","G","D","G"],2:["Em","G","Em","A"],3:["D","G","D","F#"],4:["Bm","G","Em","F#m","F#"],5:["D","G","Cm"],6:["G","Cm","A"]},
"C0111":{1:["Dm","C","Bb"],2:["C","Gm","Am","Dm"],3:["Dm","C","Bb"],4:["C","Gm","Am","Dm"],5:["Bb","C","Am"],6:["D7","Gm","A7","Dm"],7:["Bb","C","Am"],8:["D7","Gm","A","Dm"]},
"C0112":{1:["C","F"],2:["Dm","G","C"],3:["Fm","C","C7","F"],4:["Dm","D7"],5:["G","C"],6:["Am","G","Am","D"],7:["G","C"],8:["G","Am","D"]},
"C0113":{1:["E","Am","E","Am"],2:["G","C","F","E"],3:["Dm","G","C","Am"],4:["Dm","E","Am","F","E"],5:["Dm","Am"],6:["Dm","G","C"],7:["Dm","E"],8:["Am","Em"],9:["F","C"],10:["Dm","Am"],11:["Bb","Am"],12:["F","E","Am"]},
"C0114":{1:["Cm","Fm","Cm"],2:["Fm","Cm","G","Cm"],3:["Cm","Fm","Cm"],4:["Fm","Cm","Ab","G"],5:["Cm"],6:["Fm","Cm"],7:["Fm","G"],8:["Cm","Fm","Cm"],9:["Fm","Cm","Ab","G"],10:["Cm"],11:["C","F","C"],12:["F","C","G"],13:["C","G","C"],14:["G","C"],15:["G","C"],16:["F","C","G","C"]},
"C0115":{1:["Gm"],2:["F"],3:["Cm","D7"],4:["Cm","D7"],5:["Gm"],6:["F"],7:["Cm","D7"],8:["Cm","D7"],9:["Gm","F","Gm"],10:["Gm","F","Gm"],11:["F","Gm"],12:["D7"],13:["Cm","Gm"],14:["Cm","F"],15:["Cm","D7","Gm"],16:["D7","Gm"]},
"C0116":{1:["D","A","G","D"],2:["D","A","G","A"],3:["G","D","G","D"],4:["D","A","G","D"]},
"C0117":{1:["C","G","Am","F","G"],2:["C","G","Am","F","G"],3:["Am","G"],4:["F","E"],5:["A","E","F#m"],6:["Bm","E","A"],7:["E","F#m","Bm","E"]}
}
expected=set(MAP)
out={}
for cid,byline in MAP.items():
    lines=L[cid]["letra"].split("\n")
    rendered=[]
    for i,line in enumerate(lines):
        chords=byline.get(i,[])
        rendered.append("".join(f"[{c}]" for c in chords)+line)
    out[cid]="\n".join(rendered)
if set(out)!=expected or len(out)!=14:
    raise SystemExit("Conjunto de candidatos inesperado")
(R/"scripts"/"analysis_batch20e_candidates.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print("OK",len(out))
