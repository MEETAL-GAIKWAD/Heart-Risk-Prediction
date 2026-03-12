import pandas as pd
import numpy as np

try:
    df = pd.read_csv('updated_heart_risk_dataset.csv')
    print("Unique values in 'Radiotherapy Exposure':", df['Radiotherapy Exposure'].unique())
    if 'BP' in df.columns:
        print("'BP' column exists.")
    else:
        print("'BP' column does NOT exist.")
    
    print("Columns:", df.columns.tolist())
    
    # Check for duplicates
    print(f"Duplicates: {df.duplicated().sum()}")
    
except Exception as e:
    print(e)
