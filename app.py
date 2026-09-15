import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

st.set_page_config(page_title="Urban Flood Prediction", page_icon="🌧️")

st.title("🌧️ Urban Flood Risk Prediction")
st.write("Predict street-level flood depth using rainfall, elevation and drainage condition.")

# Load data
data = pd.read_csv("flood_data.csv")

# Train model
X = data[["Rainfall_mm", "Elevation_m", "Drainage_Score"]]
y = data["Flood_Depth_cm"]

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

st.subheader("Enter Location Data")

rainfall = st.number_input("Rainfall (mm)", min_value=0.0, value=70.0)
elevation = st.number_input("Elevation (m)", min_value=0.0, value=7.0)

drainage = st.selectbox(
    "Drainage Condition",
    ["Good", "Poor", "Blocked"]
)

drainage_score = {
    "Good": 3,
    "Poor": 2,
    "Blocked": 1
}[drainage]

if st.button("🔍 Predict Flood"):

    new_data = pd.DataFrame([{
        "Rainfall_mm": rainfall,
        "Elevation_m": elevation,
        "Drainage_Score": drainage_score
    }])

    prediction = model.predict(new_data)[0]

    if prediction < 5:
        risk = "LOW"
    elif prediction < 15:
        risk = "MEDIUM"
    elif prediction < 30:
        risk = "HIGH"
    else:
        risk = "VERY HIGH"

    st.success(f"Predicted Flood Depth: {prediction:.1f} cm")
    st.warning(f"Flood Risk: {risk}")