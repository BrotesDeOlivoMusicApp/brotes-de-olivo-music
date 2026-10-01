#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
L=json.loads((R/"scripts"/"analysis_batch3_lyrics.json").read_text(encoding="utf-8"))
MAP={
"C0151":[["D","G","D","A","G","A"],["D","F#m","G","A","D","A"],["D","G","A","D"],["D","A","G","A"],["D","G","A","D"]],
"C0152":[["C","C7"],["F","C"],["G","C"],["C","C7","F","G7"],["C","C7","F"],["C"],["G","C"],["G","C"],["F","G","C"]],
"C0153":[["D","A7","D"],["A7","E7","A7"],["G","D"],["A","D"],["D","A7","D","A","D"],["D7","G","D","E7","A"],["G","A7","D","G","D"],["G","A7","G","D"],["G","A7","D","A","D"]],
"C0154":[["Dm","C","Dm","Bb","F"],["Dm","C","Dm","Bb"],["Dm","C","Dm","Bb","F"],["Dm","C","Dm","Bb","Dm"],["F","Bb","C"],["F","Bb","F","C"],["Dm","C","Dm","Bb","F"],["Dm","C","Dm","Bb","Dm"],["Dm","C","Dm","Bb","F"],["Dm","C","Dm","Bb","Dm"]],
"C0155":[["Dm","C","Dm"],["C","Dm"],["C","Dm","F","Bb"],["C","Dm","F","A7"],["F","Bb","C","Dm"],["Dm","C","Dm"],["Dm","C","Dm"],["Dm","C","F","Bb"],["C","Dm","F","A7"],["F","Bb","C","Dm"]],
"C0156":[["C","G7","C"],["F","G7","C"],["F","G7","C"],["C","G7","C"],["F","G7","C"],["F","G7","C"],["C","G7","C"],["F","G7","C"],["F","G7","C"],["C","G7","C"],["F","G7","C"],["F","G7","C"],["C","G7","C"],["F","G7","C"],["F","G7","C"]],
"C0157":[["Am"],["Dm"],["G","G7"],["C","Bm7b5"],["Am"],["Dm"],["G","G7"],["C","Bm7b5"],["Dm","E7","Am","A7"],["Dm","Am","A7"],["Dm","G7","C"],["Bm7b5","F","Am","A7"],["Dm","G7","C","F"],["Bm7b5","F","Am"]],
"C0158":[["E","B7","E"],["E","A","B7"],["E","B7","E"],["A","B7","E"],["B7","E","B7"],["E","B7"],["B7","E","B7"],["E"]],
"C0159":[["D","G","D"],["G","D","A","D"],["D","G","D"],["G","D","A","D"],["D","G","A","D"]]
}
out={}
for cid, rows in MAP.items():
    lines=L[cid]["letra"].split("\n")
    new=[]
    for i,line in enumerate(lines):
        chords=rows[i] if i<len(rows) else []
        new.append("".join(f"[{c}]" for c in chords)+line)
    out[cid]="\n".join(new)
(R/"scripts"/"analysis_batch3_candidates.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print("OK",len(out))
