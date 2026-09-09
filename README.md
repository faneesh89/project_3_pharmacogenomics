# Pharmacogenomics Variant Interpretation Pipeline

A Python pipeline that maps real patient variants from ClinVar to
pharmacogenomics star alleles, determines drug metabolism phenotypes,
and generates a clinical HTML report — following CPIC and PharmVar
guidelines.

Built entirely on real, publicly available ClinVar data (GRCh38),
not synthetic or toy datasets.

---

## What it does

Given a VCF file containing patient variants, the pipeline:

1. Parses all variant records from the VCF file
2. Filters to variants in known pharmacogenes (CYP2D6, CYP2C19,
   CYP2C9, VKORC1, CYP4F2, TPMT, DPYD)
3. Matches variants to known star alleles using rs numbers — the
   same approach used by targeted clinical genotyping panels
4. Resolves TPMT special cases (e.g. *3A requires two variants
   together: rs1800460 + rs1142345)
5. Generates an HTML clinical report showing called alleles,
   function classification, and rs numbers per gene

## Results on the included dataset

Run against ClinVar GRCh38 (4,435,099 variants):

| Gene    | Called Allele(s) | Function                        |
|---------|------------------|---------------------------------|
| CYP2D6  | *41, *2, *3      | decreased, normal, no_function  |
| CYP2C19 | *3, *2           | no_function, no_function        |
| CYP2C9  | *2, *3           | decreased, no_function          |
| VKORC1  | variant          | resistant                       |
| CYP4F2  | *3               | decreased                       |
| TPMT    | *3C              | decreased                       |
| DPYD    | *13              | no_function                     |

11 variant alleles identified across 7 pharmacogenes.

---

## Pipeline architecture

```
data/clinvar.vcf.gz
      │
      ▼
vcf_parser.py        → reads compressed VCF directly (gzip.open),
                        yields one dict per variant with all 8 columns
                        + parsed INFO field
      │
      ▼
variant_filter.py     → filters by QUAL ≥ 20 and DP ≥ 10
                        (skipped for ClinVar — curated databases
                        don't have sequencing-style QUAL/DP values)
      │
      ▼
gene_filter.py        → keeps only variants in the 7 tracked
                        pharmacogenes, using chromosome + position
                        coordinate ranges
      │
      ▼
allele_caller.py      → matches each variant to a known star allele
                        by rs number (looked up from INFO['RS'] field
                        for ClinVar data, or the VCF ID column for
                        standard sequencing VCFs)
      │
      ▼
report_generator.py   → writes the HTML clinical report
```

---

## Data source

- **Database:** ClinVar (National Center for Biotechnology Information)
- **Build:** GRCh38 (hg38)
- **File type:** VCF (Variant Call Format), gzip-compressed
- **Download:** ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/
- **Size:** 4,435,099 variants

ClinVar is a freely accessible, public archive of human genetic
variants and their clinical significance, submitted by labs and
researchers worldwide.

---

## Key design decisions

**RS number matching instead of chromosomal position.**
Star alleles are matched by rs number (e.g. rs4244285 = CYP2C19*2),
not by hardcoded genomic coordinates. RS numbers are stable across
genome builds (GRCh37/38), making the pipeline build-independent.
This is the same approach used by commercial targeted genotyping
panels (e.g. those based on CPIC/PharmVar reference data).

**ClinVar stores rs numbers in the INFO field, not the ID column.**
Unlike standard sequencing VCFs (where rs numbers appear in the ID
column), ClinVar uses its own numeric accession IDs in the ID column
and stores rs numbers under the `RS` key in the INFO field. The
allele caller checks both locations — ID column first, INFO['RS']
as a fallback — to handle both data sources correctly.

**TPMT *3A requires two variants together.**
TPMT*3A is defined by both rs1800460 AND rs1142345 being present.
If only one is present, the correct call is *3B or *3C (still
decreased function, but a different allele). The pipeline handles
this case explicitly in `resolve_tpmt_alleles()` rather than
treating each variant independently.

**7-gene curated list, not the full PharmVar catalog.**
The pipeline covers the 7 most clinically actionable pharmacogenes
with clear CPIC-level evidence: CYP2D6, CYP2C19, CYP2C9, VKORC1,
CYP4F2, TPMT, and DPYD. These cover the key drug-gene pairs for
clopidogrel, codeine, warfarin, azathioprine, and 5-fluorouracil —
all drugs with FDA-recognized pharmacogenomic labeling.

---

## Bugs found and fixed during development

**ClinVar quality filter mismatch.**
ClinVar variants have an INFO field (where CLNSIG lives), but do
NOT have meaningful QUAL, DP, or FILTER values — because ClinVar is
a curated clinical database, not raw sequencer output. Running a
sequencing-style quality filter on ClinVar silently rejected all
4.4 million variants. Fix: ClinVar data is analyzed without the
quality filter, which only applies to actual sequencing output.

**rs number extraction from INFO field.**
ClinVar stores its own numeric accession IDs in the VCF ID column,
not rs numbers. RS numbers are stored as floats (e.g. `3918290.0`)
in the INFO RS field. The `get_rs_number()` function was updated to
fall back to INFO['RS'] when the ID column has no rs number, and
to convert float-formatted values correctly (`int(float(rs_raw))`).

---

## Known limitations

- Gene copy number variants (CYP2D6*5 deletion, *1xN duplication)
  cannot be detected from SNP data — these require CNV analysis.
- Phasing (which allele is on which chromosome) is not resolved —
  diplotype assignment uses simplifying assumptions.
- Star allele coverage is a representative subset of CPIC's most
  common clinically actionable alleles, not the complete PharmVar
  catalog (which contains 100+ alleles per gene).

## Possible future enhancements

- Diplotype-to-phenotype mapping using CPIC lookup tables
- Drug-specific clinical recommendations per phenotype
- Support for patient VCF files alongside ClinVar reference data

---

## Running the pipeline

```bash
git clone <this-repo>
cd project_3_pharmacogenomics

# Default — uses data/clinvar.vcf.gz
python3 main.py

# Custom input/output
python3 main.py -i path/to/your.vcf.gz -o output/my_report.html
```

Output is written to `output/pgx_clinical_report.html`.

## Requirements

```
Python 3.x (standard library only — no external dependencies)
```

---

## Project context

This is the third in a series of four genomics pipeline projects:

1. FASTQ quality control clone
2. VCF variant analysis (ClinVar, 4.4M variants)
3. **Pharmacogenomics variant interpretation (this project)**
4. TCGA cancer driver gene mutation analysis