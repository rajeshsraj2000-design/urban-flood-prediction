import os
import streamlit as st
import pandas as pd
import pydeck as pdk
from sklearn.ensemble import RandomForestRegressor


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Flood AI",
    page_icon="🌧️",
    layout="wide"
)


# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

CSV_FILE = os.path.join(BASE_DIR, "flood_data.csv")
MAP_FILE = os.path.join(BASE_DIR, "flood_map.png")


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.block-container {
    padding-top: 1rem;
}

.alert-box {
    padding: 15px;
    border-radius: 10px;
    background-color: #fff3cd;
    border: 1px solid #ffe69c;
}

.success-box {
    padding: 15px;
    border-radius: 10px;
    background-color: #d1e7dd;
    border: 1px solid #a3cfbb;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD CSV
# =========================================================

if not os.path.isfile(CSV_FILE):

    st.error("❌ flood_data.csv was not found.")

    st.write("App folder:", BASE_DIR)

    st.stop()


data = pd.read_csv(CSV_FILE)


# =========================================================
# CHECK REQUIRED COLUMNS
# =========================================================

required_columns = [
    "Rainfall_mm",
    "Elevation_m",
    "Drainage_Score",
    "Flood_Depth_cm"
]

missing_columns = [
    col for col in required_columns
    if col not in data.columns
]

if missing_columns:

    st.error(
        "Missing columns: "
        + ", ".join(missing_columns)
    )

    st.stop()


# =========================================================
# RANDOM FOREST MODEL
# =========================================================

X = data[
    [
        "Rainfall_mm",
        "Elevation_m",
        "Drainage_Score"
    ]
]

y = data["Flood_Depth_cm"]


model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🌧️ FLOOD AI")

st.sidebar.caption(
    "Urban Flood Nowcasting & Decision Support System"
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "MENU",
    [
        "🏠 Home",
        "🌊 Flood Prediction",
        "🗺️ Flood Map",
        "⏱️ Forecast",
        "🛣️ Roads",
        "🚰 Drainage",
        "🚑 Safe Route",
        "ℹ️ About"
    ]
)


# =========================================================
# SIMULATION
# =========================================================

st.sidebar.markdown("---")

st.sidebar.subheader("⚙️ Simulation")


rainfall = st.sidebar.number_input(
    "Rainfall (mm)",
    min_value=0.0,
    max_value=300.0,
    value=70.0,
    step=5.0
)


elevation = st.sidebar.number_input(
    "Elevation (m)",
    min_value=0.0,
    max_value=100.0,
    value=7.0,
    step=1.0
)


drainage_condition = st.sidebar.selectbox(
    "Drainage Condition",
    [
        "Good",
        "Poor",
        "Blocked"
    ]
)


if drainage_condition == "Good":
    drainage_score = 3

elif drainage_condition == "Poor":
    drainage_score = 2

else:
    drainage_score = 1


# =========================================================
# PREDICTION
# =========================================================

input_data = pd.DataFrame(
    [{
        "Rainfall_mm": rainfall,
        "Elevation_m": elevation,
        "Drainage_Score": drainage_score
    }]
)


prediction = model.predict(input_data)[0]

prediction = max(0, prediction)


# =========================================================
# RISK
# =========================================================

if prediction < 5:

    risk = "LOW"
    risk_icon = "🟢"

elif prediction < 15:

    risk = "MEDIUM"
    risk_icon = "🟡"

elif prediction < 30:

    risk = "HIGH"
    risk_icon = "🟠"

else:

    risk = "VERY HIGH"
    risk_icon = "🔴"


# =========================================================
# HOME
# =========================================================

if page == "🏠 Home":

    st.title("🌧️ FLOOD AI")

    st.subheader(
        "Urban Flood Nowcasting & Decision Support System"
    )


    if risk == "LOW":

        st.success(
            "✅ LOW FLOOD RISK — Current conditions are relatively safe."
        )

    elif risk == "MEDIUM":

        st.warning(
            "⚠️ MEDIUM FLOOD RISK — Monitor flood-prone areas."
        )

    elif risk == "HIGH":

        st.warning(
            "⚠️ HIGH FLOOD RISK — Flood-prone areas should be monitored."
        )

    else:

        st.error(
            "🚨 VERY HIGH FLOOD RISK — Immediate monitoring is required."
        )


    st.markdown("---")

    st.subheader("📊 Live Situation")


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "🌧️ Rainfall",
            f"{rainfall:.1f} mm"
        )


    with c2:

        st.metric(
            "🌊 Flood Depth",
            f"{prediction:.1f} cm"
        )


    with c3:

        st.metric(
            "⚠️ Risk",
            f"{risk_icon} {risk}"
        )


    with c4:

        st.metric(
            "🚰 Drainage",
            drainage_condition
        )


    st.markdown("---")

    st.subheader("⚡ Quick Monitoring")


    q1, q2, q3 = st.columns(3)


    with q1:
        st.info("🌊 Flood Prediction")


    with q2:
        st.info("🗺️ Flood Map")


    with q3:
        st.info("🚑 Safe Route")


    st.markdown("---")

    # =====================================================
    # FLOOD RISK MAP
    # =====================================================

    st.subheader("🗺️ Flood Risk Map")


    if os.path.isfile(MAP_FILE):

        try:

            with open(MAP_FILE, "rb") as image_file:

                image_bytes = image_file.read()


            st.image(
                image_bytes,
                width="stretch"
            )


            st.caption(
                "QGIS-based Chennai prototype flood-risk map."
            )

        except Exception as e:

            st.error(
                "Unable to load flood map image."
            )

            st.code(str(e))

    else:

        st.error(
            "❌ flood_map.png was not found."
        )

        st.write(
            "Expected file location:"
        )

        st.code(MAP_FILE)


    st.markdown("---")

    st.subheader("🔄 How the System Works")


    st.markdown("""
🌧️ **Rainfall**

↓

🗺️ **Elevation / Terrain**

↓

🚰 **Drainage Condition**

↓

🤖 **Machine Learning**

↓

🌊 **Flood Depth**

↓

🚨 **Flood Risk**

↓

🗺️ **Map + 🛣️ Roads + 🚑 Safe Route**
""")


    st.success(
        "✅ Flood AI prototype is running successfully."
    )


