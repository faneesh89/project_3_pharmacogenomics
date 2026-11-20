# pgx_pipeline.py
#
# Turns called star alleles into patient-level answers:

from allele_caller import ACTIVITY_SCORES

# ------------------------------------------------------------
# DIPLOTYPE BUILDER
# ------------------------------------------------------------

def _allele_sort_key(allele_name):
    """Canonical order key: by the allele number ('*2' -> 2,
    '*17' -> 17); alleles without a leading number sort last."""
    digits = ''
    for ch in allele_name:
        if ch.isdigit():
            digits += ch
        else:
            break
    if digits:
        return (int(digits), allele_name)
    return (9999, allele_name)


def build_diplotype(allele_list):
    """Build a diplotype string from called alleles, in canonical
    order, so '*3/*2' and '*2/*3' are the same string.

    A diplotype needs exactly two alleles: one called allele means the
    other chromosome carries the reference *1, zero called alleles
    means *1/*1. More than two called alleles cannot be resolved into
    a diplotype without phasing, so they are all joined and the
    phenotype lookup will report Unknown."""
    alleles = list(allele_list)
    if not alleles:
        return '*1/*1'
    if len(alleles) == 1:
        alleles.append('*1')
    return '/'.join(sorted(alleles, key=_allele_sort_key))


# -------------------------------------
# PHENOTYPE PREDICTOR
# --------------------------------------

PHENOTYPE_MAP = {
    'CYP2C19': {
        '*1/*1': 'Normal Metabolizer',
        '*1/*2': 'Intermediate Metabolizer',
        '*1/*3': 'Intermediate Metabolizer',
        '*2/*2': 'Poor Metabolizer',
        '*2/*3': 'Poor Metabolizer',
        '*3/*3': 'Poor Metabolizer',
        '*17/*17': 'Ultrarapid Metabolizer',
        '*1/*17': 'Rapid Metabolizer',
        '*2/*17': 'Intermediate Metabolizer',  # CPIC says IM, NOT normal!
    },
    'CYP2D6': {
        '*1/*1': 'Normal Metabolizer',
        '*1/*4': 'Intermediate Metabolizer',
        '*4/*4': 'Poor Metabolizer',
        '*1/*10': 'Intermediate Metabolizer',
        '*10/*10': 'Intermediate Metabolizer',
        '*1/*17': 'Intermediate Metabolizer',
        '*17/*17': 'Intermediate Metabolizer',
    },
    'CYP2C9': {
        '*1/*1': 'Normal Metabolizer',
        '*1/*2': 'Intermediate Metabolizer',
        '*1/*3': 'Intermediate Metabolizer',
        '*2/*2': 'Poor Metabolizer',
        '*2/*3': 'Poor Metabolizer',
        '*3/*3': 'Poor Metabolizer',
    },
    'TPMT': {
        '*1/*1': 'Normal Metabolizer',
        '*1/*2': 'Intermediate Metabolizer',
        '*1/*3A': 'Intermediate Metabolizer',
        '*1/*3B': 'Intermediate Metabolizer',
        '*1/*3C': 'Intermediate Metabolizer',
        '*2/*2': 'Poor Metabolizer',
        '*3A/*3A': 'Poor Metabolizer',
        '*3B/*3C': 'Poor Metabolizer',
    },
    'DPYD': {
        'Normal': 'Normal Metabolizer',
        'Intermediate': 'Intermediate Metabolizer',
        'Poor': 'Poor Metabolizer',
    }
}


