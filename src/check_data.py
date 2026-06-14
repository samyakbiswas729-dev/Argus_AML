import pandas as pd

files = {
    "PaySim": "data/paysim dataset.csv",
    "Clients": "data/clients_with_fatf_ofac.csv",
    "Transactions": "data/transactions_with_fatf_ofac.csv",
    "Country Risk": "data/country_risk.csv",
    "Sanctions": "data/sdn.csv"
}

for name, path in files.items():
    print("\n" + "="*60)
    print(name)
    print("="*60)

    df = pd.read_csv(path)

    print("Columns:")
    print(df.columns.tolist())

    print("\nShape:")
    print(df.shape)

    print("\nFirst 3 Rows:")
    print(df.head(3))
    