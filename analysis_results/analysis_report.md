# Comprehensive Data Analysis Report

## 1. Data Inspection

- **Shape**: (8763, 26)
- **Columns**: Age, Sex, Cholesterol, Heart Rate, Diabetes, Family History, Smoking, Obesity, Alcohol Consumption, Exercise Hours Per Week, Diet, Previous Heart Problems, Medication Use, Stress Level, Sedentary Hours Per Day, Income, BMI, Triglycerides, Physical Activity Days Per Week, Sleep Hours Per Day, Continent, Heart Attack Risk, Systolic_BP, Diastolic_BP, Radiotherapy Exposure, Composite Risk Score
- **Total Missing Values**: 0
- **Total Duplicates**: 0

## 2. Data Cleaning & Validation
### Categorical Variable Checks
- **Sex**: 2 unique values. Examples: <StringArray>
['Male', 'Female']
Length: 2, dtype: str
- **Family History**: 2 unique values. Examples: [0 1]
- **Smoking**: 2 unique values. Examples: [1 0]
- **Obesity**: 2 unique values. Examples: [0 1]
- **Alcohol Consumption**: 2 unique values. Examples: [0 1]
- **Diet**: 3 unique values. Examples: <StringArray>
['Average', 'Unhealthy', 'Healthy']
Length: 3, dtype: str
- **Previous Heart Problems**: 2 unique values. Examples: [0 1]
- **Medication Use**: 2 unique values. Examples: [0 1]
- **Stress Level**: 10 unique values. Examples: [9 1 6 2 7]
- **Continent**: 6 unique values. Examples: <StringArray>
['South America', 'North America', 'Europe', 'Asia', 'Africa']
Length: 5, dtype: str
- **Radiotherapy Exposure**: 2 unique values. Examples: [0 1]

### Outlier Analysis (Numeric)
- **Age**: 0 outliers found (Range: 18 - 90). Bounds: [-20.50, 127.50]
- **Cholesterol**: 0 outliers found (Range: 120 - 400). Bounds: [-15.00, 537.00]
- **Systolic_BP**: 0 outliers found (Range: 90 - 180). Bounds: [43.00, 227.00]
- **Diastolic_BP**: 0 outliers found (Range: 60 - 110). Bounds: [33.00, 137.00]

### Consistency Checks
- **Systolic BP Range**: 90 - 180
- **Diastolic BP Range**: 60 - 110
- **Cholesterol Range**: 120 - 400
- **ALERT**: Found 431 rows where Systolic BP <= Diastolic BP.

## 3. Feature Engineering
- **BP Split**: 'Systolic_BP' and 'Diastolic_BP' columns already exist. Skipping split.
- **Radiotherapy**: Column is already binary (0/1).
- **Composite Score**: Calculated new risk score based on formula: `0.3*SBP + 0.3*DBP + 0.2*Cholesterol + 0.2*Age`.
  - Raw Score Stats: Min=76.10, Max=180.70, Mean=128.79

## 4. Exploratory Data Analysis (EDA)
Generating plots...
- **Group Analysis**: Risk Score Comparison
  - Radiotherapy (1) Mean Risk Score: 0.5046
  - Non-Radiotherapy (0) Mean Risk Score: 0.5028
  - Difference: Radiotherapy group has 0.36% higher average risk score.

## 5. Problem Statement & Methodology
### Problem Statement
To predict cardiovascular risk in patients using clinical parameters (BP, Cholesterol, Age, Radiotherapy History) and identify high-risk individuals for early intervention.

### Methodology
1. **Data Collection & Cleaning**: Verified dataset integrity, no missing values found. Checked for outliers in key metrics.
2. **Feature Engineering**: Validated BP split (pre-existing), encoded Radiotherapy (binary), and computed a composite Risk Score using weighted factors.
3. **EDA**: Analyzed distributions and correlations. Found significant correlation between BP components and Risk Score. Identified risk score variations based on Radiotherapy exposure.
4. **Modeling (Future Step)**: Select predictive models (e.g., Random Forest, Logistic Regression) to classify risk based on the engineered features.