def predict_phenotype(gene, allele_info_list):
    """Predict phenotype for one gene from its called alleles.

    DPYD uses the CPIC activity-score system: each called allele
    contributes its function score, missing copies are *1 (score 1.0),
    and the total maps to Normal / Intermediate / Poor. Every other
    gene uses a direct diplotype lookup."""
    n_called = len(allele_info_list)

    if gene == 'DPYD':
        if n_called == 0:
            total_score = 2.0
        elif n_called <= 2:
            total_score = 0.0
            for allele_info in allele_info_list:
                function = allele_info.get('function', 'normal')
                total_score += ACTIVITY_SCORES.get(function, 0.0)
            total_score += (2 - n_called) * 1.0
        else:
            return 'Unknown Phenotype'

        if total_score >= 2.0:
            return 'Normal Metabolizer'
        elif total_score >= 1.0:
            return 'Intermediate Metabolizer'
        else:
            return 'Poor Metabolizer'

    allele_names = [a['allele'] for a in allele_info_list]
    if gene == 'VKORC1':
            functions = {a.get('function', 'normal') for a in allele_info_list}
            if 'sensitive' in functions and 'resistant' in functions:
                return 'Intermediate'
            if 'sensitive' in functions:
                return 'Sensitive'
            if 'resistant' in functions:
                return 'Resistant'
            return 'Normal'
    diplotype = build_diplotype(allele_names)

    if gene in PHENOTYPE_MAP and diplotype in PHENOTYPE_MAP[gene]:
        return PHENOTYPE_MAP[gene][diplotype]

    return "Unknown Phenotype"


# -----------------------------
# RECOMMENDATION ENGINE
# -----------------------------

RECOMMENDATION_MAP = {
    'CYP2C19': {
        'Poor Metabolizer': '⚠️ AVOID Clopidogrel. Use Prasugrel or Ticagrelor.',
        'Intermediate Metabolizer': 'Standard dose, monitor efficacy.',
        'Normal Metabolizer': 'Standard dose.',
        'Ultrarapid Metabolizer': 'Standard dose.'
    },
    'CYP2D6': {
        'Poor Metabolizer': '⚠️ AVOID Codeine. No pain relief. Consider Morphine.',
        'Intermediate Metabolizer': 'Reduced efficacy. Monitor and consider alternative.',
        'Normal Metabolizer': 'Standard dose.',
        'Ultrarapid Metabolizer': '⚠️ AVOID Codeine. Risk of respiratory depression!'
    },
    'CYP2C9': {
        'Poor Metabolizer': '⚠️ Warfarin: Reduce dose by 50-70%. High bleeding risk.',
        'Intermediate Metabolizer': 'Warfarin: Reduce dose by 20-40%. Monitor INR closely.',
        'Normal Metabolizer': 'Standard warfarin dose.'
    },
    'VKORC1': {
        'Sensitive': '⚠️ Warfarin: Significantly lower dose (A/A = ~3x less).',
        'Intermediate': 'Warfarin: Reduced dose. Monitor INR.',
        'Normal': 'Standard warfarin dose.'
    },
    'TPMT': {
        'Poor Metabolizer': '⚠️ AVOID Azathioprine/6-MP or reduce to 10% dose. FATAL bone marrow suppression!',
        'Intermediate Metabolizer': 'Reduce dose 30-50%. Monitor CBC closely.',
        'Normal Metabolizer': 'Standard dose.'
    },
    'DPYD': {
        'Poor Metabolizer': '⚠️ AVOID 5-FU/Capecitabine. EU-mandated testing!',
        'Intermediate Metabolizer': 'Reduce dose 25-50%. Monitor toxicity closely.',
        'Normal Metabolizer': 'Standard dose.'
    }
}


def get_recommendation(gene, phenotype):
    if gene in RECOMMENDATION_MAP and phenotype in RECOMMENDATION_MAP[gene]:
        return RECOMMENDATION_MAP[gene][phenotype]
    return "No specific recommendation."


# --------------------
# PATIENT REPORT
# --------------------

VKORC1_VARIANT_LABELS = {
    'sensitive': '-1639A (sensitive: lower dose)',
    'resistant': 'D36Y (resistant: higher dose)',
}


def vkorc1_report_line(allele_info_list):
    """Name the actual VKORC1 variants carried, with their dose
    direction, so the step-5 line explains itself instead of
    saying 'No specific recommendation'."""
    parts = [VKORC1_VARIANT_LABELS[a.get('function')]
             for a in allele_info_list
             if a.get('function') in VKORC1_VARIANT_LABELS]
    if not parts:
        return 'No VKORC1 sensitivity/resistance variants called.'
    return 'Warfarin: carries ' + ' + '.join(parts) + '.'



