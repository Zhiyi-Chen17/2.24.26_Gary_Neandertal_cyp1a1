#!/usr/bin/env bash
set -euo pipefail

for s in neandertal denisova ustishim; do
  bcftools filter -i 'QUAL>20 && INFO/DP>5' results/${s}.CYP1A1.vcf -Oz -o results/${s}.CYP1A1.flt.vcf.gz
  tabix -p vcf results/${s}.CYP1A1.flt.vcf.gz
done
