# gene_filter.py

PHARMACOGENES = {
    'CYP2D6':  {'chrom': '22', 'start': 42120962, 'end': 42131727},
    'CYP2C19': {'chrom': '10', 'start': 94762536, 'end': 94922264},
    'CYP2C9':  {'chrom': '10', 'start': 94938544, 'end': 94990149},
    'VKORC1':  {'chrom': '16', 'start': 31090260, 'end': 31095980},
    'CYP4F2':  {'chrom': '19', 'start': 15877893, 'end': 15900528},
    'TPMT':    {'chrom': '6',  'start': 18128311, 'end': 18155348},
    'DPYD':    {'chrom': '1',  'start': 97077743, 'end': 97995000},
}

def filter_pharmacogenes(variants):
    """
    Takes an iterable of variant dicts (from vcf_parser.read_vcf)
    Returns only variants that fall inside one of our pharmacogenes,
    tagged with which gene they belong to
    """
    gene_variants = []

    for var in variants:
        chrom = var['CHROM'].replace('chr', '')
        pos = var['POS']

        for gene_name, coords in PHARMACOGENES.items():
            if chrom == coords['chrom'] and coords['start'] <= pos <= coords['end']:
                var['GENE'] = gene_name
                gene_variants.append(var)
                break

    return gene_variants



