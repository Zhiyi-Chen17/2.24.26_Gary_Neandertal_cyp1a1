#!/usr/bin/env bash
set -euo pipefail
source config/config.sh

mkdir -p results/logs

# Call variants within REGION for each sample
freebayes -f "$REF" -r "$REGION" "$BAM_NEANDERTAL" > results/neandertal.CYP1A1.vcf 2> results/logs/freebayes_neandertal.log
freebayes -f "$REF" -r "$REGION" "$BAM_DENISOVAN" > results/denisova.CYP1A1.vcf   2> results/logs/freebayes_denisova.log
freebayes -f "$REF" -r "$REGION" "$BAM_USTISHIM"  > results/ustishim.CYP1A1.vcf   2> results/logs/freebayes_ustishim.log
