
import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Content Monetization Dashboard", layout="wide")

st.title("📊 Content Monetization Modeler Dashboard")

# ---------------- LOAD MODEL ----------------
try:
    pipeline = joblib.load("youtube_pipeline.pkl")
except Exception as e:
    st.error(f"Model loading failed: {e}")
    st.stop()

# ---------------- LOAD DATA ----------------
df = pd.read_csv(r"C:\Users\haris\.vscode\youtube analysis\cleaned_youtube_ad_revenue_dataset.csv")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔍 Filters")

category_options = ["All"] + sorted(df["category"].dropna().unique())
category_filter = st.sidebar.selectbox("Category", category_options)

device_options = ["All"] + sorted(df["device"].dropna().unique())
device_filter = st.sidebar.selectbox("Device", device_options)

country_options = ["All"] + sorted(df["country"].dropna().unique())
country_filter = st.sidebar.selectbox("Country", country_options)

filtered_df = df.copy()

if category_filter != "All":
    filtered_df = filtered_df[filtered_df["category"] == category_filter]

if device_filter != "All":
    filtered_df = filtered_df[filtered_df["device"] == device_filter]

if country_filter != "All":
    filtered_df = filtered_df[filtered_df["country"] == country_filter]

# ---------------- KPI METRICS ----------------
st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Views", f"{filtered_df['views'].sum():,}")
col2.metric("Total Revenue", f"${filtered_df['ad_revenue_usd'].sum():,.2f}")
col3.metric("Avg Engagement", f"{((filtered_df['likes']+filtered_df['comments'])/filtered_df['views']).mean():.4f}")
col4.metric("Total Videos", f"{len(filtered_df):,}")

# ---------------- CATEGORY ANALYSIS ----------------
st.subheader("📊 Category Performance")

# ---------------- AGGREGATION ----------------
cat_stats = filtered_df.groupby("category").agg({
    "views": "sum",
    "likes": "sum",
    "comments": "sum",
    "ad_revenue_usd": "sum"
}).reset_index()

# Avoid division by zero
cat_stats["engagement"] = (
    (cat_stats["likes"] + cat_stats["comments"]) /
    cat_stats["views"].replace(0, 1)
)

# ---------------- SORTING ----------------
cat_revenue = filtered_df.groupby("category")["ad_revenue_usd"].sum()
# ---------------- REVENUE CHART ----------------
st.subheader("🥧 Revenue Share by Category")

fig, ax = plt.subplots()

ax.pie(
    cat_revenue,
    labels=cat_revenue.index,
    autopct='%1.1f%%'
)

ax.set_title("Revenue Distribution by Category")

st.pyplot(fig)

# ---------------- ENGAGEMENT CHART ----------------
st.subheader("🔥 Engagement by Category")

engagement_sorted = cat_stats.sort_values(by="engagement", ascending=False)

fig, ax = plt.subplots()

ax.barh(engagement_sorted["category"], engagement_sorted["engagement"])
ax.set_xlabel("Engagement Rate")
ax.set_title("Top Categories by Engagement")

st.pyplot(fig)

# ---------------- REVENUE DISTRIBUTION ----------------
st.subheader("💰 Revenue Distribution")

fig, ax = plt.subplots()

ax.hist(filtered_df["ad_revenue_usd"], bins=30)

ax.set_xlabel("Revenue")
ax.set_ylabel("Frequency")
ax.set_title("Revenue Distribution")

st.pyplot(fig)
# ---------------- PREDICTION SECTION ----------------
st.subheader("🚀 Predict Ad Revenue")

col1, col2, col3 = st.columns(3)

views = col1.number_input("Views", 1, value=1000)
likes = col2.number_input("Likes", 0, value=100)
comments = col3.number_input("Comments", 0, value=10)

watch_time = col1.number_input("Watch Time", 1.0, value=5000.0)
video_length = col2.number_input("Video Length", 0.1, value=10.0)
subscribers = col3.number_input("Subscribers", 1, value=10000)

category = st.selectbox("Category", df["category"].unique())
device = st.selectbox("Device", df["device"].unique())
country = st.selectbox("Country", df["country"].unique())

year = st.number_input("Year", 2000, 2030, 2024)
month = st.number_input("Month", 1, 12, 1)
day = st.number_input("Day", 1, 31, 1)

if st.button("🚀 Predict Revenue"):

    engagement_rate = (likes + comments) / views if views else 0
    views_per_subscriber = views / subscribers if subscribers else 0

    input_df = pd.DataFrame([{
        "views": views,
        "likes": likes,
        "comments": comments,
        "watch_time_minutes": watch_time,
        "video_length_minutes": video_length,
        "subscribers": subscribers,
        "category": category,
        "device": device,
        "country": country,
        "year": year,
        "month": month,
        "day": day,
        "engagement_rate": engagement_rate,
        "views_per_subscriber": views_per_subscriber
    }])

    try:
        prediction = pipeline.predict(input_df)
        st.success(f"💰 Predicted Revenue: ${prediction[0]:.2f}")

        if engagement_rate > 0.1:
            st.info("🔥 High engagement content")
        else:
            st.warning("⚠️ Low engagement content")

    except Exception as e:
        st.error(f"Prediction error: {e}")
