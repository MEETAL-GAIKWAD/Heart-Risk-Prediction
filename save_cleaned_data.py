
import pandas as pd

df = pd.read_csv('updated_heart_risk_dataset.csv')
initial_count = len(df)

# Drop rows where SBP <= DBP
df_clean = df[df['Systolic_BP'] > df['Diastolic_BP']]
final_count = len(df_clean)
dropped_count = initial_count - final_count

print(f"Dropped {dropped_count} rows where Systolic BP <= Diastolic BP.")

# Save cleaned data
clean_path = 'cleaned_heart_risk_dataset.csv'
df_clean.to_csv(clean_path, index=False)
print(f"Cleaned dataset saved to: {clean_path}")
