import pandas as pd

try:
    df = pd.read_csv('updated_heart_risk_dataset.csv')
    print("Columns:", df.columns.tolist())
    print("\nFirst 2 rows:")
    print(df.head(2))
    print("\nInfo:")
    print(df.info())
except Exception as e:
    print(e)
