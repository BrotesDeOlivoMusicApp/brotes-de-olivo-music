#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
L=json.loads((R/"scripts"/"analysis_batch20b_lyrics.json").read_text(encoding="utf-8"))
MAP={
"C0048":[["G"],["E"],["C"],["D"],["G","Em"],["Em"],["Am"],["D"],["G"],["Em"],["Am"],["D"],["G","Em"],["Am","C"],["D"]],
"C0050":[["G","Em","C","Am","D"],["G","Em","C","Am","D"],["Am","Em","C","Am","D"],["G","Em","C","D","G"]],
"C0051":[["G","C","G"],["C","G","D"],["G","C","G"],["C","G","D"],["G","C","G"],["C","G","D"],["C","D"],["G","Em"],["Am","D","Am"],["C"],["G"],["C","G","D"],["C","D"],["C","D","G"],["C","D","Bm","Em"],["C","D","Am","D"]],
"C0052":[["D","Am"],["Bm","Gbm"],["G","D","G"],["Am"],["G","Gbm","Bm"],["G","Am","D"],["G","Am","Gbm","Bm"],["G","Am","D"],[],[],[],[]],
"C0053":[["C","F","G","C"],["Am","F","Fm","C"],["G","C","Em","F","C"]],
"C0056":[["Am","F"],["Dm","Em"],[],["Am","F"],["Dm","Em"],["Am","F"],["Dm","Em"],["Am","F"],["Dm","Em"],[],["Am","F"],["Dm","Em"],["Am","F"],["Dm","Em"],["Am","F"],["Dm"],[],["Am","F"],["Dm","Em"],["Am","F"],["Dm","Em"]],
"C0057":[["Cm","Bb"],["Gm","Cm"],["Cm","Bb"],["Gm","Cm"],[],["Fm","Cm","G","Cm"],["Fm","Cm","G"],["Fm","Cm","G","Cm"],["Fm","Cm","G"],[],["Cm","Bb"],["Gm","Cm"],["Cm","Bb"],["Gm","Cm"],[],["Cm","Bb"],["Gm","Cm"],["Cm","Bb"],["Gm","Cm"],[],["Cm","Bb"],["Gm","Cm"],["Cm","Bb"],["Gm","Cm"]],
"C0058":[["G","D","Em","Bm"],["C","D"],["G","D","Em","Bm"],["C","D","G"],[],["C","D","G","Em"],["C","D","G"],["C","D"],["B","Em"],["C","D","G"]],
"C0059":[["Am","G","Dm","Am"],["Am","G","Dm","Am"],["G","Em","Am"],["G","Em","Am"],[],["Dm","C","Bb","Am"],["Dm","C","Bb","E"],[],["Am","G","Dm","Am"],["Am","G","Dm","Am"],["G","Em","Am"],["G","Em","Am"]],
"C0060":[["C"],["F"],["Dm"],["G","C"],["C"],["F"],["Dm"],["G","C"],[],["Am","Bm"],["D","E"],["F","G"],["Dm","Em","G","A","C","D"],[],["D"],["G"],["Em","A"],["D"],["D"],["G"],["Em","A"],["D"]],
"C0061":[["Fm","Eb","Db","Cm","Ab","Eb","Fm"]],
"C0062":[["C","Bb"],["F","C"],["Dm","Bb"],["F","C"],[],["Dm"],["Bb","F","C"],["Bb"],["F","Bb"],["Dm","C","F"],["G"],[],["C","Dm","Bb","F","C"],["Dm"],["Bb","F"],["C","Dm","Bb","F","C"],["Dm","Bb"],["F"],["Dm","G","Dm","G"]],
"C0063":[["Gm","Cm","Bb","Cm","Gm"],["Cm","Bb","Cm","Gm"],["Cm","Bb","Cm"],[],["Gm","Cm"],["Eb","Cm","D"],["Gm","Eb","Cm","Gm"],["Eb","D","Gm"],[],["Gm","Cm","Bb","Cm","Gm"],["Cm","Bb","Cm"]],
"C0064":[["D","E","F#m"],["D","E","A"],[],["D","E","F#m"],["D","E","A"]],
"C0065":[["D","A","Bm","A"],["D","A","G","A"],["D","A","Bm","A"],["D","A","G","A"],[],["G","D","Em","A"],[],["D","A","Bm","A"],["D","A","Bm","A"],["D","A","Bm","A"],["D","A","G","A"],[],["D","A","Bm","A"],["D","A","Bm","A"],[],["D","A","G"]],
"C0066":[["Dm","C","Am","Dm"]]
}
out={}
for cid,rows in MAP.items():
    lines=L[cid]["letra"].split("\n")
    rendered=[]
    for i,line in enumerate(lines):
        chords=rows[i] if i<len(rows) else []
        rendered.append("".join(f"[{c}]" for c in chords)+line)
    out[cid]="\n".join(rendered)
(R/"scripts"/"analysis_batch20b_candidates.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print("OK",len(out))