# =========================================================
# FLOOD PREDICTION
# =========================================================

elif page == "🌊 Flood Prediction":

    st.title("🌊 Flood Prediction")


    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(
            "Rainfall",
            f"{rainfall:.1f} mm"
        )


    with c2:

        st.metric(
            "Flood Depth",
            f"{prediction:.1f} cm"
        )


    with c3:

        st.metric(
            "Risk",
            f"{risk_icon} {risk}"
        )


    st.markdown("---")


    st.subheader("🤖 Machine Learning Model")


    st.write(
        "Random Forest uses rainfall, elevation and "
        "drainage condition to estimate flood depth."
    )


    st.dataframe(
        input_data,
        use_container_width=True
    )


# =========================================================
# FLOOD MAP
# =========================================================

elif page == "🗺️ Flood Map":

    st.title("🗺️ Flood Map")


    st.subheader("QGIS Flood Risk Map")


    if os.path.isfile(MAP_FILE):

        with open(MAP_FILE, "rb") as image_file:

            image_bytes = image_file.read()


        st.image(
            image_bytes,
            width="stretch"
        )

    else:

        st.error(
            "❌ flood_map.png was not found."
        )

        st.code(MAP_FILE)


    st.markdown("---")


    st.subheader("📍 Interactive Flood Location Map")


    if (
        "Latitude" in data.columns
        and
        "Longitude" in data.columns
    ):

        map_data = data[
            [
                "Latitude",
                "Longitude",
                "Flood_Depth_cm"
            ]
        ].dropna()


        if len(map_data) > 0:

            layer = pdk.Layer(
                "ScatterplotLayer",
                data=map_data,
                get_position="[Longitude, Latitude]",
                get_radius=250,
                get_fill_color="[255, 80, 80, 180]",
                pickable=True
            )


            view_state = pdk.ViewState(
                latitude=map_data["Latitude"].mean(),
                longitude=map_data["Longitude"].mean(),
                zoom=11
            )


            deck = pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip={
                    "text":
                    "Flood Depth: {Flood_Depth_cm} cm"
                }
            )


            st.pydeck_chart(deck)


        else:

            st.warning(
                "No valid coordinate data available."
            )


    else:

        st.warning(
            "Latitude and Longitude columns are required."
        )


# =========================================================
# FORECAST
# =========================================================

elif page == "⏱️ Forecast":

    st.title("⏱️ 0–3 Hour Flood Forecast")


    current_depth = prediction


    forecast_data = pd.DataFrame(
        {
            "Time": [
                "Now",
                "+30 min",
                "+1 hour",
                "+2 hours",
                "+3 hours"
            ],

            "Flood Depth (cm)": [
                current_depth,
                current_depth * 1.15,
                current_depth * 1.30,
                current_depth * 1.50,
                current_depth * 1.70
            ]
        }
    )


    st.dataframe(
        forecast_data,
        use_container_width=True
    )


    st.line_chart(
        forecast_data.set_index("Time")
    )


    st.info(
        "Prototype forecast. Real-time IMD/radar rainfall "
        "integration is planned as the next stage."
    )


# =========================================================
# ROADS
# =========================================================

elif page == "🛣️ Roads":

    st.title("🛣️ Flooded Road Detection")


    road_data = pd.DataFrame(
        {
            "Road": [
                "Road A",
                "Road B",
                "Road C",
                "Road D"
            ],

            "Predicted Depth (cm)": [
                prediction * 0.6,
                prediction * 1.2,
                prediction * 0.8,
                prediction * 1.5
            ]
        }
    )


    def road_status(depth):

        if depth < 10:
            return "🟢 Safe"

        elif depth < 25:
            return "🟡 Caution"

        elif depth < 40:
            return "🟠 Flooded"

        else:
            return "🔴 Highly Flooded"


    road_data["Status"] = road_data[
        "Predicted Depth (cm)"
    ].apply(road_status)


    st.dataframe(
        road_data,
        use_container_width=True
    )


