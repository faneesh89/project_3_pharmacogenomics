#!/usr/bin/env python3
"""
Project 3: Pharmacogenomics Pipeline 
"""
import argparse
import os
import sys
from datetime import datetime
from vcf_parser import read_vcf
from variant_filter import filter_variants
from gene_filter import filter_pharmacogenes
from allele_caller import call_alleles
from pgx_pipeline import build_patient_report, build_warfarin_report
from report_generator import generate_html_report


def main():
    parser = argparse.ArgumentParser(description="Pharmacogenomics Clinical Pipeline")
    parser.add_argument(
        "-i", "--input",
        default="data/clinvar.vcf.gz",
        help="Path to input VCF file (default: data/clinvar.vcf.gz)"
    )
    parser.add_argument(
        "-o", "--output",
        default="output/pgx_clinical_report.html",
        help="Output HTML report path (default: output/pgx_clinical_report.html)"
    )
    parser.add_argument("--min_qual",  type=float, default=20.0,
                        help="Minimum QUAL score (default: 20.0)")
    parser.add_argument("--min_depth", type=int,   default=10,
                        help="Minimum read depth DP (default: 10)")
    parser.add_argument('--age', type=int, default=None, help='Patient age in years')
    parser.add_argument('--height', type=float, default=None, help='Height in cm')
    parser.add_argument('--weight', type=float, default=None, help='Weight in kg')
    parser.add_argument('--amiodarone', action='store_true', help='Taking amiodarone')
    parser.add_argument('--smoker', action='store_true', help='Current smoker')
    parser.add_argument('--debug-alleles', action='store_true',
                    help='Print raw allele records for inspection')
    args = parser.parse_args()

    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    print("\n" + "="*60)
    print("STARTING PHARMACOGENOMICS PIPELINE")
    print("="*60)

    try:
        print(f"[1/5] Reading VCF file: {args.input} ...")
        all_variants = list(read_vcf(args.input))
        print(f"      Total variants parsed: {len(all_variants)}")
    except FileNotFoundError:
        print(f"Error: '{args.input}' not found. Check your path or use -i to specify one.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error while parsing VCF: {e}")
        sys.exit(1)

    print(f"[2/5] Filtering by quality (QUAL >= {args.min_qual}, DP >= {args.min_depth})...")
    passed_variants, rejected_stats = filter_variants(
        all_variants, min_qual=args.min_qual, min_depth=args.min_depth
    )
    print(f"      Passed QC: {len(passed_variants)}")
    print(f"      Failed QC: {len(rejected_stats)}")

    print("[3/5] Filtering to known pharmacogenes (CYP2D6, CYP2C19, etc.)...")
    pgx_variants = filter_pharmacogenes(passed_variants)
    print(f"      Found {len(pgx_variants)} variants in pharmacogenes")

    print("[4/5] Calling star alleles...")
    alleles = call_alleles(pgx_variants)
    if args.debug_alleles:
        print("\n--- DEBUG: raw allele records ---")
        for gene in ('VKORC1', 'CYP4F2', 'CYP2C19'):
            for record in alleles.get(gene, []):
                print(f"{gene:<8} {record}")
        print("--- end debug ---\n")

    print("[5/5] Predicting phenotypes and drug recommendations...")
    report_rows = []                                  # NEW: keep the rows
    for gene, allele_list in alleles.items():
        row = build_patient_report(gene, allele_list)
        report_rows.append(row)                       # NEW: collect instead of discard
        print(f"  {row['gene']:<8} {row['diplotype']:<14} {row['phenotype']}")
        print(f"           {row['recommendation']}")

# clinical envelope — unused today, ready for the IWPC dose estimate later
    clinical = {
        'age':        args.age,
        'height_cm':  args.height,
        'weight_kg':  args.weight,
        'amiodarone': args.amiodarone,
        'smoker':     args.smoker,
}

    warfarin = build_warfarin_report(alleles, report_rows)
    if warfarin:
        print("\n  WARFARIN COMBINED RECOMMENDATION")
        print("  " + "-" * 40)
        for gene_name, factor in warfarin['factors'].items():
            print(f"  {gene_name:<8} x{factor}")
        print(f"  Net dose factor: x{warfarin['net_factor']}")
        print(f"  {warfarin['verdict']}")

    generate_html_report(alleles, args.output)

    print("="*60)
    print("PIPELINE COMPLETE!")
    print(f"Report saved to: {args.output}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
    