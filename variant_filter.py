def filter_variants(variants, min_qual=20, min_depth=10):
    """
    Filter variants by quality metrics (QUAL, DP, FILTER).
    Returns (passed_list, rejected_list).
    """
    filtered = []
    rejected = []

    for var in variants:
        # Fetch values safely, default to None if they don't exist
        qual = var.get('QUAL')
        depth = var['info_dict'].get('dp')

        reasons = []
        
        # Only check QUAL if it actually exists AND is a real number (skips 0 and '.')
        if qual is not None and qual not in (0, 0.0) and qual < min_qual:
            reasons.append(f"Low QUAL ({qual})")
        
        # Only check DP if it actually exists in the VCF
        if depth is not None and depth not in (0, 0.0) and depth < min_depth:
            reasons.append(f"Low DP ({depth})")
            
        # This is the new fix! Allow both 'PASS' and '.' to pass the filter
        if var.get('FILTER') not in [None, 'PASS', '.']:
            reasons.append(f"FILTER={var.get('FILTER')}")

        if not reasons:
            filtered.append(var)
        else:
            rejected.append({
                'variant': var,
                'reasons': reasons
            })

    return filtered, rejected