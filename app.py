import streamlit as st


# PAGE CONFIG (AESTHETICS)

st.set_page_config(
    page_title="SpaceX Falcon 9 | ML Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# SIDEBAR (GLOBAL NAVIGATION AREA)

with st.sidebar:
    st.markdown("## 🚀 SpaceX Falcon 9")
    st.markdown("### Machine Learning Project")
    st.markdown("---")

    st.markdown(
        """
        **Pages in this App:**
        - 🔮 Model Prediction  
        - 📊 Data Dashboard  

        Use the sidebar to navigate.
        """
    )

    st.markdown("---")
    st.caption("Built with Streamlit • Localhost Demo")


# MAIN LANDING PAGE CONTENT

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #FFFFFF;
    }
    .sub-title {
        font-size: 20px;
        color: #CCCCCC;
    }
    .info-box {
        background-color: #1f2933;
        padding: 20px;
        border-radius: 12px;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">🚀 SpaceX Falcon 9 Launch Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Interactive ML Predictions & Launch Performance Dashboard</div>', unsafe_allow_html=True)

st.markdown("---")

st.markdown(
    """
    <div class="info-box">
        <h3>📌 What does this app do?</h3>
        <ul>
            <li><b>Predict</b> whether a Falcon 9 launch will successfully land</li>
            <li><b>Analyze</b> historical SpaceX launch data</li>
            <li><b>Visualize</b> success rates, payload trends, and launch sites</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-box">
        <h3>🧭 How to use</h3>
        <ol>
            <li>Open <b>Model Prediction</b> to test launch scenarios</li>
            <li>Open <b>Dashboard</b> to explore data with slicers</li>
        </ol>
    </div>
    """,
    unsafe_allow_html=True
)
