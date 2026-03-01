#!/usr/bin/env python3
from pathlib import Path
import subprocess

# Config
REF = str(Path.home() / "1data/ref/human_g1k_v37/human_g1k_v37.fasta")
BED = "results/CYP1A1.NM_000499.CDS.bed"

samples = {
  "neandertal": "results/neandertal.CYP1A1.flt.vcf.gz",
  "denisova":   "results/denisova.CYP1A1.flt.vcf.gz",
  "ustishim":   "results/ustishim.CYP1A1.flt.vcf.gz",
}

def run(cmd, stdin=None):
    p = subprocess.run(cmd, input=stdin, text=True, check=True, capture_output=True)
    return p.stdout

def revcomp(seq: str) -> str:
    comp = str.maketrans("ACGTNacgtn", "TGCANtgcan")
    return seq.translate(comp)[::-1]

# Read BED
exons=[]
strand=None
with open(BED) as f:
    for ln in f:
        chrom, start0, end0, name, score, st = ln.strip().split("\t")
        exons.append((chrom, int(start0), int(end0)))
        strand=st

# Always build in genomic order, then revcomp if minus strand
exons.sort(key=lambda x: x[1])

Path("results").mkdir(parents=True, exist_ok=True)

for tag, vcfgz in samples.items():
    parts=[]
    for chrom, start0, end0 in exons:
        region = f"{chrom}:{start0+1}-{end0}"  # faidx: 1-based inclusive
        ref_fa  = run(["samtools","faidx",REF,region])
        cons_fa = run(["bcftools","consensus","-H","1",vcfgz], stdin=ref_fa)
        seq="".join([ln.strip() for ln in cons_fa.splitlines() if not ln.startswith(">")]).upper()
        parts.append(seq)

    cds="".join(parts)
    if strand == "-":
        cds = revcomp(cds)

    out = f">{tag}_CYP1A1_CDS\n" + "\n".join(cds[i:i+60] for i in range(0,len(cds),60)) + "\n"
    Path(f"results/{tag}.CYP1A1.cds.fa").write_text(out)
    print(tag, "CDS len", len(cds), "strand", strand, "head", cds[:30])
