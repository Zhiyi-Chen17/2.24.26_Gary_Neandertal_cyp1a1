#!/usr/bin/env bash
set -euo pipefail

for s in neandertal denisova ustishim; do
  transeq -sequence results/${s}.CYP1A1.cds.fa -outseq results/${s}.CYP1A1.protein.fa
done

cat results/neandertal.CYP1A1.protein.fa results/denisova.CYP1A1.protein.fa results/ustishim.CYP1A1.protein.fa > results/CYP1A1_three.protein.fa
clustalo -i results/CYP1A1_three.protein.fa -o results/alignments/CYP1A1_three.aln.fa --outfmt=fasta --force
