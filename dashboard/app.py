from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Argus AML",
    page_icon="🛡️",
    layout="wide"
)

# ==================================================
# FILE PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RESULTS_FILE = BASE_DIR / "outputs" / "argus_aml_results.csv"
ALERTS_FILE = BASE_DIR / "outputs" / "aml_alerts.csv"
CLIENTS_FILE = BASE_DIR / "data" / "clients_with_fatf_ofac.csv"
CASES_FILE = BASE_DIR / "outputs" / "cases.csv"

# ==================================================
# LOAD DATA
# ==================================================

df = pd.read_csv(RESULTS_FILE)
alerts = pd.read_csv(ALERTS_FILE)
clients = pd.read_csv(CLIENTS_FILE)

try:
    cases = pd.read_csv(CASES_FILE)
except:
    cases = pd.DataFrame()

# ==================================================
# COUNTRY CODE MAPPING
# ==================================================

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

for frame in [df, alerts]:

    if "client_country" in frame.columns:
        frame["client_country"] = (
            frame["client_country"]
            .replace(country_map)
        )

    if "counterparty_country" in frame.columns:
        frame["counterparty_country"] = (
            frame["counterparty_country"]
            .replace(country_map)
        )

if "country" in clients.columns:
    clients["country"] = (
        clients["country"]
        .replace(country_map)
    )

# ==================================================
# HEADER
# ==================================================

st.title("🛡️ Argus AML")

st.subheader(
    "AI-Powered Transaction Monitoring & Financial Crime Investigation Platform"
)

# ==================================================
# EXECUTIVE KPIs
# ==================================================

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Transactions",
    f"{len(df):,}"
)

k2.metric(
    "AML Alerts",
    f"{len(alerts):,}"
)

k3.metric(
    "Anomalies",
    f"{len(df[df['anomaly_flag'] == -1]):,}"
)

k4.metric(
    "High Risk Alerts",
    f"{len(df[df['risk_level'] == 'HIGH']):,}"
)

st.divider()

# ==================================================
# CLIENT RISK INDICATORS
# ==================================================

st.subheader("Client Risk Indicators")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "PEP Clients",
    int(clients["pep_flag"].sum())
)

c2.metric(
    "Sanctioned Clients",
    int(clients["sanctions_flag"].sum())
)

c3.metric(
    "FATF Country Clients",
    int(clients["fatf_country_flag"].sum())
)

c4.metric(
    "High Opacity Clients",
    int(
        (
            clients["ownership_opacity_score"] >= 0.7
        ).sum()
    )
)

st.divider()

# ==================================================
# ALERT BREAKDOWN
# ==================================================

st.subheader("Alert Breakdown")

a1, a2, a3, a4 = st.columns(4)

a1.metric(
    "OFAC Matches",
    int(df["ofac_match_flag"].sum())
)

a2.metric(
    "FATF Alerts",
    int(df["fatf_country_flag"].sum())
)

a3.metric(
    "Structuring Alerts",
    int(df["structuring_pattern_flag"].sum())
)

a4.metric(
    "Rapid Movement Alerts",
    int(df["rapid_movement_flag"].sum())
)

st.divider()

# ==================================================
# RISK DISTRIBUTION
# ==================================================

st.subheader("Risk Distribution")

risk_counts = (
    df["risk_level"]
    .value_counts()
    .reset_index()
)

risk_counts.columns = [
    "Risk Level",
    "Count"
]

fig = px.pie(
    risk_counts,
    names="Risk Level",
    values="Count",
    hole=0.4
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================================
# RISK SCORE HISTOGRAM
# ==================================================

st.subheader(
    "Risk Score Distribution"
)

fig2 = px.histogram(
    df,
    x="overall_risk_score",
    nbins=30,
    title="Overall Risk Score Distribution"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==================================================
# TOP RISK CLIENTS
# ==================================================

st.subheader("Top Risk Clients")

top_clients = (
    df.groupby("client_id")
    ["overall_risk_score"]
    .max()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

st.dataframe(
    top_clients,
    use_container_width=True
)

# ==================================================
# COUNTRY ALERT ANALYSIS
# ==================================================

st.subheader(
    "Country Alert Analysis"
)

country_alerts = (
    alerts.groupby(
        "counterparty_country"
    )
    .size()
    .reset_index(name="alerts")
    .sort_values(
        by="alerts",
        ascending=False
    )
)

fig3 = px.bar(
    country_alerts.head(10),
    x="counterparty_country",
    y="alerts",
    text="alerts",
    title="Top 10 Countries by AML Alerts"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.dataframe(
    country_alerts,
    use_container_width=True
)

# ==================================================
# CASE MANAGEMENT
# ==================================================

st.divider()

st.subheader(
    "Case Management"
)

if not cases.empty:

    open_cases = len(
        cases[
            cases["status"] == "OPEN"
        ]
    )

    st.metric(
        "Open Cases",
        open_cases
    )

    st.dataframe(
        cases.head(100),
        use_container_width=True
    )

else:

    st.info(
        "No cases.csv found. Run the case management module first."
    )

# ==================================================
# ALERT INVESTIGATION
# ==================================================

st.divider()

st.subheader(
    "Alert Investigation"
)

risk_filter = st.selectbox(
    "Filter by Risk Level",
    [
        "ALL",
        "HIGH",
        "MEDIUM",
        "LOW"
    ]
)

if risk_filter == "ALL":

    filtered_alerts = alerts

else:

    filtered_alerts = alerts[
        alerts["risk_level"]
        ==
        risk_filter
    ]

st.dataframe(
    filtered_alerts.head(100),
    use_container_width=True
)

# ==================================================
# DOWNLOAD ALERTS
# ==================================================

csv = filtered_alerts.to_csv(
    index=False
)

st.download_button(
    label="Download AML Alerts",
    data=csv,
    file_name="aml_alerts.csv",
    mime="text/csv"
)

# ==================================================
# EXPLAINABLE AI
# ==================================================

if "explanation" in alerts.columns:

    st.divider()

    st.subheader(
        "Alert Explanations"
    )

    st.dataframe(
        alerts[
            [
                "transaction_id",
                "client_id",
                "overall_risk_score",
                "explanation"
            ]
        ].head(50),
        use_container_width=True
    )
