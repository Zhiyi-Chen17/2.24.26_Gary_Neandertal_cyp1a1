#!/usr/bin/env python3
from collections import OrderedDict
from pathlib import Path

aln="results/alignments/CYP1A1_three.aln.fa"

seqs=OrderedDict()
name=None
for ln in open(aln):
    ln=ln.strip()
    if not ln:
        continue
    if ln.startswith(">"):
        name=ln[1:].split()[0]
        seqs[name]=[]
    else:
        seqs[name].append(ln)
for k in seqs:
    seqs[k]="".join(seqs[k])

names=list(seqs.keys())
L=len(seqs[names[0]])
assert all(len(seqs[n])==L for n in names)

aa_pos=0
diff=[]
for i in range(L):
    col=[seqs[n][i] for n in names]
    if col[0] != "-":
        aa_pos += 1
    nongap=[c for c in col if c != "-"]
    if len(set(nongap))>1:
        diff.append((aa_pos, col))

out_lines=[]
out_lines.append("\t".join(["AA_pos"]+names))
for p, col in diff:
    out_lines.append("\t".join([str(p)]+col))

Path("results/variants").mkdir(parents=True, exist_ok=True)
Path("results/variants/diff_sites.tsv").write_text("\n".join(out_lines)+"\n")

print("Num diff sites:", len(diff))
for p, col in diff:
    print(p, *col, sep="\t")
