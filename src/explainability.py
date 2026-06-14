def explain_alert(row):

    reasons = []

    if row["ofac_match_flag"] == 1:
        reasons.append("OFAC Match")

    if row["fatf_country_flag"] == 1:
        reasons.append("FATF High-Risk Country")

    if row["structuring_pattern_flag"] == 1:
        reasons.append("Structuring Pattern")

    if row["rapid_movement_flag"] == 1:
        reasons.append("Rapid Movement")

    if row["trade_mispricing_flag"] == 1:
        reasons.append("Trade Mispricing")

    if row["overall_risk_score"] >= 70:
        reasons.append("High Risk Score")

    return ", ".join(reasons)