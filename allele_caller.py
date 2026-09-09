# allele_database.py

ALLELE_DEFINITIONS = {

    # ═══════════════════════════════════════════════════════════════════
    # CYP2D6 — Chromosome 22
    # ═══════════════════════════════════════════════════════════════════
    'CYP2D6': {
        'rs3892097': {
            'allele': '*4',
            'ref': 'G',
            'alt': 'A',
            'function': 'no_function',
            'note': 'c.506-1G>A — splice site defect, most common loss-of-function in Europeans (~20% frequency). No residual enzyme activity.'
        },
        'rs1065852': {
            'allele': '*10',
            'ref': 'C',
            'alt': 'T',
            'function': 'decreased',
            'note': 'c.100C>T (Pro34Ser) — most common decreased-function allele in East Asian populations (~50% frequency).'
        },
        'rs16947': {
            'allele': '*2',
            'ref': 'C',
            'alt': 'A',
            'function': 'normal',
            'note': 'c.2850C>T — normal function, but must co-occur with rs1135840 to fully define *2. Alone classified as normal activity.'
        },
        'rs28371706': {
            'allele': '*17',
            'ref': 'C',
            'alt': 'C',
            'function': 'decreased',
            'note': 'c.1023C>T (Cys337Arg) — decreased function, common in African populations (~34% frequency).'
        },
        'rs28371725': {
            'allele': '*41',
            'ref': 'G',
            'alt': 'T',
            'function': 'decreased',
            'note': 'c.2988G>A — splicing defect, decreased function. Often seen with gene duplications.'
        },
        'rs35742686': {
            'allele': '*3',
            'ref': 'A',
            'alt': 'del',
            'function': 'no_function',
            'note': '2549delA — frameshift mutation, no function.'
        },
        # NOTE: CYP2D6*5 = ENTIRE GENE DELETION — requires CNV analysis (not detected by SNP lookup)
        # NOTE: CYP2D6*1xN = GENE DUPLICATION — requires CNV analysis (not detected by SNP lookup)
    },

    # ═══════════════════════════════════════════════════════════════════
    # CYP2C19 — Chromosome 10
    # ═══════════════════════════════════════════════════════════════════
    'CYP2C19': {
        'rs4244285': {
            'allele': '*2',
            'ref': 'G',
            'alt': 'A',
            'function': 'no_function',
            'note': 'c.681G>A — aberrant splicing, premature stop codon. Most common loss-of-function allele (~15-30% frequency). FDA Black Box Warning for clopidogrel in carriers.'
        },
        'rs4986893': {
            'allele': '*3',
            'ref': 'G',
            'alt': 'A',
            'function': 'no_function',
            'note': 'c.636G>A (Trp212Ter) — premature stop codon, no function. More common in Asian populations (~5-9%).'
        },
        'rs12248560': {
            'allele': '*17',
            'ref': 'C',
            'alt': 'T',
            'function': 'increased',
            'note': 'c.-806C>T — increased transcription, increased enzyme activity. IMPORTANT: *17 does NOT compensate for *2 (see CPIC Table 1). *2/*17 is still Intermediate Metabolizer!'
        },
        'rs28399504': {
            'allele': '*4',
            'ref': 'G',
            'alt': 'A',
            'function': 'no_function',
            'note': 'c.1A>G — start codon loss, no protein produced.'
        },
    },

    # ═══════════════════════════════════════════════════════════════════
    # CYP2C9 — Chromosome 10
    # ═══════════════════════════════════════════════════════════════════
    'CYP2C9': {
        'rs1799853': {
            'allele': '*2',
            'ref': 'C',
            'alt': 'T',
            'function': 'decreased',
            'note': 'c.430C>T (Arg144Cys) — reduced enzyme activity (~12% of normal). Common in Europeans (~11%). Slower warfarin clearance → bleeding risk at standard dose.'
        },
        'rs1057910': {
            'allele': '*3',
            'ref': 'A',
            'alt': 'C',
            'function': 'no_function',
            'note': 'c.1075A>C (Ile359Leu) — severely reduced activity (~5% of normal). Most clinically important CYP2C9 variant. Europeans ~7%, Asians ~2-4%.'
        },
        'rs56165452': {
            'allele': '*5',
            'ref': 'C',
            'alt': 'T',
            'function': 'no_function',
            'note': 'c.1080C>G (Asp360Glu) — no function, rare variant.'
        },
        'rs28371686': {
            'allele': '*6',
            'ref': 'A',
            'alt': 'del',
            'function': 'no_function',
            'note': '818delA — frameshift, no function.'
        },
    },

    # ═══════════════════════════════════════════════════════════════════
    # VKORC1 — Chromosome 16 (Pharmacodynamic gene — Warfarin target)
    # ═══════════════════════════════════════════════════════════════════
    'VKORC1': {
        'rs9923231': {
            'allele': 'A',
            'ref': 'G',
            'alt': 'T',
            'function': 'sensitive',
            'note': '-1639G>A — VKORC1 promoter variant. A allele reduces VKORC1 expression → more sensitive to warfarin → LOWER dose needed. A/A genotype needs ~3x less warfarin than G/G!'
        },
        'rs61742245': {
            'allele': 'variant',
            'ref': 'C',
            'alt': 'A',
            'function': 'resistant',
            'note': 'Associated with warfarin resistance — higher dose needed.'
        },
    },

    # ═══════════════════════════════════════════════════════════════════
    # CYP4F2 — Chromosome 19 (Vitamin K metabolism — warfarin dose modifier)
    # ═══════════════════════════════════════════════════════════════════
    'CYP4F2': {
        'rs2108622': {
            'allele': '*3',
            'ref': 'G',
            'alt': 'T',
            'function': 'decreased',
            'note': 'c.1297G>A (Val433Met) — reduced Vitamin K metabolism. Vitamin K accumulates → competes with warfarin → need HIGHER warfarin dose. ~30% of Europeans carry this!'
        },
    },

    # ═══════════════════════════════════════════════════════════════════
    # TPMT — Chromosome 6 (Thiopurine inactivation — FATAL if missed)
    # ═══════════════════════════════════════════════════════════════════
    'TPMT': {
        'rs1800462': {
            'allele': '*2',
            'ref': 'G',
            'alt': 'C',
            'function': 'no_function',
            'note': 'c.238G>C (Ala80Pro) — no enzyme activity. Less common than *3A in most populations.'
        },
        'rs1800460': {
            'allele': '*3A_part1',
            'ref': 'G',
            'alt': 'A',
            'function': 'no_function',
            'note': 'c.460G>A (Ala154Thr) — ONE of TWO variants defining *3A. Must co-occur with rs1142345 for *3A classification. ALONE = *3B allele (still decreased function).'
        },
        'rs1142345': {
            'allele': '*3A_part2',
            'ref': 'A',
            'alt': 'C',
            'function': 'no_function',
            'note': 'c.719A>G (Tyr240Cys) — ONE of TWO variants defining *3A. Must co-occur with rs1800460 for *3A classification. ALONE = *3C allele (still decreased function). *3A is most common nonfunctional TPMT allele (~5% Europeans).'
        },
        'rs1800584': {
            'allele': '*4',
            'ref': 'G',
            'alt': 'A',
            'function': 'no_function',
            'note': 'c.626-1G>A — splice site defect, no function. Rare.'
        },
    },

    # ═══════════════════════════════════════════════════════════════════
    # DPYD — Chromosome 1 (5-FU clearance — EU-mandated testing since 2020)
    # ═══════════════════════════════════════════════════════════════════
    'DPYD': {
        'rs3918290': {
            'allele': '*2A',
            'ref': 'G',
            'alt': 'A',
            'function': 'no_function',
            'note': 'c.1905+1G>A (IVS14+1G>A) — splice site defect, exon 14 skipping, no functional enzyme. Most studied DPYD variant. Activity Score = 0. EU mandated testing!'
        },
        'rs55886062': {
            'allele': '*13',
            'ref': 'T',
            'alt': 'C',
            'function': 'no_function',
            'note': 'c.1679T>G (Ile560Ser) — severely reduced activity. Activity Score = 0. Rare but clinically critical.'
        },
        'rs67376798': {
            'allele': 'c.2846A>T',
            'ref': 'A',
            'alt': 'T',
            'function': 'decreased',
            'note': 'c.2846A>T (Asp949Val) — decreased function. Activity Score = 0.5. EU-mandated pre-treatment testing.'
        },
        'rs56038477': {
            'allele': 'c.1236G>A',
            'ref': 'G',
            'alt': 'A',
            'function': 'decreased',
            'note': 'c.1236G>A/HapB3 — decreased function. Activity Score = 0.5. Often occurs with rs75017182 as part of HapB3 haplotype.'
        },
    },
}

