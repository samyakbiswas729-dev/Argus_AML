def calculate_client_risk(row):

    score = 0

    if row["pep_flag"] == 1:
        score += 25

    if row["sanctions_flag"] == 1:
        score += 30

    if row["fatf_country_flag"] == 1:
        score += 20

    score += row["ownership_opacity_score"] * 20

    return min(score, 100)
