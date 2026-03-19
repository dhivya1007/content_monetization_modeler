
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
df = pd.read_csv(r"C:\Users\haris\.vscode\youtube analysis\youtube_ad_revenue_dataset.csv")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔍 Filters")

category_filter = st.sidebar.multiselect(
    "Category",
    df["category"].unique(),
    default=df["category"].unique()
)

device_filter = st.sidebar.multiselect(
    "Device",
    df["device"].unique(),
    default=df["device"].unique()
)

country_filter = st.sidebar.multiselect(
    "Country",
    df["country"].unique(),
    default=df["country"].unique()
)

filtered_df = df[
    (df["category"].isin(category_filter)) &
    (df["device"].isin(device_filter)) &
    (df["country"].isin(country_filter))
]

# ---------------- KPI METRICS ----------------
st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Views", f"{filtered_df['views'].sum():,}")
col2.metric("Total Revenue", f"${filtered_df['ad_revenue_usd'].sum():,.2f}")
col3.metric("Avg Engagement", f"{((filtered_df['likes']+filtered_df['comments'])/filtered_df['views']).mean():.4f}")
col4.metric("Total Videos", f"{len(filtered_df):,}")

# ---------------- CATEGORY ANALYSIS ----------------
st.subheader("📊 Category Performance")

cat_stats = filtered_df.groupby("category").agg({
    "views": "sum",
    "likes": "sum",
    "comments": "sum",
    "ad_revenue_usd": "sum"
}).reset_index()

cat_stats["engagement"] = (cat_stats["likes"] + cat_stats["comments"]) / cat_stats["views"]

# Revenue Chart
fig, ax = plt.subplots()
ax.bar(cat_stats["category"], cat_stats["ad_revenue_usd"])
plt.xticks(rotation=45)
ax.set_ylabel("Revenue")
st.pyplot(fig)

# Engagement Chart
st.subheader("🔥 Engagement by Category")

fig, ax = plt.subplots()
ax.bar(cat_stats["category"], cat_stats["engagement"])
plt.xticks(rotation=45)
st.pyplot(fig)

# ---------------- REVENUE DISTRIBUTION ----------------
st.subheader("💰 Revenue Distribution")

fig, ax = plt.subplots()
ax.hist(filtered_df["ad_revenue_usd"], bins=30)
ax.set_xlabel("Revenue")
ax.set_ylabel("Frequency")
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