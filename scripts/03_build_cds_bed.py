#!/usr/bin/env python3
from pathlib import Path
import sys

infile = "metadata/CYP1A1.refGene.tsv"
tx = "NM_000499"
outbed = f"results/CYP1A1.{tx}.CDS.bed"

lines = Path(infile).read_text().strip().splitlines()
rows = [ln.strip().split() for ln in lines[1:] if ln.strip()]

row = None
for r in rows:
    if r[0] == tx:
        row = r
        break
if row is None:
    sys.exit(f"Cannot find {tx} in {infile}")

chrom = row[1]
strand = row[2]
if chrom.startswith("chr"):
    chrom = chrom[3:]

cdsStart, cdsEnd = int(row[3]), int(row[4])
exonStarts = [int(x) for x in row[5].strip(",").split(",")]
exonEnds   = [int(x) for x in row[6].strip(",").split(",")]

cds_exons = []
for s, e in zip(exonStarts, exonEnds):
    cs = max(s, cdsStart)
    ce = min(e, cdsEnd)
    if cs < ce:
        cds_exons.append((cs, ce))

# UCSC/BED coordinates: 0-based half-open
# We keep exon list unsorted here; downstream script sorts by genomic coordinate.
out = []
for i, (s, e) in enumerate(cds_exons, start=1):
    out.append(f"{chrom}\t{s}\t{e}\t{tx}_CDS_exon{i}\t0\t{strand}")

Path("results").mkdir(parents=True, exist_ok=True)
Path(outbed).write_text("\n".join(out) + "\n")
print(f"Wrote {outbed} exons={len(cds_exons)} strand={strand} cds={cdsStart}-{cdsEnd}")
