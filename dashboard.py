import pandas as pd
import streamlit as st

st.set_page_config(page_title="RFI Audit Dashboard", layout="wide")

st.title("RFI Data Audit & Risk Dashboard")

file_path = r"C:\Users\rhansen\OneDrive - Haugland Group, LLC\Documents\Internship\Resume Related\Projects\Pythons\PDTRANSFORM.csv"
df = pd.read_csv(file_path)

df["Status"] = df["Status"].astype(str).str.lower().str.strip()
df["Assigned_To"] = df["Assigned_To"].astype(str).str.lower().str.strip()

df["Created_Date"] = pd.to_datetime(df["Created_Date"], errors="coerce")
df["Closed_Date"] = pd.to_datetime(df["Closed_Date"], errors="coerce")
df["Due_Date"] = pd.to_datetime(df["Due_Date"], errors="coerce")

df["Cost_Impact"] = df["Cost_Impact"].replace('[\$,]', '', regex=True)
df["Cost_Impact"] = pd.to_numeric(df["Cost_Impact"], errors="coerce")

bad_dates = df[df["Closed_Date"] < df["Created_Date"]]
negative_days = df[df["Days_Open"] < 0]
duplicates = df[df.duplicated()]

overdue = df[
    (df["Status"] != "closed") &
    (df["Due_Date"] < pd.Timestamp.today())
]

risky = df[
    (df["Days_Open"] > 100) |
    (df["Cost_Impact"] > 100000)
]

st.sidebar.header("Filters")

people = st.sidebar.multiselect(
    "Assigned To",
    options=df["Assigned_To"].dropna().unique()
)

status_filter = st.sidebar.multiselect(
    "Status",
    options=df["Status"].unique()
)

filtered_df = df.copy()

if people:
    filtered_df = filtered_df[filtered_df["Assigned_To"].isin(people)]

if status_filter:
    filtered_df = filtered_df[filtered_df["Status"].isin(status_filter)]

st.header("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", len(df))
col2.metric("Overdue RFIs", len(overdue))
col3.metric("High Risk Items", len(risky))
col4.metric("Duplicates", len(duplicates))

col5, col6, col7 = st.columns(3)

col5.metric("Missing Values", int(df.isnull().sum().sum()))
col6.metric("Invalid Dates", len(bad_dates))
col7.metric("Negative Durations", len(negative_days))

st.divider()

colA, colB = st.columns(2)

with colA:
    st.subheader("Status Distribution")
    st.bar_chart(filtered_df["Status"].value_counts())

with colB:
    st.subheader("Average Days Open by Person")
    avg_days = df.groupby("Assigned_To")["Days_Open"].mean().sort_values(ascending=False)
    st.bar_chart(avg_days)

st.divider()

st.subheader("Overdue RFIs")
st.dataframe(overdue, use_container_width=True)

st.subheader("High Risk RFIs")
st.dataframe(risky[["RFI_ID", "Days_Open", "Cost_Impact", "Assigned_To"]], use_container_width=True)

st.subheader("Invalid Timeline Records")
st.dataframe(bad_dates, use_container_width=True)

st.subheader("Duplicate Records")
st.dataframe(duplicates, use_container_width=True)

st.divider()

st.subheader("Search RFI")

search = st.text_input("Enter RFI ID")

if search:
    result = df[df["RFI_ID"].str.contains(search, case=False, na=False)]
    st.dataframe(result, use_container_width=True)

st.subheader("Download Data")

st.download_button(
    label="Download Overdue RFIs",
    data=overdue.to_csv(index=False),
    file_name="overdue_rfis.csv"
)

st.download_button(
    label="Download High Risk RFIs",
    data=risky.to_csv(index=False),
    file_name="high_risk_rfis.csv"
)