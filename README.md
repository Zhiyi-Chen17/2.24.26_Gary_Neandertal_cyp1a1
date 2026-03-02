# 2.24.26_Gary_Neandertal_cyp1a1
# CYP1A1 ancient protein reconstruction (hg19/GRCh37)

This repository contains a to reconstruct the **CYP1A1** coding sequence (CDS) and protein sequence from high-coverage ancient BAM files, and to compare amino acid differences by multiple sequence alignment.

The workflow follows the same method described in the 2016 AHR analysis (https://doi.org/10.1093/molbev/msw143), but applied to **CYP1A1**.

---

## Summary of current result

Using **RefSeq transcript NM_000499** (hg19/refGene) for CYP1A1 CDS reconstruction, we observe **one** amino-acid difference among the three reconstructed proteins (haplotype-1 consensus):

- **AA 482:** Ref = **V**, Neandertal = **V**, Denisovan = **M**, Ust’-Ishim = **V**  
  (output: `results/variants/diff_sites.tsv`)

---

## Data sources (consistent with 2016 AHR analysis)

We use high-coverage genomes analogous to those used for AHR:

1) **Neandertal (ENA ERP002097)**
- Source:
- File used here: `L9105.bam` / `all-L9105.bam` (this repo expects a local BAM named `all-L9105.rgfix.bam`)
- Note: in our local copy, reads contain `RG:Z:L9105` but the BAM header lacks `@RG`, so we add an `@RG` header line to create `all-L9105.rgfix.bam` for compatibility with freebayes.

2) **Denisovan high-coverage**
- In the AHR paper, Denisovan was accessed via a UCSC alignment track.
- Here we directly download the BAM:
  - `https://hgdownload.soe.ucsc.edu/gbdb/hg19/bbi/T_hg19_1000g.bam`
- This repo expects a local BAM named `T_hg19_1000g.bam`.

3) **Ancient modern human (ENA PRJEB6622)**
- This repo expects a local BAM named `Ust_Ishim.hg19_1000g.all.bam`.

### Reference genome
- **1000 Genomes GRCh37** reference (`human_g1k_v37.fasta`)
---

## Pipeline overview
1) Call variants in the CYP1A1 locus for each BAM using **freebayes**
2) Filter variants using **bcftools** (`QUAL>20 && INFO/DP>5`)
3) Build a CDS exon BED for **NM_000499** from UCSC `refGene` export (`metadata/CYP1A1.refGene.tsv`)
4) Reconstruct per-sample CDS by applying variants exon-by-exon with `bcftools consensus -H 1`
   - Important: CYP1A1 is on the **minus strand**, so we reconstruct in genomic order and then reverse-complement the final CDS
5) Translate CDS to protein (**EMBOSS transeq**)
6) Perform multiple sequence alignment (**Clustal Omega**) and report amino-acid differences

Outputs are written under `results/`.

---

## Requirements

Tools (tested versions in our environment):
- samtools
- bcftools
- freebayes
- bedtools
- EMBOSS (transeq)
- clustalo (Clustal Omega)
- python3


---

## Setup

### 1) Clone repo
```bash
git clone git@github.com:Zhiyi-Chen17/2.24.26_Gary_Neandertal_cyp1a1.git
cd cyp1a1-archaic
```
### 2) Create Conda Environment
```bash
conda env create -f environment/archaic_cyp1a1.yml
conda activate archaic_cyp1a1
```

### 3) Prepare reference
Download and index a GRCh37/hg19 reference with contigs 1..22 (no chr prefix), e.g. 1000G human_g1k_v37.fasta, and update config/config.sh if needed.

### 4) Prepare BAMs

Down the all-L9105.bam, T_hg19_1000g.bam and Ust_Ishim.hg19_1000g.all.bam as described in **Data sources**, add an `@RG` header line to create `all-L9105.rgfix.bam` for compatibility with freebayes.

Create index of BAMs

---

## Run
```bash
./scripts/01_call_variants.sh
./scripts/02_filter_vcf.sh
./scripts/03_build_cds_bed.py
./scripts/04_reconstruct_cds.py
./scripts/05_translate_and_align.sh
./scripts/06_diff_sites.py
```
---

## Key outputs:

VCFs: results/*CYP1A1.vcf, results/*CYP1A1.flt.vcf.gz

CDS FASTA: results/{neandertal,denisova,ustishim}.CYP1A1.cds.fa

Protein FASTA: results/{neandertal,denisova,ustishim}.CYP1A1.protein.fa

Alignment: results/alignments/CYP1A1_three.aln.fa

Difference table: results/variants/diff_sites.tsv

---

## Citation

This repo’s workflow is designed to mirror the reconstruction approach described in the AHR study:

Neandertal BAM from ENA (ERP002097; L9105)

Denisovan via UCSC alignment resources

Ust’-Ishim BAM from ENA (PRJEB6622)

Variant calling with freebayes; alignment with Clustal Omega