# ═══════════════════════════════════════════════════════════════════════
# ACTIVITY SCORES — for DPYD phenotype calculation
# ═══════════════════════════════════════════════════════════════════════

ACTIVITY_SCORES = {
    'normal': 1.0,
    'decreased': 0.5,
    'no_function': 0.0,
    'increased': 1.5,
    'sensitive': None,
    'resistant': None,
}


def get_rs_number(variant):
    """
    Extract rs number from VCF ID column first, then fall back
    to the RS key in the INFO field (ClinVar stores its own IDs
    in the ID column, but rs numbers in INFO['RS']).
    """
    # Try ID column first (standard VCF approach)
    id_field = variant.get('ID', '.')
    if id_field and id_field != '.':
        for part in id_field.split(';'):
            part = part.strip()
            if part.startswith('rs'):
                return part

    # Fall back to INFO field RS key (ClinVar-specific)
    info = variant.get('info_dict', {})
    rs_raw = info.get('RS', info.get('DBSNP', None))
    if rs_raw and rs_raw != '.':
        try:
            # ClinVar stores RS as a float (e.g. 3918290.0)
            # Convert: 3918290.0 → 'rs3918290'
            rs_num = str(int(float(rs_raw)))
            return f'rs{rs_num}'
        except (ValueError, TypeError):
            return None

    return None

