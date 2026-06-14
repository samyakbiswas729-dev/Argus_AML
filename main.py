from src.case_management import create_cases
import pandas as pd

from src.aml_rules import calculate_rule_score
from src.risk_engine import calculate_client_risk
from src.anomaly_detection import detect_anomalies


print("=" * 60)
print("ARGUS AML STARTING...")
print("=" * 60)

# -------------------------
# LOAD DATA
# -------------------------

clients = pd.read_csv(
    "data/clients_with_fatf_ofac.csv"
)

transactions = pd.read_csv(
    "data/transactions_with_fatf_ofac.csv"
)

# -------------------------
# CLIENT RISK
# -------------------------

clients["client_risk_score"] = clients.apply(
    calculate_client_risk,
    axis=1
)

# -------------------------
# TRANSACTION RISK
# -------------------------

transactions["transaction_risk_score"] = transactions.apply(
    calculate_rule_score,
    axis=1
)

# -------------------------
# MERGE
# -------------------------

merged = transactions.merge(
    clients[
        [
            "client_id",
            "client_risk_score"
        ]
    ],
    on="client_id",
    how="left"
)

# -------------------------
# OVERALL RISK
# -------------------------

merged["overall_risk_score"] = (
    merged["transaction_risk_score"]
    +
    merged["client_risk_score"]
)

# -------------------------
# ANOMALY DETECTION
# -------------------------

merged = detect_anomalies(merged)

# -------------------------
# RISK LEVEL
# -------------------------

def assign_risk_level(score):

    if score >= 70:
        return "HIGH"

    elif score >= 40:
        return "MEDIUM"

    return "LOW"


merged["risk_level"] = merged[
    "overall_risk_score"
].apply(assign_risk_level)

# -------------------------
# ALERTS
# -------------------------

alerts = merged[
    (
        merged["overall_risk_score"] >= 50
    )
    |
    (
        merged["anomaly_flag"] == -1
    )
]

# -------------------------
# SAVE OUTPUTS
# -------------------------

merged.to_csv(
    "outputs/argus_aml_results.csv",
    index=False
)

alerts.to_csv(
    "outputs/aml_alerts.csv",
    index=False
)

# =====================================
# CASE MANAGEMENT
# =====================================

cases = create_cases(alerts)
country_map = {
    "IR": "Iran",
    "KP": "North Korea",
    "SY": "Syria",
    "RU": "Russia",
    "SD": "Sudan",
    "VE": "Venezuela",
    "LB": "Lebanon",
    "CN": "China",
    "IN": "India",
    "SG": "Singapore",
    "US": "United States",
    "UK": "United Kingdom",
    "AE": "United Arab Emirates",
    "AF": "Afghanistan",
    "AU": "Australia",
    "CA": "Canada",
    "CH": "Switzerland",
    "DE": "Germany",
    "FR": "France",
    "JP": "Japan",
    "NL": "Netherlands"
}

cases["client_country"] = (
    cases["client_country"]
    .replace(country_map)
)

cases["counterparty_country"] = (
    cases["counterparty_country"]
    .replace(country_map)
)

cases.to_csv(
    "outputs/cases.csv",
    index=False
)

print(
    f"Cases Generated: {len(cases)}"
)


# -------------------------
# SUMMARY
# -------------------------

print("\n")
print("=" * 60)
print("ARGUS AML SUMMARY")
print("=" * 60)

print(f"Total Transactions : {len(merged)}")
print(f"AML Alerts         : {len(alerts)}")
print(f"Anomalies Detected : {(merged['anomaly_flag'] == -1).sum()}")
print(f"High Risk Txns     : {(merged['risk_level'] == 'HIGH').sum()}")
print(f"Medium Risk Txns   : {(merged['risk_level'] == 'MEDIUM').sum()}")
print(f"Low Risk Txns      : {(merged['risk_level'] == 'LOW').sum()}")

print("\nARGUS AML EXECUTION COMPLETED")