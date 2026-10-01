#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
L=json.loads((R/"scripts"/"analysis_batch20c_lyrics.json").read_text(encoding="utf-8"))
MAP={
"C0067":{0:["G","D","C","D","G"],1:["D","C","D","G"],2:["C","Am","C","D","G"],3:["D","C","D","G"],5:["D","G","D","G"],6:["C","G","D","G"],7:["D","G","D","G"],8:["C","G","D","G"],10:["G","D","C","D","G"],11:["D","C","D","G"],12:["C","D","G"],13:["D","C","D","G"]},
"C0068":{0:["E","A","G#m","C#m"],1:["A","B","E","B"],2:["E","A","G#m","C#m"],3:["A","B","E","B"]},
"C0069":{1:["D","A7","G","D"],2:["A7","G","Em","A"],3:["Asus4","A"],4:["Em","A7","D","A","G","A"],5:["D","A7","Em7","A"],6:["D","A7","G","D"],7:["A7","G","Em","A"],8:["Asus4","A"],9:["Em","A7","D","A","G","A"],10:["D","A7","Em7","A"]},
"C0070":{1:["C","G","Am","Em"],2:["F","Bm7b5","A7","E7","C","G"]},
"C0071":{1:["Em","Am","Em","Am","B7","Em"],2:["Am","B7","C","Em","Am","D","Em"]},
"C0072":{1:["Am","G"],2:["Am","G"],3:["C","G"],4:["F","E7"]},
"C0074":{1:["C","C7","F","C"],2:["F","C","G","C"]},
"C0075":{1:["F","Bb","C","F"]},
"C0076":{1:["C","F"],2:["C","F"],3:["C","Em"],4:["F","C"]},
"C0077":{1:["C","F","C","F","G","C","F","C","F","G","C","G","Am","Em","F","G","C"]},
"C0078":{1:["G","D","C","G","C","G","A7","D"],2:["G","D","C","G","C","G","D","G"]},
"C0079":{1:["G","C","G","C","G"],2:["C","D","C","D"],3:["G","C","G","C","G"],4:["C","D","C","D"],5:["G","C","G","C","G"],6:["C","D","C","D"]},
"C0080":{1:["C","Am","F","G","C","C","Am","F","G","C"]},
"C0081":{1:["F","G","C","G","F","G"],2:["F","G","C","G","F","G","C"],3:["C","G","C","F","G","C"],4:["C","G","C","F","G","C"]},
"C0082":{1:["Am","C","F","G","C","Am","C","F","G","C"]},
"C0083":{1:["Dm","A7","Gm","A7","Dm"],2:["Gm","A7","Dm","A7","Dm"],3:["Gm","Dm","A7","Gm","A7","Dm"]},
"C0084":{1:["Dm","F"],2:["Gm","Dm","A7","Dm"]}
}
out={}
for cid,byline in MAP.items():
    lines=L[cid]["letra"].split("\n")
    rendered=[]
    for i,line in enumerate(lines):
        chords=byline.get(i,[])
        rendered.append("".join(f"[{c}]" for c in chords)+line)
    out[cid]="\n".join(rendered)
(R/"scripts"/"analysis_batch20c_candidates.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print("OK",len(out))
