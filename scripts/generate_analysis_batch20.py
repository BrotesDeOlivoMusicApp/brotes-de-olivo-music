#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
L=json.loads((R/"scripts"/"analysis_batch20_lyrics.json").read_text(encoding="utf-8"))
MAP={
"C0029":[["Am","E","Am"],["Am","E","Am"],["Am","E","Dm","Am"],["C","Dm","E"],["Dm","Am"],["E","Dm","Am"]],
"C0030":[["A","D","Bm"],["D","Bm","D","E"],["D","A","Bm","A"]],
"C0031":[["D","G","D"],["G","D"],["G","C","A"],["F","Am","G","D"],["D","C","G","D"],["G","C","D","C","A"],["F","Am","G","D"],["F","Am","G","A"]],
"C0032":[["Em","Am","B7","Em"],["Em","D","Am","Em"],["Em","D","Am","B7"]],
"C0033":[["D","G","D","G","A"],["D","G","D","G","A"],["G","Em","G","A","D"],["D","A","Bm","Em","A","D"]],
"C0034":[["G","C","G"],["C","G"],["B7","Em"],["C","Am","D"],["G","D","Em"],["C","Am","D"],["G","D","G","Em"],["C","D","G"],["G","D","Em"],["C","Am","D"],["G","D","G","Em","Bm","C","D","G"]],
"C0035":[["Am","G"],["Am","G","Dm","G"],["Am","G"],["Am","G","F","G"],["Am","D","Am"],["Am","C","G","Am"],["Am","D","Am"],["Am","C","G","Am"]],
"C0036":[["D","Bm","Gbm","G","D","G","D"],["G","Gm","D","G","A","D"]],
"C0037":[["Em","B7","Am","Em"],["Em","B7","Em"],["Am","B7","Am"],["C","B7"],["Em","Am","B7","Am"],["B7","Em"],["Am","B7","C"],["Am","B7","Em"],["Am","B7","Em"],["Am","B7","Em"],["Am","D","C"],["C","B7"],["Am","B7","Em"]],
"C0038":[["Em","Bm","C","G"],["Am","C","D","Am","B7"],["Em","Bm","C","G"],["Am","C","D"],["Am","B7"],["Am","B7"]],
"C0039":[["C","F","C","C","Em","F","G"],["F","C","G","C"]],
"C0040":[["G","C","G","C","Am"],["C","D","G","D7"],["C","Am","D7"],["G","C","G","C","Am"],["C","D","G"],["C","D","C","G"]],
"C0041":[["D","G","D"],["G","Am"],["G","Am","Em","Am"],["D","G","D"],["G","Am"],["G","Am"],["Em","Am"],["D","G","D"],["G","Am"],["G","Am"],["Em","Am"],["D","G","D"],["G","Am"],["G","Am"],["Em","Am"]],
"C0042":[["C","G"],["Am","G","C"],["Am","F","G"],["C","Em","Am","F","G"],["C","Am","Em","F","Fm","F","C"]],
"C0043":[["G","G","C"],["C","D","G"],["Em","Bm","C","D","Em"],["G","G","C"],["C","D","G"],["Em","Bm","C","D","Em"],[],[],[],[],[],[]],
"C0044":[["G","G","C","G"],["G","F","C","G"],["G","C","G"],["G","C","G"],["G","C","G"],["F","C","G"],["F","C","G"]],
"C0045":[["Am","G"],["Dm","E","Am"],["Am","Dm","G"],["F","E","Am"],["Dm","G","C","Am"],["Dm","E","Am"],[],[],[],[],[],[],[]],
"C0046":[["C","D","G","C","Em","D"],["C","D","G","C","Em","D"],["G","D","C","D","G"],["D","Am","D","G"],["D","C","D"],["C","D","G","C","Em","D"],["C","D","G","C","Em","D"],["G","D","C"],["D","G","D","G"],["D","C","D"]],
"C0047":[["C","F","C","Em","F","G"],["Am","F","A7","Dm","C","G"],["F","C","F","C"],[],[]]
}
out={}
for cid,rows in MAP.items():
    lines=L[cid]["letra"].split("\n")
    rendered=[]
    for i,line in enumerate(lines):
        chords=rows[i] if i<len(rows) else []
        rendered.append("".join(f"[{c}]" for c in chords)+line)
    out[cid]="\n".join(rendered)
(R/"scripts"/"analysis_batch20_candidates.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print("OK",len(out))
