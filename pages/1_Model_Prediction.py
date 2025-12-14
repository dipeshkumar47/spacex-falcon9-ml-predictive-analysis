import streamlit as st
import pandas as pd

from streamlit_utils.feature_builder import build_features
from streamlit_utils.model_loader import load_model_and_scaler, get_training_columns

# --------------------------------------------------
# LOAD MODEL, SCALER & TRAINING SCHEMA
# --------------------------------------------------
model, scaler = load_model_and_scaler()
training_columns = get_training_columns()

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------
st.markdown("## 🔮 Falcon 9 Launch Success Prediction")
st.markdown("Predict whether a Falcon 9 booster will successfully land.")
st.markdown("---")

left_col, right_col = st.columns([1.2, 1])

# --------------------------------------------------
# USER INPUTS
# --------------------------------------------------
with left_col:
    st.markdown("### 🧾 Launch Parameters")

    flight_number = st.number_input("Flight Number", min_value=1, value=50)
    payload_mass = st.slider("Payload Mass (kg)", 0, 15000, 5000, step=100)
    flights = st.number_input("Number of Previous Flights", min_value=0, value=1)

    orbit = st.selectbox(
        "Orbit",
        [
            "LEO", "GTO", "ISS", "SSO", "PO", "MEO",
            "HEO", "GEO", "TLI", "SO", "VLEO",
            "ES-L1", "HCO", "Unknown"
        ]
    )

    launch_site = st.selectbox(
        "Launch Site",
        [
            "CCSFS SLC 40 (Florida)",
            "KSC LC 39A (Florida)",
            "VAFB SLC 4E (California)",
            "Kwajalein Atoll (Marshall Islands)"
        ]
    )

    grid_fins = st.selectbox("Grid Fins Used?", ["Yes", "No"])
    reused = st.selectbox("Booster Reused?", ["Yes", "No"])
    legs = st.selectbox("Landing Legs Deployed?", ["Yes", "No"])

    predict_btn = st.button("🚀 Predict Launch Outcome", use_container_width=True)

# --------------------------------------------------
# PREDICTION LOGIC
# --------------------------------------------------
with right_col:
    st.markdown("### 📊 Prediction Result")

    if predict_btn:
        input_df = pd.DataFrame([{
            "flight_number": flight_number,
            "PayloadMass": payload_mass,
            "Flights": flights,
            "Orbit": orbit,
            "LaunchSiteName": launch_site,
            "GridFins": 1 if grid_fins == "Yes" else 0,
            "Reused": 1 if reused == "Yes" else 0,
            "Legs": 1 if legs == "Yes" else 0
        }])

        # Feature engineering
        features_df = build_features(input_df, scaler)


        # Scaling
        features_scaled = scaler.transform(features_df)

        # Prediction
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0][1]

        if prediction == 1:
            st.success("✅ Predicted Outcome: SUCCESS")
        else:
            st.error("❌ Predicted Outcome: FAILURE")

        st.metric("Success Probability", f"{probability:.2%}")
        st.progress(float(probability))

    else:
        st.info("Enter parameters and click **Predict Launch Outcome**")
