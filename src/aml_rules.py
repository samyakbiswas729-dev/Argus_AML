def calculate_rule_score(row):

    score = 0

    if row["ofac_match_flag"] == 1:
        score += 40

    if row["fatf_country_flag"] == 1:
        score += 20

    if row["structuring_pattern_flag"] == 1:
        score += 15

    if row["rapid_movement_flag"] == 1:
        score += 15

    if row["trade_mispricing_flag"] == 1:
        score += 10

    return score
