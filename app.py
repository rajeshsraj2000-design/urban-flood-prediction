import streamlit as st
import pandas as pd
import pydeck as pdk
from sklearn.ensemble import RandomForestRegressor

# -------------------------------------------------
# PAGE SETTINGS
# -------------------------------------------------
st.set_page_config(
    page_title="Urban Flood Nowcasting System",
    page_icon="🌧️",
    layout="wide"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------
st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    color: #666;
}

.alert-box {
    padding: 15px;
    border-radius: 10px;
    background-color: #fff3cd;
    border-left: 6px solid #ff9800;
    margin-bottom: 20px;
}

.section-title {
    font-size: 25px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown(
    '<div class="main-title">🌧️ FLOOD AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Urban Flood Nowcasting & Decision Support System</div>',
    unsafe_allow_html=True
)

st.divider()

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.title("🌧️ FLOOD AI")
st.sidebar.caption("Urban Flood Nowcasting System")

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

# -------------------------------------------------
# SIMULATION INPUTS
# -------------------------------------------------
st.sidebar.divider()
st.sidebar.subheader("⚙️ Simulation")

rainfall = st.sidebar.number_input(
    "Rainfall (mm)",
    min_value=0.0,
    value=70.0
)

elevation = st.sidebar.number_input(
    "Elevation (m)",
    min_value=0.0,
    value=7.0
)

drainage_condition = st.sidebar.selectbox(
    "Drainage Condition",
    ["Good", "Poor", "Blocked"]
)

drainage_score = {
    "Good": 3,
    "Poor": 2,
    "Blocked": 1
}[drainage_condition]

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
data = pd.read_csv("flood_data.csv")

X = data[
    [
        "Rainfall_mm",
        "Elevation_m",
        "Drainage_Score"
    ]
]

y = data["Flood_Depth_cm"]

# -------------------------------------------------
# TRAIN MODEL
# -------------------------------------------------
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# -------------------------------------------------
# CURRENT PREDICTION
# -------------------------------------------------
new_data = pd.DataFrame({
    "Rainfall_mm": [rainfall],
    "Elevation_m": [elevation],
    "Drainage_Score": [drainage_score]
})

prediction = model.predict(new_data)[0]

# -------------------------------------------------
# RISK
# -------------------------------------------------
if prediction < 5:
    risk = "LOW"
elif prediction < 15:
    risk = "MEDIUM"
elif prediction < 30:
    risk = "HIGH"
else:
    risk = "VERY HIGH"

# -------------------------------------------------
# HOME
# -------------------------------------------------
if page == "🏠 Home":

    if prediction >= 15:
        st.markdown(
            f"""
            <div class="alert-box">
            ⚠️ <b>{risk} FLOOD RISK</b><br>
            Flood-prone areas should be monitored.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.header("🌧️ Urban Flood Nowcasting")

    st.write(
        "An AI-assisted prototype for predicting urban flood "
        "depth using rainfall, elevation and drainage condition."
    )

    # Metrics
    st.subheader("📊 Live Situation")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🌧️ Rainfall",
            f"{rainfall:.1f} mm"
        )

    with col2:
        st.metric(
            "🌊 Flood Depth",
            f"{prediction:.1f} cm"
        )

    with col3:
        st.metric(
            "⚠️ Risk",
            risk
        )

    with col4:
        st.metric(
            "🚰 Drainage",
            drainage_condition
        )

    st.divider()

    # Quick monitoring
    st.subheader("⚡ Quick Monitoring")

    q1, q2, q3 = st.columns(3)

    with q1:
        st.info("🌊 Flood Prediction")

    with q2:
        st.info("🗺️ Flood Map")

    with q3:
        st.info("🚑 Safe Route")

    # QGIS map
    st.subheader("🗺️ Flood Risk Map")

    try:
        st.image("flood_map.png", width="stretch")
        st.caption(
            "QGIS-based Chennai prototype flood-risk map."
        )
    except Exception:
        st.warning(
            "Flood map image is not available."
        )

    # System flow
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


# -------------------------------------------------
# FLOOD PREDICTION
# -------------------------------------------------
elif page == "🌊 Flood Prediction":

    st.header("🌊 Flood Prediction")

    st.write(
        "The Random Forest model predicts flood depth "
        "from rainfall, elevation and drainage condition."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Rainfall",
            f"{rainfall:.1f} mm"
        )

    with col2:
        st.metric(
            "Elevation",
            f"{elevation:.1f} m"
        )

    with col3:
        st.metric(
            "Flood Depth",
            f"{prediction:.1f} cm"
        )

    st.divider()

    if risk == "LOW":
        st.success(f"🟢 Flood Risk: {risk}")

    elif risk == "MEDIUM":
        st.warning(f"🟡 Flood Risk: {risk}")

    elif risk == "HIGH":
        st.warning(f"🟠 Flood Risk: {risk}")

    else:
        st.error(f"🔴 Flood Risk: {risk}")

    st.subheader("📋 Input Data")

    input_table = pd.DataFrame({
        "Parameter": [
            "Rainfall",
            "Elevation",
            "Drainage Condition",
            "Drainage Score"
        ],
        "Value": [
            f"{rainfall:.1f} mm",
            f"{elevation:.1f} m",
            drainage_condition,
            drainage_score
        ]
    })

    st.table(input_table)

    st.info(
        "⚠️ This prototype uses sample training data. "
        "Real-time rainfall and terrain data can be integrated "
        "in the next development stage."
    )


# -------------------------------------------------
# FLOOD MAP
# -------------------------------------------------
elif page == "🗺️ Flood Map":

    st.header("🗺️ Flood Risk Map")

    try:
        st.image(
            "flood_map.png",
            width="stretch"
        )

        st.caption(
            "QGIS-based Chennai prototype flood-risk map."
        )

    except Exception:
        st.error(
            "❌ flood_map.png was not found."
        )

    st.divider()

    st.subheader("📍 Interactive Flood Location Map")

    map_data = data[
        [
            "Latitude",
            "Longitude",
            "Flood_Depth_cm"
        ]
    ].copy()

    def map_status(depth):

        if depth < 5:
            return "SAFE"

        elif depth < 15:
            return "CAUTION"

        elif depth < 30:
            return "FLOOD RISK"

        else:
            return "AVOID"

    map_data["Status"] = map_data[
        "Flood_Depth_cm"
    ].apply(map_status)

    def get_color(status):

        if status == "SAFE":
            return [0, 180, 0]

        elif status == "CAUTION":
            return [255, 200, 0]

        elif status == "FLOOD RISK":
            return [255, 120, 0]

        else:
            return [220, 0, 0]

    map_data["Color"] = map_data[
        "Status"
    ].apply(get_color)

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_data,
        get_position="[Longitude, Latitude]",
        get_fill_color="Color",
        get_radius=250,
        pickable=True
    )

    view_state = pdk.ViewState(
        latitude=13.0827,
        longitude=80.2707,
        zoom=10,
        pitch=0
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "text":
            "Flood Depth: {Flood_Depth_cm} cm\n"
            "Status: {Status}"
        }
    )

    st.pydeck_chart(deck)

    st.caption(
        "🟢 Safe | 🟡 Caution | 🟠 Flood Risk | 🔴 Avoid"
    )

    st.caption(
        "Prototype map uses sample Chennai coordinates."
    )


# -------------------------------------------------
# FORECAST
# -------------------------------------------------
elif page == "⏱️ Forecast":

    st.header("⏱️ 0–3 Hour Flood Forecast")

    st.write(
        "Prototype short-term flood-depth forecast."
    )

    forecast_data = pd.DataFrame({

        "Time": [
            "Now",
            "+30 min",
            "+1 hour",
            "+2 hours",
            "+3 hours"
        ],

        "Predicted Flood Depth (cm)": [

            round(prediction, 1),

            round(prediction * 1.15, 1),

            round(prediction * 1.30, 1),

            round(prediction * 1.50, 1),

            round(prediction * 1.70, 1)
        ]
    })

    st.table(forecast_data)

    st.subheader("📈 Forecast Chart")

    chart_data = forecast_data.set_index(
        "Time"
    )

    st.line_chart(
        chart_data[
            "Predicted Flood Depth (cm)"
        ]
    )

    st.warning(
        "⚠️ This is a prototype forecast. "
        "Real-time Doppler radar/nowcast data is not yet "
        "connected."
    )


# -------------------------------------------------
# ROADS
# -------------------------------------------------
elif page == "🛣️ Roads":

    st.header("🛣️ Flooded Road Detection")

    st.write(
        "The system identifies roads that may become "
        "unsafe based on predicted flood depth."
    )

    road_depths = pd.DataFrame({

        "Road": [
            "Road A",
            "Road B",
            "Road C",
            "Road D"
        ],

        "Predicted Flood Depth (cm)": [

            round(prediction * 0.25, 1),

            round(prediction * 0.60, 1),

            round(prediction, 1),

            round(prediction * 1.40, 1)
        ]
    })

    def get_status(depth):

        if depth < 5:
            return "🟢 SAFE"

        elif depth < 15:
            return "🟡 CAUTION"

        elif depth < 30:
            return "🟠 FLOOD RISK"

        else:
            return "🔴 AVOID"

    road_depths["Status"] = road_depths[
        "Predicted Flood Depth (cm)"
    ].apply(get_status)

    st.table(road_depths)

    st.info(
        "Prototype road detection. "
        "Actual OpenStreetMap/municipal road-network "
        "data can be integrated later."
    )


# -------------------------------------------------
# DRAINAGE
# -------------------------------------------------
elif page == "🚰 Drainage":

    st.header("🚰 Urban Drainage Network")

    st.write(
        "The drainage network represents manholes, "
        "junctions, pipes and outlet points."
    )

    drainage_data = pd.DataFrame({

        "Node": [
            "Manhole M1",
            "Junction J1",
            "Junction J2",
            "Outlet O1"
        ],

        "Type": [
            "Inlet",
            "Junction",
            "Junction",
            "Outlet"
        ],

        "Pipe Capacity (L/s)": [
            1000,
            800,
            600,
            1000
        ],

        "Incoming Flow (L/s)": [
            700,
            900,
            750,
            750
        ]
    })

    def drainage_status(row):

        if row["Incoming Flow (L/s)"] <= row[
            "Pipe Capacity (L/s)"
        ]:

            return "🟢 Normal"

        else:

            return "🔴 Over Capacity"

    drainage_data["Status"] = drainage_data.apply(
        drainage_status,
        axis=1
    )

    st.table(drainage_data)

    # Blockage
    st.subheader("🚧 Drainage Blockage Analysis")

    blockage = st.selectbox(
        "Select Drainage Condition",
        [
            "No Blockage",
            "Partial Blockage",
            "Severe Blockage"
        ]
    )

    if blockage == "No Blockage":
        blockage_factor = 1.0

    elif blockage == "Partial Blockage":
        blockage_factor = 0.6

    else:
        blockage_factor = 0.3

    base_capacity = 1000

    effective_capacity = (
        base_capacity * blockage_factor
    )

    st.metric(
        "Effective Drainage Capacity",
        f"{effective_capacity:.0f} L/s"
    )

    if effective_capacity < 700:

        st.error(
            "🔴 Drainage capacity is insufficient. "
            "Surcharge and surface flooding may occur."
        )

    else:

        st.success(
            "🟢 Drainage capacity is currently sufficient."
        )

    # Drainage network map
    st.subheader("🗺️ Drainage Network Flow Map")

    st.write(
        "The network shows the direction of stormwater "
        "flow through manholes, junctions and outlet."
    )

    drainage_nodes = pd.DataFrame({

        "Node": [
            "M1",
            "J1",
            "J2",
            "O1"
        ],

        "Latitude": [
            13.0827,
            13.0850,
            13.0800,
            13.0870
        ],

        "Longitude": [
            80.2707,
            80.2750,
            80.2650,
            80.2800
        ],

        "Type": [
            "Manhole",
            "Junction",
            "Junction",
            "Outlet"
        ]
    })

    pipe_map_data = pd.DataFrame({

        "Start": [
            "M1",
            "J1",
            "J2"
        ],

        "End": [
            "J1",
            "J2",
            "O1"
        ],

        "Flow": [
            700,
            900,
            750
        ],

        "Status": [
            "Normal",
            "Over Capacity",
            "Over Capacity"
        ],

        "Start_Lon": [
            80.2707,
            80.2750,
            80.2650
        ],

        "Start_Lat": [
            13.0827,
            13.0850,
            13.0800
        ],

        "End_Lon": [
            80.2750,
            80.2650,
            80.2800
        ],

        "End_Lat": [
            13.0850,
            13.0800,
            13.0870
        ]
    })

    normal_pipes = pipe_map_data[
        pipe_map_data["Status"] == "Normal"
    ]

    risk_pipes = pipe_map_data[
        pipe_map_data["Status"] == "Over Capacity"
    ]

    normal_layer = pdk.Layer(
        "LineLayer",
        data=normal_pipes,
        get_source_position=[
            "Start_Lon",
            "Start_Lat"
        ],
        get_target_position=[
            "End_Lon",
            "End_Lat"
        ],
        get_width=6,
        get_color=[0, 120, 255]
    )

    risk_layer = pdk.Layer(
        "LineLayer",
        data=risk_pipes,
        get_source_position=[
            "Start_Lon",
            "Start_Lat"
        ],
        get_target_position=[
            "End_Lon",
            "End_Lat"
        ],
        get_width=8,
        get_color=[220, 0, 0]
    )

    node_layer = pdk.Layer(
        "ScatterplotLayer",
        data=drainage_nodes,
        get_position=[
            "Longitude",
            "Latitude"
        ],
        get_radius=180,
        get_fill_color=[255, 165, 0],
        pickable=True
    )

    drainage_view = pdk.ViewState(
        latitude=13.0830,
        longitude=80.2720,
        zoom=13,
        pitch=0
    )

    drainage_deck = pdk.Deck(
        layers=[
            normal_layer,
            risk_layer,
            node_layer
        ],
        initial_view_state=drainage_view,
        tooltip={
            "text":
            "Node: {Node}\nType: {Type}"
        }
    )

    st.pydeck_chart(drainage_deck)

    st.caption(
        "🔵 Normal drainage pipe | "
        "🔴 Over-capacity drainage pipe | "
        "🟠 Node"
    )

    # Pipe flow
    st.subheader("💧 Drainage Pipe Flow")

    pipe_data = pd.DataFrame({

        "Pipe": [
            "M1 → J1",
            "J1 → J2",
            "J2 → O1"
        ],

        "Flow Rate (L/s)": [
            700,
            900,
            750
        ],

        "Status": [
            "🟢 Normal",
            "🔴 Over Capacity",
            "🔴 Over Capacity"
        ]
    })

    st.table(pipe_data)

    st.info(
        "💧 Stormwater flows from the inlet/manhole "
        "through junctions and finally reaches the outlet."
    )


# -------------------------------------------------
# SAFE ROUTE
# -------------------------------------------------
elif page == "🚑 Safe Route":

    st.header("🚑 Flood-Safe Route Suggestion")

    st.write(
        "The prototype compares routes based on predicted "
        "flood depth."
    )

    route_data = pd.DataFrame({

        "Route": [
            "Route A",
            "Route B",
            "Route C"
        ],

        "Predicted Flood Depth (cm)": [
            8,
            18,
            32
        ]
    })

    st.table(route_data)

    safe_route = route_data.loc[
        route_data[
            "Predicted Flood Depth (cm)"
        ].idxmin(),
        "Route"
    ]

    safe_depth = route_data[
        "Predicted Flood Depth (cm)"
    ].min()

    st.success(
        f"🚑 Suggested Safer Route: "
        f"{safe_route} "
        f"({safe_depth} cm predicted flood depth)"
    )

    st.info(
        "Prototype demonstration. "
        "Future version can use real road-network "
        "and GIS routing data."
    )


# -------------------------------------------------
# ABOUT
# -------------------------------------------------
elif page == "ℹ️ About":

    st.header("ℹ️ About the Project")

    st.write(
        "Urban Flood Nowcasting System is an AI-assisted "
        "prototype designed to predict urban flood risk "
        "at a local level."
    )

    st.subheader("🎯 Main Objective")

    st.write(
        "Predict flood depth and risk using rainfall, "
        "elevation and drainage conditions."
    )

    st.subheader("🤖 Technologies Used")

    technologies = pd.DataFrame({

        "Technology": [
            "Python",
            "Random Forest",
            "QGIS",
            "Streamlit",
            "PyDeck",
            "CSV Dataset"
        ],

        "Purpose": [
            "Data processing and prediction",
            "Flood prediction model",
            "Flood-risk mapping",
            "Web dashboard",
            "Interactive maps",
            "Prototype training data"
        ]
    })

    st.table(technologies)

    st.subheader("🔄 System Architecture")

    st.markdown("""
    🌧️ Rainfall Data

    ↓

    🗺️ DEM / Elevation

    ↓

    🚰 Drainage Network

    ↓

    🤖 Machine Learning

    ↓

    🌊 Flood Depth Prediction

    ↓

    🚨 Flood Risk

    ↓

    🗺️ GIS Dashboard

    ↓

    🛣️ Flood-Safe Route
    """)

    st.subheader("🚀 Future Development")

    st.write("""
    • Real-time Doppler radar rainfall integration

    • High-resolution DEM integration

    • Actual urban drainage network

    • OpenStreetMap road-network integration

    • Real-time 0–3 hour flood nowcasting

    • Emergency route optimisation

    • Mobile application
    """)

    st.warning(
        "⚠️ Current version is a working prototype using "
        "sample data. It is not yet a validated real-time "
        "Chennai flood prediction system."
    )

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.divider()

st.caption(
    "🌧️ Urban Flood Nowcasting System | "
    "AI-assisted prototype | "
    "Sample data demonstration"
)