def build_patient_report(gene, allele_info_list):
    diplotype = build_diplotype([a['allele'] for a in allele_info_list])
    phenotype = predict_phenotype(gene, allele_info_list)
    recommendation = get_recommendation(gene, phenotype)
    if gene == 'VKORC1':
        recommendation = vkorc1_report_line(allele_info_list)
    return {
        'gene': gene,
        'alleles_found': [a['allele'] for a in allele_info_list],
        'diplotype': diplotype,
        'phenotype': phenotype,
        'recommendation': recommendation
    }

# --------------------
# WARFARIN MODULE
# --------------------
# Warfarin dosing is a product of three forces: CYP2C9 clearance,
# VKORC1 target sensitivity and CYP4F2 vitamin K metabolism.
# Each gene contributes a multiplicative factor to the standard dose.

WARFARIN_DOSE_FACTORS = {
    'CYP2C9': {
        'Normal Metabolizer': 1.0,
        'Intermediate Metabolizer': 0.7,
        'Poor Metabolizer': 0.4,
    },
    'VKORC1': {
        'sensitive': 0.6,   # -1639 A allele: lower VKORC1 expression
        'resistant': 1.3,   # resistance variant: more drug needed
        'normal': 1.0,
    },
    'CYP4F2': {
        'carrier': 1.1,     # *3: slower vitamin K metabolism
        'normal': 1.0,
    },
}


def vkorc1_combined_factor(vkorc1_alleles):
    """Multiply the dose factor of every called VKORC1 variant.

    Replaces the old 'sensitive wins' rule, which dropped one
    variant from the report. Each called variant now contributes
    its own factor:
        -1639A (sensitive) x0.6, D36Y (resistant) x1.3
        both together -> 0.6 * 1.3 = 0.78
    Limitation: treats variants as independent effects and does
    not phase haplotypes — research estimate only.
    """
    factor = 1.0
    for allele in vkorc1_alleles:
        status = allele.get('function', 'normal')
        factor *= WARFARIN_DOSE_FACTORS['VKORC1'].get(status, 1.0)
    return round(factor, 3)


def resolve_cyp4f2_status(allele_info_list):
    """CYP4F2*3 carriers need a higher warfarin dose."""
    if any(a['function'] == 'decreased' for a in allele_info_list):
        return 'carrier'
    return 'normal'


def build_warfarin_report(alleles, patient_rows):
    """Combine CYP2C9, VKORC1 and CYP4F2 into one warfarin dose
    recommendation. Returns None if CYP2C9 has no phenotype."""
    phenotypes = {row['gene']: row['phenotype'] for row in patient_rows}
    cyp2c9_phenotype = phenotypes.get('CYP2C9')

    if cyp2c9_phenotype not in WARFARIN_DOSE_FACTORS['CYP2C9']:
        return None

    factors = {
        'CYP2C9': WARFARIN_DOSE_FACTORS['CYP2C9'][cyp2c9_phenotype],
        'VKORC1': vkorc1_combined_factor(alleles.get('VKORC1', [])),
        'CYP4F2': WARFARIN_DOSE_FACTORS['CYP4F2'][
            resolve_cyp4f2_status(alleles.get('CYP4F2', []))],
    }

    net = 1.0
    for factor in factors.values():
        net *= factor

    if net <= 0.35:
        verdict = 'Very low dose expected - high bleeding risk, extended INR monitoring'
    elif net <= 0.70:
        verdict = 'Substantially reduced dose from standard, close INR monitoring'
    elif net <= 0.95:
        verdict = 'Slightly reduced dose, routine INR monitoring'
    elif net <= 1.15:
        verdict = 'Standard dose expected'
    else:
        verdict = 'Higher dose than standard likely needed, watch for under-anticoagulation'

    return {
        'cyp2c9_phenotype': cyp2c9_phenotype,
        'factors': factors,
        'net_factor': round(net, 2),
        'verdict': verdict + ' [genotype-based dose modifiers - research estimate, not medical advice]',
    }
