#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
L=json.loads((R/"scripts"/"analysis_batch4_lyrics.json").read_text(encoding="utf-8"))
MAP={
"C0171":[
 [],["C","F","A","Dm"],["C","F","Bb","A"],["Bb","F","G#"],["F#","C#","F#","G#"],
 ["C#","G#","Cb","F#"],["F#m","C#","D#","G#"],[],[],[],[]
],
"C0172":[
 [],["C","Em","F","C","Em","G"],["Am","E","C","D","F","C"],["C","Am","F","E"],
 ["F","G","C","F","G","Cm"],["Cm","Fm","Bb","D#"],["G#","Fm","G","C7"],["F","G","C","F"],["G","C"]
],
"C0173":[
 [],["G","B"],["Em","G7","C","A"],["D","F","C"],["Cm","C","D"],
 ["G","D","C","Cm","G"],["B","Em","G7","C"],["D","C","D","C"],["D","C","Cm","G"],
 [],[],[],[],[],[],[],[]
],
"C0174":[
 [],["F","C","Bb","F"],["Dm","Am","Bb","C"],["Dm","Am","Gm","Bb"],["C","F","Gm","C"],
 ["Gm","A7","Dm"],["A7","Dm","Gm","A7"],["C","Gm","C","F"],["Gm","A7","Dm","F","Dm","C"],
 [],[],[],[],[],[],[],[],["Dm","A7","Dm"]
],
"C0175":[
 [],["Dm","G","C","A7"],["Dm","G"],["D7","Fm","C","A7"],["Dm","Ddim7","F","G"],
 ["F","C"],["E","Am","Gm","C","F"],["Gm","A7"],["Dm","G","Gm","A7","Dm"]
],
"C0176":[
 [],["C","Em","Am","Em"],["F","G","F","G"],["C","Em","Am","Em"],["F","G","F","G"],
 ["C","Em","F","G"],["Dm","Em","F","G"],["F","G","F","G"],["F","Em","F","G"],
 [],[],[],[],[]
],
"C0177":[
 [],["Em","D","A"],["Em","D","Bm","Em"],["G","D","C","Em"],["G","D","C","Em"],
 ["Em","D"],["C","Bm"],["A","D"],["C","Am","D","Em"],
 [],[],[],[],[],[],[],[],[]
],
"C0178":[
 [],["D","G","D"],["Bm","Em","A","D"],["D","G","D","G","A"],["G","A","D"],
 [],[],[],[],[],[]
],
"C0179":[
 [],["D","G","A"],["Em","G","D"],["D","D7","G"],["D","A","D"],
 ["A","D","G","A","E","A","D"],["D","D7","G","Em","A","D"],["Bm","G","A","D"],
 [],[],[],[],[],[]
],
"C0180":[
 [],["Am","Dm","Am","Dm"],["G","Dm","G","C"],["A","Gm","A7","Dm"],["Am","Dm","E","Am"],
 ["Am","Em"],["Am","C","G","Em","Am"],
 [],[],[],[],[],[],[],[],[],[]
]
}
out={}
for cid,rows in MAP.items():
    lines=L[cid]["letra"].split("\n")
    new=[]
    for i,line in enumerate(lines):
        chords=rows[i] if i<len(rows) else []
        new.append("".join(f"[{c}]" for c in chords)+line)
    out[cid]="\n".join(new)
(R/"scripts"/"analysis_batch4_candidates.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print("OK",len(out))
