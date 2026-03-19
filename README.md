Content Monetization Modeler
🧠 Project Overview

The Content Monetization Modeler is a machine learning project that predicts YouTube ad revenue based on video performance metrics such as views, likes, comments, watch time, subscriber count, and contextual features like category, device, and country.

It also includes a Streamlit dashboard for interactive revenue prediction and exploratory data analysis (EDA).

🎯 Problem Statement

With the increasing reliance on YouTube as a revenue source, creators and media companies need data-driven tools to estimate potential earnings.

This project builds a Linear Regression-based model to predict ad revenue and provides insights into factors that influence monetization.

🚀 Features

📈 Predict YouTube ad revenue using ML model

📊 Interactive Streamlit dashboard

🔍 Exploratory Data Analysis (EDA)

📉 Feature importance insights

🧹 Data preprocessing pipeline

📊 Category-wise performance analysis

🌍 Country & device-based insights

🧰 Tech Stack

Python 🐍

Pandas 📊

NumPy

Scikit-learn 🤖

Matplotlib 📉

Streamlit 🚀

Joblib

📂 Dataset

Name: youtube_Ad_revenue_dataset.csv
Size: ~122,000 rows
Target Variable: ad_revenue_usd

📌 Features include:

views

likes

comments

watch_time_minutes

video_length_minutes

subscribers

category

device

country

engagement_rate

views_per_subscriber

date features (year, month, day)

⚙️ Workflow
1️⃣ Data Preprocessing

Missing value handling

Duplicate removal

Encoding categorical variables

Feature engineering

2️⃣ Exploratory Data Analysis (EDA)

Revenue distribution analysis

Category-wise performance

Engagement trends

3️⃣ Model Building

Linear Regression model

Train-test split

Feature scaling & encoding

4️⃣ Model Evaluation

R² Score

RMSE (Root Mean Squared Error)

MAE (Mean Absolute Error)

5️⃣ Deployment

Streamlit web application for real-time predictions

📊 Business Use Cases

🎯 Content Strategy Optimization

💰 Revenue Forecasting

📢 Ad Campaign Planning

🛠 Creator Analytics Tools

🖥️ Streamlit App Features

Input video metrics

Predict ad revenue instantly

Category & country selection

Interactive dashboard

Data insights visualization

📷 App Preview (optional)

(Add screenshot here if available)

📦 Installation
1️⃣ Clone the repository
git clone https://github.com/your-username/content-monetization-modeler.git
cd content-monetization-modeler
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Run Streamlit app
streamlit run app.py
📈 Model Performance

R² Score: ~(add your value)

RMSE: (add value)

MAE: (add value)

🔍 Key Insights

Views are the strongest predictor of revenue

Engagement rate significantly improves predictions

Category and country strongly influence monetization

Watch time is a key retention indicator

📁 Project Structure
content-monetization-modeler/
│
├── app.py
├── youtube_pipeline.pkl
├── youtube_Ad_revenue_dataset.csv
├── requirements.txt
├── README.md
🧑‍💻 Author

Dhivya Parthiban
Data Science Student
Project: Social Media Analytics & ML

⭐ Future Improvements

Add advanced ML models (XGBoost, Random Forest)

Improve feature engineering

Deploy on cloud (Streamlit Cloud / Render)

Add real-time YouTube API integration

📌 Conclusion

This project demonstrates how machine learning can be used to estimate and optimize YouTube monetization strategies by analyzing user engagement and content performance.
