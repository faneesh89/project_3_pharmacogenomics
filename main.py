#!/usr/bin/env python3
"""
Project 3: Pharmacogenomics Pipeline - Main Entry Point
"""
import argparse
import os
import sys
from datetime import datetime
from vcf_parser import read_vcf
from variant_filter import filter_variants
from gene_filter import filter_pharmacogenes
from allele_caller import call_alleles
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
        default="output/pgx_clinical_report.html",  # ← now inside output/
        help="Output HTML report path (default: output/pgx_clinical_report.html)"
    )
    parser.add_argument("--min_qual",  type=float, default=20.0,
                        help="Minimum QUAL score (default: 20.0)")
    parser.add_argument("--min_depth", type=int,   default=10,
                        help="Minimum read depth DP (default: 10)")

    args = parser.parse_args()

    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    print("\n" + "="*60)
    print("STARTING PHARMACOGENOMICS PIPELINE")
    print("="*60)

    # 2. Read and parse the VCF file
    try:
        print(f"[1/4] Reading VCF file: {args.input} ...")
        all_variants = list(read_vcf(args.input))
        print(f"      Total variants parsed: {len(all_variants)}")
    except FileNotFoundError:
        print(f"Error: '{args.input}' not found. Check your path or use -i to specify one.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error while parsing VCF: {e}")
        sys.exit(1)

    print(f"[2/4] Filtering by quality (QUAL >= {args.min_qual}, DP >= {args.min_depth})...")
    passed_variants, rejected_stats = filter_variants(
        all_variants, min_qual=args.min_qual, min_depth=args.min_depth
    )
    print(f"      Passed QC: {len(passed_variants)}")
    print(f"      Failed QC: {len(rejected_stats)}")

    print("[3/4] Filtering to known pharmacogenes (CYP2D6, CYP2C19, etc.)...")
    pgx_variants = filter_pharmacogenes(passed_variants)
    print(f"      Found {len(pgx_variants)} variants in pharmacogenes")


    print("[4/4] Calling star alleles and generating HTML report...")
    alleles = call_alleles(pgx_variants)
    generate_html_report(alleles, args.output)

    print("="*60)
    print("PIPELINE COMPLETE!")
    print(f"Report saved to: {args.output}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()