import time
from datetime import datetime
import pandas as pd
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import plotly.express as px

# ----------------------------
# SETTINGS (EDIT THESE 2)
# ----------------------------
SERVICE_ACCOUNT_FILE = "service_account.json"
SPREADSHEET_NAME = "Internal Operations Submission Form (Responses)"   # <-- change if different
WORKSHEET_NAME = "Processed_Logs"                                      # <-- must match your sheet tab

REFRESH_SECONDS = 15

# ----------------------------
# STREAMLIT PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Internal Ops AI Workflow Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Internal Operations AI Workflow Dashboard")
st.caption("Live monitoring from Google Sheets → Processed_Logs")

# ----------------------------
# AUTH + SHEETS READ
# ----------------------------
@st.cache_data(ttl=REFRESH_SECONDS)
def load_data():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
    ]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    client = gspread.authorize(creds)

    sh = client.open(SPREADSHEET_NAME)
    ws = sh.worksheet(WORKSHEET_NAME)

    rows = ws.get_all_records()  # list of dicts
    df = pd.DataFrame(rows)

    if df.empty:
        return df

    # Normalize expected columns
    for col in ["Original_Input", "Category", "Cerebras_Response", "Routing_Destination", "Timestamp"]:
        if col not in df.columns:
            df[col] = ""

    # Parse timestamp safely
    def parse_ts(x):
        if pd.isna(x):
            return pd.NaT
        s = str(x).strip()
        if not s:
            return pd.NaT
        # Try common formats
        for fmt in (
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%d/%m/%Y %H:%M:%S",
            "%d/%m/%Y %H:%M",
            "%m/%d/%Y %H:%M:%S",
            "%m/%d/%Y %H:%M",
        ):
            try:
                return datetime.strptime(s, fmt)
            except Exception:
                pass
        # fallback
        return pd.to_datetime(s, errors="coerce")

    df["Timestamp_parsed"] = df["Timestamp"].apply(parse_ts)

    # Clean category
    df["Category"] = df["Category"].astype(str).str.strip()
    df.loc[df["Category"] == "", "Category"] = "Unknown"

    # Sort newest first
    df = df.sort_values(by="Timestamp_parsed", ascending=False, na_position="last").reset_index(drop=True)

    # Daily grouping
    df["Date"] = df["Timestamp_parsed"].dt.date

    return df

# ----------------------------
# LOAD DATA
# ----------------------------
try:
    df = load_data()
except Exception as e:
    st.error("Could not load Google Sheet data. Check Spreadsheet name, Worksheet name, and sharing permissions.")
    st.code(str(e))
    st.stop()

if df.empty:
    st.warning("No processed records found yet in Processed_Logs.")
    st.stop()

# ----------------------------
# FILTERS
# ----------------------------
left, right = st.columns([2, 1])

with left:
    categories = sorted(df["Category"].unique().tolist())
    selected_categories = st.multiselect("Filter by Category", categories, default=categories)

with right:
    show_latest = st.number_input("Show latest records", min_value=10, max_value=500, value=50, step=10)

df_f = df[df["Category"].isin(selected_categories)].copy()

# ----------------------------
# KPIs
# ----------------------------
k1, k2, k3, k4 = st.columns(4)

total = len(df_f)
k1.metric("Total Processed", f"{total}")

# Today's count
today = datetime.now().date()
today_count = int((df_f["Date"] == today).sum())
k2.metric("Processed Today", f"{today_count}")

# Most common category
top_cat = df_f["Category"].value_counts().idxmax() if total > 0 else "N/A"
top_cat_count = int(df_f["Category"].value_counts().max()) if total > 0 else 0
k3.metric("Top Category", f"{top_cat}", f"{top_cat_count} items")

# Last processed time
last_ts = df_f["Timestamp_parsed"].dropna().iloc[0] if df_f["Timestamp_parsed"].notna().any() else None
k4.metric("Last Processed", last_ts.strftime("%Y-%m-%d %H:%M:%S") if last_ts else "N/A")

st.divider()

# ----------------------------
# CHARTS
# ----------------------------
c1, c2 = st.columns(2)

# Category breakdown
cat_counts = df_f["Category"].value_counts().reset_index()
cat_counts.columns = ["Category", "Count"]

fig_pie = px.pie(
    cat_counts,
    names="Category",
    values="Count",
    title="Category Breakdown",
)
c1.plotly_chart(fig_pie, use_container_width=True)

# Daily volume
daily = df_f.groupby("Date", dropna=False).size().reset_index(name="Count")
daily = daily.dropna(subset=["Date"]).sort_values("Date")

fig_bar = px.bar(
    daily,
    x="Date",
    y="Count",
    title="Daily Processing Volume",
)
c2.plotly_chart(fig_bar, use_container_width=True)

# Trend over time (by timestamp)
st.subheader("Processing Trend Over Time")
trend = df_f.dropna(subset=["Timestamp_parsed"]).copy()
trend = trend.sort_values("Timestamp_parsed")
trend["Count"] = 1
trend["Cumulative"] = trend["Count"].cumsum()

fig_line = px.line(
    trend,
    x="Timestamp_parsed",
    y="Cumulative",
    title="Cumulative Processed Over Time",
)
st.plotly_chart(fig_line, use_container_width=True)

# ----------------------------
# TABLE (LATEST RECORDS)
# ----------------------------
st.subheader("Latest Processed Records")

show_cols = ["Timestamp", "Category", "Routing_Destination", "Original_Input", "Cerebras_Response"]
table_df = df_f[show_cols].head(int(show_latest)).copy()

# Make long text readable
table_df["Original_Input"] = table_df["Original_Input"].astype(str).str.slice(0, 160)
table_df["Cerebras_Response"] = table_df["Cerebras_Response"].astype(str).str.slice(0, 240)

st.dataframe(table_df, use_container_width=True, height=420)

st.caption(f"Auto-refresh every {REFRESH_SECONDS} seconds.")
time.sleep(REFRESH_SECONDS)
st.rerun()