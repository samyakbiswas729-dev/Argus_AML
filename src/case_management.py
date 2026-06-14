
import pandas as pd

def create_cases(alerts):

    cases = alerts.copy()

    cases["case_id"] = [
        f"CASE-{i:05d}"
        for i in range(1, len(cases) + 1)
    ]

    cases["status"] = "OPEN"

    cases["priority"] = cases["overall_risk_score"].apply(
        lambda x: "HIGH" if x >= 70 else "MEDIUM"
    )

    cases["investigator"] = "Unassigned"

    return cases

    cases["investigator"] = "Unassigned"

    return cases