def call_allele_for_variant(variant):
    """
    Takes ONE variant dict (already tagged with 'GENE' from gene_filter.py)
    Returns allele info dict if this variant matches a known star allele,
    otherwise returns None.
 
    Matching strategy:
    1. Primary: match by RS NUMBER (stable, build-independent)
    2. The ALT allele in the VCF must match our expected variant base
 
    Returns dict like:
    {
        'allele': '*4',
        'function': 'no_function',
        'rs': 'rs3892097',
        'note': '...'
    }
    or None if not a recognized allele-defining variant.
    """

    gene = variant.get('GENE')
    if not gene or gene not in ALLELE_DEFINITIONS:
        return None

    rs = get_rs_number(variant)
    if not rs : 
        return None

    gene_defs = ALLELE_DEFINITIONS[gene]
    if rs not in gene_defs:
        return None

    definitions = gene_defs[rs]

    vcf_alt = variant.get('ALT','')
    expected_alt = definitions.get('alt','')

    if expected_alt == 'del':
        ref = variant.get('REF','')
        if len(vcf_alt) >= len(ref):
            return None

    elif expected_alt not in ('',None) and vcf_alt != expected_alt:
        return None

    return{
        'allele' : definitions['allele'],
        'function': definitions['function'],
        'rs' : rs,
        'note' : definitions['note']
    }


def call_alleles_for_all_variants(pgx_variants):

    results = {}

    for gene in ALLELE_DEFINITIONS.keys():
        results[gene] = []

    for variant in pgx_variants:
        allele_info = call_allele_for_variant(variant)
        if allele_info:
            gene = variant.get('GENE')          
            if gene in results:
                results[gene].append(allele_info)
    return results

def summarize_allele_results(allele_results):
    summary = {}

    for gene, alleles in allele_results.items():
        if not alleles:
            summary[gene] = {
                'alleles_found': [],
                'count': 0,
                'note': 'No known tag variants found — assuming *1 (reference)'
            }
        else:
            allele_names = [a['allele'] for a in alleles]
            functions = [a['function'] for a in alleles]
        summary[gene] = {
                'alleles_found': allele_names,
                'count': len(alleles),
                'functions': functions,
                'note': f"Found {len(alleles)} known variant(s)"
            }
    return summary

def resolve_tpmt_alleles(tpmt_alleles):

    allele_name = [a['allele'] for a in tpmt_alleles]

    has_part1 = '*3A_part1' in allele_name
    has_part2 = '*3A_part2' in allele_name

    resolved = []
    for a in tpmt_alleles:
        if a['allele'] == '3A_part1':
            if has_part2:
                resolved.append({**a, 'allele': '*3A', 'function': 'no_function',
                                  'note': '*3A confirmed (both rs1800460 + rs1142345 present)'})\

            else:
                resolved.append({**a, 'allele': '*3B', 'function': 'decreased',
                                  'note': '*3B (rs1800460 alone, no rs1142345)'})
        elif a['allele'] == '*3A_part2':
            if has_part1:
                pass
            else:
                resolved.append({**a, 'allele': '*3C', 'function': 'decreased',
                                  'note': '*3C (rs1142345 alone, no rs1800460)'})
        else:
            resolved.append(a)

    return resolved

def call_alleles(pgx_variants):
    raw = call_alleles_for_all_variants(pgx_variants)
    
    if 'TPMT' in raw:
        raw['TPMT'] = resolve_tpmt_alleles(raw['TPMT'])
    
    return raw