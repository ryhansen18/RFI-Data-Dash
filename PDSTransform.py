import pandas as pd

# File path to the dataset
file_path = r"C:\Users\rhansen\OneDrive - Haugland Group, LLC\Documents\Internship\Resume Related\Projects\Pythons\PDTRANSFORM.csv"

# Load CSV into DataFrame
df = pd.read_csv(file_path)

# Preview data
print("\n=== DATA LOADED SUCCESSFULLY ===")
print(df.head())

# Show structure and data types
print("\n=== INFO ===")
print(df.info())

# Check missing values
print("\n=== MISSING VALUES ===")
print(df.isnull().sum())

# Identify duplicate rows
print("\n=== DUPLICATES ===")
print(df[df.duplicated()])

# Standardize text fields
df["Status"] = df["Status"].astype(str).str.lower().str.strip()
df["Assigned_To"] = df["Assigned_To"].astype(str).str.lower().str.strip()

# Show cleaned status distribution
print("\n=== STATUS COUNTS ===")
print(df["Status"].value_counts())

# Convert date columns to datetime
df["Created_Date"] = pd.to_datetime(df["Created_Date"], errors="coerce")
df["Closed_Date"] = pd.to_datetime(df["Closed_Date"], errors="coerce")
df["Due_Date"] = pd.to_datetime(df["Due_Date"], errors="coerce")

# Clean and convert cost column to numeric
df["Cost_Impact"] = df["Cost_Impact"].replace('[\$,]', '', regex=True)
df["Cost_Impact"] = pd.to_numeric(df["Cost_Impact"], errors="coerce")

# Filter high-cost records
high_cost = df[df["Cost_Impact"] > 100000]

print("\n=== HIGH COST RFIs ===")
print(high_cost[["RFI_ID", "Cost_Impact", "Assigned_To"]])

# Find invalid timelines (closed before created)
bad_dates = df[df["Closed_Date"] < df["Created_Date"]]

print("\n=== INVALID DATE RECORDS ===")
print(bad_dates)

# Find records with negative duration
negative_days = df[df["Days_Open"] < 0]

print("\n=== NEGATIVE DAYS ===")
print(negative_days)

# Identify overdue RFIs
overdue = df[
    (df["Status"] != "closed") &
    (df["Due_Date"] < pd.Timestamp.today())
]

print("\n=== OVERDUE RFIs ===")
print(overdue[["RFI_ID", "Assigned_To", "Due_Date"]])

# Summary of data quality issues
print("\n=== DATA QUALITY SUMMARY ===")

print(f"Total Rows: {len(df)}")
print(f"Missing Values: {df.isnull().sum().sum()}")
print(f"Duplicate Rows: {df.duplicated().sum()}")
print(f"Invalid Date Records: {len(bad_dates)}")
print(f"Negative Days Records: {len(negative_days)}")

# Analyze average delay by person
print("\n=== AVERAGE DAYS OPEN BY PERSON ===")
print(df.groupby("Assigned_To")["Days_Open"].mean().sort_values(ascending=False))

# Identify high-risk records
risky = df[
    (df["Days_Open"] > 100) |
    (df["Cost_Impact"] > 100000)
]

print("\n=== HIGH RISK RECORDS ===")
print(risky[["RFI_ID", "Days_Open", "Cost_Impact", "Assigned_To"]])

# Export key datasets
overdue.to_csv("overdue_rfis.csv", index=False)
risky.to_csv("high_risk_rfis.csv", index=False)
bad_dates.to_csv("invalid_dates.csv", index=False)
