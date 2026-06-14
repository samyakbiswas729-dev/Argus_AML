from sklearn.ensemble import IsolationForest


def detect_anomalies(df):

    features = df[
        [
            "amount",
            "overall_risk_score"
        ]
    ]

    model = IsolationForest(
        contamination=0.02,
        random_state=42
    )

    df["anomaly_flag"] = model.fit_predict(
        features
    )

    return df
