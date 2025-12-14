import streamlit as st
import pandas as pd
import plotly.express as px
import os
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# ==================================================
# GLOBAL PAGE STYLING (FONTS + SPACING)
# ==================================================
st.markdown(
    """
    <style>
        .main-title {
            font-size: 38px;
            font-weight: 700;
        }
        .section-title {
            font-size: 26px;
            font-weight: 600;
            margin-top: 40px;
        }
        .subtext {
            font-size: 18px;
            color: #6c757d;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ==================================================
# PATH SETUP
# ==================================================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "interim", "cleaned_launches.csv")

# ==================================================
# LOAD DATA
# ==================================================
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

# --------------------------------------------------
# PRECOMPUTED MAP DATA (GROUND TRUTH)
# --------------------------------------------------
site_df = pd.DataFrame({
    "LaunchSite": [
        "CCSFS SLC 40",
        "VAFB SLC 4E",
        "KSC LC 39A",
        "Kwajalein Atoll"
    ],
    "Latitude": [
        28.561857,
        34.632093,
        28.608058,
        9.047721
    ],
    "Longitude": [
        -80.577366,
        -120.610829,
        -80.603956,
        167.743129
    ],
    "class": [
        0.642857,
        0.766667,
        0.827586,
        0.000000
    ]
})


# ==================================================
# PAGE HEADER
# ==================================================
st.markdown("📊 <span class='main-title'>SpaceX Falcon 9 – Launch Dashboard</span>", unsafe_allow_html=True)
st.markdown("<span class='subtext'>Interactive analysis of Falcon 9 launch performance</span>", unsafe_allow_html=True)
st.markdown("---")

# ==================================================
# SIDEBAR FILTERS (POWER BI STYLE)
# ==================================================
with st.sidebar:
    st.markdown("## 🎛 Filters")

    launch_sites = st.multiselect(
        "Launch Site",
        options=sorted(df["LaunchSiteName"].unique()),
        default=sorted(df["LaunchSiteName"].unique())
    )

    orbits = st.multiselect(
        "Orbit",
        options=sorted(df["Orbit"].unique()),
        default=sorted(df["Orbit"].unique())
    )

    payload_range = st.slider(
        "Payload Mass (kg)",
        int(df["PayloadMass"].min()),
        int(df["PayloadMass"].max()),
        (int(df["PayloadMass"].min()), int(df["PayloadMass"].max()))
    )

    outcome = st.radio("Outcome", ["All", "Success", "Failure"])

# ==================================================
# APPLY FILTERS
# ==================================================
filtered_df = df[
    (df["LaunchSiteName"].isin(launch_sites)) &
    (df["Orbit"].isin(orbits)) &
    (df["PayloadMass"].between(payload_range[0], payload_range[1]))
]

if outcome == "Success":
    filtered_df = filtered_df[filtered_df["class"] == 1]
elif outcome == "Failure":
    filtered_df = filtered_df[filtered_df["class"] == 0]

# ==================================================
# KPI SECTION
# ==================================================
k1, k2, k3 = st.columns(3)

k1.metric("🚀 Total Launches", len(filtered_df))
k2.metric("✅ Successful Landings", int(filtered_df["class"].sum()))
success_rate = filtered_df["class"].mean() * 100 if len(filtered_df) > 0 else 0
k3.metric("📈 Success Rate", f"{success_rate:.2f}%")

# ==================================================
# SUCCESS RATE BY LAUNCH SITE
# ==================================================
st.markdown("<div class='section-title'>Success Rate by Launch Site</div>", unsafe_allow_html=True)

fig_site = px.bar(
    filtered_df.groupby("LaunchSiteName")["class"].mean().reset_index(),
    x="LaunchSiteName",
    y="class",
    labels={"class": "Success Rate"},
    height=500,
    color="class",
    color_continuous_scale="Blues"
)
st.plotly_chart(fig_site, use_container_width=True)

# ==================================================
# SUCCESS RATE BY ORBIT
# ==================================================
st.markdown("<div class='section-title'>Success Rate by Orbit</div>", unsafe_allow_html=True)

fig_orbit = px.bar(
    filtered_df.groupby("Orbit")["class"].mean().reset_index(),
    x="Orbit",
    y="class",
    labels={"class": "Success Rate"},
    height=500,
    color="class",
    color_continuous_scale="Viridis"
)
st.plotly_chart(fig_orbit, use_container_width=True)

# ==================================================
# PAYLOAD VS SUCCESS SCATTER
# ==================================================
st.markdown("<div class='section-title'>Payload Mass vs Launch Outcome</div>", unsafe_allow_html=True)

fig_payload = px.scatter(
    filtered_df,
    x="PayloadMass",
    y="class",
    color="class",
    height=550,
    labels={"class": "Outcome (0 = Fail, 1 = Success)"},
    opacity=0.7
)
st.plotly_chart(fig_payload, use_container_width=True)

# ==================================================
# HEATMAP — PAYLOAD MASS vs ORBIT (SUCCESS RATE)
# ==================================================
st.markdown(
    "<div class='section-title'>Heatmap: Payload Mass vs Orbit (Success Rate)</div>",
    unsafe_allow_html=True
)

# Create payload bins (numeric)
bins = pd.cut(filtered_df["PayloadMass"], bins=6)

# Convert bins to readable strings (IMPORTANT FIX)
filtered_df = filtered_df.copy()
filtered_df["PayloadBin"] = bins.astype(str)

heatmap_df = (
    filtered_df
    .groupby(["Orbit", "PayloadBin"])["class"]
    .mean()
    .reset_index()
)

fig_heatmap = px.imshow(
    heatmap_df.pivot(
        index="Orbit",
        columns="PayloadBin",
        values="class"
    ),
    color_continuous_scale="Turbo",
    height=600,
    labels=dict(color="Success Rate"),
    aspect="auto"
)

st.plotly_chart(fig_heatmap, use_container_width=True)


# ==================================================
# FOLIUM MAP (JUPYTER-STYLE, ROCKET ICONS)
# ==================================================
st.markdown("<div class='section-title'>🌍 Launch Sites – Success Rate Map</div>", unsafe_allow_html=True)


spacex_map = folium.Map(
    location=[39.8283, -98.5795],
    zoom_start=4,
    tiles="OpenStreetMap"
)


marker_cluster = MarkerCluster().add_to(spacex_map)

def get_color(rate):
    if rate >= 0.75:
        return "green"
    elif rate >= 0.5:
        return "orange"
    else:
        return "red"

for _, row in site_df.iterrows():
    popup_text = f"""
    <strong>{row['LaunchSite']}</strong><br>
    Success Rate: {row['class']:.2%}
    """
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=popup_text,
        icon=folium.Icon(
            color=get_color(row["class"]),
            icon="rocket",
            prefix="fa"
        )
    ).add_to(marker_cluster)

st_folium(spacex_map, width=1100, height=600)

st.caption("🚀 Map updates dynamically with dashboard filters")
