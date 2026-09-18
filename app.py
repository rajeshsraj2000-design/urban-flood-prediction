import streamlit as st
import pandas as pd
import pydeck as pdk
from sklearn.ensemble import RandomForestRegressor

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Flood AI",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS - APP STYLE
# ============================================================

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

.app-header {
    padding: 28px;
    border-radius: 22px;
    background: linear-gradient(
        135deg,
        #0b3d62,
        #1976d2
    );
    color: white;
    margin-bottom: 22px;
}

.app-header h1 {
    font-size: 38px;
    margin: 0;
    font-weight: 750;
}

.app-header p {
    font-size: 16px;
    margin-top: 8px;
}

.alert-box {
    padding: 20px;
    border-radius: 18px;
    background-color: #fff3cd;
    border: 1px solid #ffe69c;
    margin-bottom: 20px;
}

.info-box {
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #dddddd;
    background-color: #fafafa;
}

.section-title {
    font-size: 25px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 15px;
}

.app-footer {
    text-align: center;
    padding: 20px;
    color: #777;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================

data = pd.read_csv("flood_data.csv")

# ============================================================
# MACHINE LEARNING MODEL
# ============================================================

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

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## 🌧️ FLOOD AI")

st.sidebar.caption(
    "Urban Flood Nowcasting"
)

st.sidebar.divider()

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

st.sidebar.divider()

st.sidebar.markdown("### ⚙️ Simulation")

rainfall = st.sidebar.number_input(
    "Rainfall (mm)",
    min_value=0.0,
    value=70.0,
    step=1.0
)

elevation = st.sidebar.number_input(
    "Elevation (m)",
    min_value=0.0,
    value=7.0,
    step=0.5
)

drainage = st.sidebar.selectbox(
    "Drainage Condition",
    [
        "Good",
        "Poor",
        "Blocked"
    ]
)

drainage_score = {
    "Good": 3,
    "Poor": 2,
    "Blocked": 1
}[drainage]

# ============================================================
# PREDICTION
# ============================================================

new_data = pd.DataFrame({
    "Rainfall_mm": [rainfall],
    "Elevation_m": [elevation],
    "Drainage_Score": [drainage_score]
})

prediction = model.predict(new_data)[0]

# ============================================================
# RISK
# ============================================================

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

# ============================================================
# HOME
# ============================================================

if page == "🏠 Home":

    st.markdown("""
    <div class="app-header">

    <h1>🌧️ Flood AI</h1>

    <p>
    Urban Flood Nowcasting & Decision Support System
    </p>

    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # ALERT
    # --------------------------------------------------------

    if risk == "VERY HIGH":

        st.error(
            "🚨 VERY HIGH FLOOD RISK — Immediate monitoring required."
        )

    elif risk == "HIGH":

        st.warning(
            "⚠️ HIGH FLOOD RISK — Flood-prone areas should be monitored."
        )

    elif risk == "MEDIUM":

        st.warning(
            "🟡 MEDIUM FLOOD RISK — Continue monitoring."
        )

    else:

        st.success(
            "🟢 LOW FLOOD RISK — Current conditions are relatively safe."
        )

    # --------------------------------------------------------
    # MAIN METRICS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📊 Live Situation</div>',
        unsafe_allow_html=True
    )

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
            f"{risk_icon} {risk}"
        )

    with col4:

        st.metric(
            "🚰 Drainage",
            drainage
        )

    st.divider()

    # --------------------------------------------------------
    # QUICK ACTIONS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">⚡ Quick Monitoring</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "🌊 **Flood Prediction**\n\n"
            "Estimate current flood depth."
        )

    with col2:

        st.info(
            "🗺️ **Flood Map**\n\n"
            "View flood-risk locations."
        )

    with col3:

        st.info(
            "🚑 **Safe Route**\n\n"
            "Compare flood-safe routes."
        )

    st.divider()

    # --------------------------------------------------------
    # MAP
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">🗺️ Flood Risk Map</div>',
        unsafe_allow_html=True
    )

    st.image(
        "flood_map.png.png",
        use_container_width=True
    )

    st.caption(
        "QGIS-based Chennai prototype flood-risk map."
    )

    st.divider()

    # --------------------------------------------------------
    # SYSTEM FLOW
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">🔄 How the System Works</div>',
        unsafe_allow_html=True
    )

    st.code(
        "🌧️ Rainfall\n"
        "      ↓\n"
        "🗺️ Elevation / Terrain\n"
        "      ↓\n"
        "🚰 Drainage Condition\n"
        "      ↓\n"
        "🤖 Machine Learning\n"
        "      ↓\n"
        "🌊 Flood Depth\n"
        "      ↓\n"
        "🚨 Flood Risk\n"
        "      ↓\n"
        "🗺️ Map + 🛣️ Roads + 🚑 Safe Route"
    )

    st.divider()

    st.success(
        "✅ Flood AI prototype is running successfully."
    )

# ============================================================
# FLOOD PREDICTION
# ============================================================

elif page == "🌊 Flood Prediction":

    st.title("🌊 Flood Prediction")

    st.write(
        "Use the simulation controls in the sidebar "
        "to estimate flood depth."
    )

    st.divider()

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
            "Drainage",
            drainage
        )

    st.divider()

    st.subheader("🌊 Prediction Result")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Flood Depth",
            f"{prediction:.1f} cm"
        )

    with col2:

        st.metric(
            "Flood Risk",
            f"{risk_icon} {risk}"
        )

    if risk == "LOW":

        st.success(
            "🟢 Low flood risk"
        )

    elif risk == "MEDIUM":

        st.warning(
            "🟡 Medium flood risk"
        )

    elif risk == "HIGH":

        st.warning(
            "🟠 High flood risk"
        )

    else:

        st.error(
            "🔴 Very high flood risk"
        )

    st.divider()

    st.subheader("🤖 Machine Learning")

    st.write(
        "**Algorithm:** Random Forest Regressor"
    )

    st.write(
        "**Features:** Rainfall + Elevation + Drainage Score"
    )

# ============================================================
# FLOOD MAP
# ============================================================

elif page == "🗺️ Flood Map":

    st.title("🗺️ Flood Risk Map")

    st.write(
        "Prototype spatial flood-risk visualization."
    )

    st.image(
        "flood_map.png.png",
        use_container_width=True
    )

    st.caption(
        "QGIS-based Chennai prototype."
    )

    st.divider()

    st.subheader("📍 Interactive Flood Locations")

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

    def map_color(status):

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
    ].apply(map_color)

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

# ============================================================
# FORECAST
# ============================================================

elif page == "⏱️ Forecast":

    st.title("⏱️ 0–3 Hour Forecast")

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

        "Flood Depth (cm)": [

            round(prediction, 1),

            round(prediction * 1.15, 1),

            round(prediction * 1.30, 1),

            round(prediction * 1.50, 1),

            round(prediction * 1.70, 1)
        ]
    })

    st.dataframe(
        forecast_data,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("📈 Flood Trend")

    st.line_chart(
        forecast_data.set_index("Time")
    )

    st.warning(
        "⚠️ Prototype forecast. Real-time radar/nowcast "
        "integration is planned for the next development stage."
    )

# ============================================================
# ROADS
# ============================================================

elif page == "🛣️ Roads":

    st.title("🛣️ Flooded Road Detection")

    st.write(
        "Prototype road-level flood-risk assessment."
    )

    road_depths = pd.DataFrame({

        "Road": [
            "Road A",
            "Road B",
            "Road C",
            "Road D"
        ],

        "Flood Depth (cm)": [

            round(prediction * 0.25, 1),

            round(prediction * 0.60, 1),

            round(prediction, 1),

            round(prediction * 1.40, 1)
        ]
    })

    def road_status(depth):

        if depth < 5:
            return "🟢 SAFE"

        elif depth < 15:
            return "🟡 CAUTION"

        elif depth < 30:
            return "🟠 FLOOD RISK"

        else:
            return "🔴 AVOID"

    road_depths["Status"] = road_depths[
        "Flood Depth (cm)"
    ].apply(road_status)

    st.dataframe(
        road_depths,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    avoid_count = len(
        road_depths[
            road_depths["Status"] == "🔴 AVOID"
        ]
    )

    risk_count = len(
        road_depths[
            road_depths["Status"] == "🟠 FLOOD RISK"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🚫 Roads to Avoid",
            avoid_count
        )

    with col2:

        st.metric(
            "⚠️ Flood Risk Roads",
            risk_count
        )

# ============================================================
# DRAINAGE
# ============================================================

elif page == "🚰 Drainage":

    st.title("🚰 Urban Drainage Network")

    st.write(
        "Prototype drainage network showing "
        "manholes, junctions, pipes and outlet."
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

        "Capacity (L/s)": [
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

        if (
            row["Incoming Flow (L/s)"]
            <=
            row["Capacity (L/s)"]
        ):
            return "🟢 Normal"

        return "🔴 Over Capacity"

    drainage_data["Status"] = drainage_data.apply(
        drainage_status,
        axis=1
    )

    st.dataframe(
        drainage_data,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("🚧 Blockage Analysis")

    blockage = st.selectbox(
        "Drainage Condition",
        [
            "No Blockage",
            "Partial Blockage",
            "Severe Blockage"
        ]
    )

    if blockage == "No Blockage":

        factor = 1.0

    elif blockage == "Partial Blockage":

        factor = 0.6

    else:

        factor = 0.3

    capacity = 1000 * factor

    st.metric(
        "Effective Capacity",
        f"{capacity:.0f} L/s"
    )

    if capacity < 700:

        st.error(
            "🔴 Insufficient drainage capacity."
        )

    else:

        st.success(
            "🟢 Drainage capacity is sufficient."
        )

    st.divider()

    st.subheader("🗺️ Drainage Flow Map")

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
        get_source_position="[Start_Lon, Start_Lat]",
        get_target_position="[End_Lon, End_Lat]",
        get_width=6,
        get_color=[0, 120, 255]
    )

    risk_layer = pdk.Layer(
        "LineLayer",
        data=risk_pipes,
        get_source_position="[Start_Lon, Start_Lat]",
        get_target_position="[End_Lon, End_Lat]",
        get_width=8,
        get_color=[220, 0, 0]
    )

    node_layer = pdk.Layer(
        "ScatterplotLayer",
        data=drainage_nodes,
        get_position="[Longitude, Latitude]",
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
            "Node: {Node}\n"
            "Type: {Type}"
        }
    )

    st.pydeck_chart(
        drainage_deck
    )

    st.caption(
        "🔵 Normal pipe | 🔴 Over-capacity pipe | 🟠 Node"
    )

# ============================================================
# SAFE ROUTE
# ============================================================

elif page == "🚑 Safe Route":

    st.title("🚑 Flood-Safe Route")

    st.write(
        "Prototype route comparison based on flood depth."
    )

    route_data = pd.DataFrame({

        "Route": [
            "Route A",
            "Route B",
            "Route C"
        ],

        "Flood Depth (cm)": [
            8,
            18,
            32
        ],

        "Status": [
            "🟢 Safer",
            "🟡 Caution",
            "🔴 Avoid"
        ]
    })

    st.dataframe(
        route_data,
        use_container_width=True,
        hide_index=True
    )

    safe_route = route_data.loc[
        route_data["Flood Depth (cm)"].idxmin(),
        "Route"
    ]

    safe_depth = route_data[
        "Flood Depth (cm)"
    ].min()

    st.success(
        f"🚑 Suggested Safer Route: "
        f"{safe_route} "
        f"({safe_depth} cm predicted flood depth)"
    )

    st.info(
        "Future version can integrate actual road-network "
        "data and routing APIs."
    )

# ============================================================
# ABOUT
# ============================================================

elif page == "ℹ️ About":

    st.title("ℹ️ About Flood AI")

    st.markdown("""
    ## 🌧️ Urban Flood Nowcasting System

    A prototype decision-support system for urban flood
    monitoring and prediction.

    ### 🎯 Objective

    Estimate urban flood depth using:

    - Rainfall
    - Elevation
    - Drainage condition

    ### 🧠 Technologies

    | Technology | Purpose |
    |---|---|
    | Python | Data processing |
    | Random Forest | Flood prediction |
    | Streamlit | Web application |
    | QGIS | Flood mapping |
    | PyDeck | Interactive maps |
    | Pandas | Data handling |

    ### 🔄 System Flow

    Rainfall  
    ↓  
    Elevation  
    ↓  
    Drainage  
    ↓  
    Machine Learning  
    ↓  
    Flood Depth  
    ↓  
    Flood Risk  
    ↓  
    Maps + Roads + Safe Route
    """)

    st.divider()

    st.warning(
        "⚠️ Current version is a prototype using sample data. "
        "Real-time radar, validated flood observations and "
        "actual municipal drainage/road-network data can be "
        "integrated in the next development stage."
    )

    st.success(
        "✅ Urban Flood Nowcasting prototype completed."
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="app-footer">

🌧️ Urban Flood Nowcasting System |
Prototype Decision Support Dashboard

</div>
""", unsafe_allow_html=True)
