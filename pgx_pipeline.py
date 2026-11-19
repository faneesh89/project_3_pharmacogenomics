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

def build_patient_report(gene, allele_info_list):
    diplotype = build_diplotype([a['allele'] for a in allele_info_list])
    phenotype = predict_phenotype(gene, allele_info_list)
    recommendation = get_recommendation(gene, phenotype)
    return {
        'gene': gene,
        'alleles_found': [a['allele'] for a in allele_info_list],
        'diplotype': diplotype,
        'phenotype': phenotype,
        'recommendation': recommendation
    }