# =========================================================
# DRAINAGE
# =========================================================

elif page == "🚰 Drainage":

    st.title("🚰 Urban Drainage Network")


    drainage_table = pd.DataFrame(
        {
            "Node": [
                "N1",
                "N2",
                "N3",
                "N4",
                "N5"
            ],

            "Type": [
                "Manhole",
                "Manhole",
                "Junction",
                "Pump",
                "Outfall"
            ],

            "Condition": [
                "Good",
                "Poor",
                "Blocked",
                "Good",
                "Good"
            ],

            "Capacity (L/s)": [
                1000,
                800,
                500,
                1200,
                1500
            ]
        }
    )


    st.dataframe(
        drainage_table,
        use_container_width=True
    )


    st.markdown("---")


    st.subheader("🚨 Drainage Blockage Analysis")


    if drainage_condition == "Blocked":

        st.error(
            "🚨 Drainage blockage detected."
        )

    elif drainage_condition == "Poor":

        st.warning(
            "⚠️ Poor drainage condition detected."
        )

    else:

        st.success(
            "✅ Drainage condition is good."
        )


    st.markdown("---")


    st.subheader("🔄 Drainage Network Flow Map")


    flow_data = pd.DataFrame(
        {
            "start_lat": [
                13.0827,
                13.0850,
                13.0800,
                13.0870
            ],

            "start_lon": [
                80.2707,
                80.2750,
                80.2650,
                80.2800
            ],

            "end_lat": [
                13.0850,
                13.0800,
                13.0870,
                13.0780
            ],

            "end_lon": [
                80.2750,
                80.2650,
                80.2800,
                80.2600
            ]
        }
    )


    line_layer = pdk.Layer(
        "LineLayer",
        data=flow_data,
        get_source_position="[start_lon, start_lat]",
        get_target_position="[end_lon, end_lat]",
        get_width=5,
        pickable=True
    )


    view_state = pdk.ViewState(
        latitude=13.0827,
        longitude=80.2707,
        zoom=11
    )


    deck = pdk.Deck(
        layers=[line_layer],
        initial_view_state=view_state
    )


    st.pydeck_chart(deck)


    st.markdown("---")


    st.subheader("🚰 Drainage Pipe Flow")


    pipe_flow = pd.DataFrame(
        {
            "Pipe": [
                "P1",
                "P2",
                "P3",
                "P4"
            ],

            "Capacity (L/s)": [
                1000,
                800,
                600,
                1200
            ],

            "Estimated Flow (L/s)": [
                rainfall * 8,
                rainfall * 6,
                rainfall * 7,
                rainfall * 9
            ]
        }
    )


    st.dataframe(
        pipe_flow,
        use_container_width=True
    )


# =========================================================
# SAFE ROUTE
# =========================================================

elif page == "🚑 Safe Route":

    st.title("🚑 Flood-Safe Route Suggestion")


    route_data = pd.DataFrame(
        {
            "Road": [
                "Road A",
                "Road B",
                "Road C",
                "Road D"
            ],

            "Flood Depth (cm)": [
                prediction * 0.6,
                prediction * 1.2,
                prediction * 0.8,
                prediction * 1.5
            ]
        }
    )


    safe_road = route_data.loc[
        route_data["Flood Depth (cm)"].idxmin(),
        "Road"
    ]


    st.success(
        f"🚑 Suggested safer road: **{safe_road}**"
    )


    st.dataframe(
        route_data,
        use_container_width=True
    )


    st.info(
        "Prototype route recommendation. "
        "Real navigation API integration can be added later."
    )


# =========================================================
# ABOUT
# =========================================================

elif page == "ℹ️ About":

    st.title("ℹ️ About Flood AI")


    st.subheader(
        "Urban Flood Nowcasting & Decision Support System"
    )


    st.write(
        """
This project is a working prototype for urban flood
prediction and decision support.
"""
    )


    st.markdown("### 🎯 Main Objectives")

    st.markdown("""
- Predict flood depth
- Estimate flood risk
- Display flood-risk maps
- Provide 0–3 hour prototype forecast
- Identify potentially flooded roads
- Analyse drainage conditions
- Demonstrate flood-safe route suggestion
""")


    st.markdown("### 🧠 Technologies Used")

    st.markdown("""
- Python
- Pandas
- Scikit-learn
- Random Forest
- Streamlit
- PyDeck
- QGIS
- CSV
""")


    st.info(
        "Currently this is a working prototype using sample "
        "rainfall, elevation, drainage and flood-depth data. "
        "Real-time IMD/radar and actual road/drainage network "
        "integration are planned as the next stage."
    )
