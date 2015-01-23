
def splits_match_total(total_mins,  total_secs,  total_mils,
                       split1_mins, split1_secs, split1_mils,
                       split2_mins, split2_secs, split2_mils,
                       split3_mins, split3_secs, split3_mils):
    
    total  = total_mils  + (total_secs  * 1000) + (total_mins  * 60 * 1000)
    split1 = split1_mils + (split1_secs * 1000) + (split1_mins * 60 * 1000)
    split2 = split2_mils + (split2_secs * 1000) + (split2_mins * 60 * 1000)
    split3 = split3_mils + (split3_secs * 1000) + (split3_mins * 60 * 1000)

    return (total == (split1 + split2 + split3))
