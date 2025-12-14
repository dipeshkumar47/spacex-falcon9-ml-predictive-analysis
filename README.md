\# 🚀 SpaceX Falcon 9 Launch Analysis \& ML Dashboard



An end-to-end machine learning and data analytics project that analyzes SpaceX Falcon 9 launches, predicts first-stage landing success, and presents insights through an interactive Streamlit dashboard.



This project focuses on building a \*\*real-world data pipeline\*\* — from raw API data to a deployable ML application — rather than just training a model in notebooks.



---



\## 📌 Project Highlights



\- 🔗 Real-time data ingestion from \*\*SpaceX public v4 APIs\*\*

\- 🧹 Data cleaning, wrangling, and feature engineering from nested JSON

\- 🤖 Machine learning model to predict Falcon 9 landing success

\- 📊 Interactive analytics dashboard with slicers, charts, and heatmaps

\- 🌍 Geospatial launch-site visualization with rocket icons and clustering

\- 🧠 Clear separation of ML-ready data and visualization-ready data



---



\## 🗂️ Project Structure



```text

spacex-falcon9-ml-dashboard/

├── app.py                      # Main Streamlit entry point

├── pages/

│   ├── 1\_Model\_Prediction.py   # ML inference page

│   └── 2\_Dashboard.py          # Analytics dashboard

├── data/

│   ├── raw/                    # Raw API and scraped data

│   ├── interim/                # Cleaned data for analysis \& dashboards

│   └── processed/              # Feature-engineered data for ML

├── models/

│   ├── best\_model.pkl          # Trained ML model

│   └── scaler.pkl              # Feature scaler

├── notebooks/

│   ├── 01\_data\_collection.ipynb

│   ├── 02\_data\_wrangling.ipynb

│   ├── 03\_eda\_sql.ipynb

│   ├── 04\_geo\_visuals.ipynb

│   ├── 05\_modeling.ipynb

│   └── 06\_final\_analysis.ipynb

├── src/

│   ├── fetch\_api.py            # SpaceX API calls

│   ├── wrangle.py              # Data cleaning \& preprocessing

│   ├── features.py             # Feature engineering helpers

│   ├── visualize.py            # Visualization utilities

│   └── eval.py                 # Model evaluation

├── config/

│   ├── config.yaml

│   └── model\_params.yaml

├── requirements.txt

└── README.md



