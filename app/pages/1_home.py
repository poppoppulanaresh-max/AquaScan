import streamlit as st
from app.styles.theme import inject_theme
from app.components.header import render_header
from app.components.metric_card import render_metric_card
from src.database.repository import Repository

# Apply styling
inject_theme()

# Render warning banner and page title
render_header("AI-Powered River Microplastic Pollution Detection")

# Initialize database repository
try:
    repo = Repository()
    stats = repo.get_statistics()
except Exception as e:
    print(f"[Home] Database stats loading error: {str(e)}")
    stats = {
        'total_scans': 0,
        'rivers_monitored': 0,
        'avg_density': 0.0,
        'critical_alerts': 0
    }

# 1. HERO SECTION
st.markdown(
    """
    <div class="glass-card" style="text-align: center; padding: 3rem 1.5rem !important; margin-bottom: 2rem;">
        <h1 style="font-size: 3.5rem; margin-bottom: 10px; font-family: 'Space Grotesk', sans-serif;">
            <span class="wave-accent">🌊</span> AQUASCAN
        </h1>
        <p style="font-size: 1.3rem; color: #90CAF9; margin-bottom: 25px; font-family: 'Inter', sans-serif;">
            AI-Powered River Microplastic Pollution Detection & Analysis
        </p>
        <p style="max-width: 800px; margin: 0 auto 30px auto; font-size: 1.05rem; line-height: 1.7; color: #E0F7FA;">
            AquaScan leverages advanced Computer Vision (YOLOv8) and Deep Learning (CSRNet) to detect, 
            classify, and quantify microplastic particulates in river water bodies. Providing immediate 
            visual analytics, severity mapping, and compliance reports for researchers and environmental authorities.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# 2. LIVE STATS ROW
st.markdown("### 📊 System Live Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    render_metric_card("Total Scans Run", f"{stats['total_scans']}", "🔬")
with col2:
    render_metric_card("Rivers Monitored", f"{stats['rivers_monitored']}", "🗺️")
with col3:
    render_metric_card("Avg Density (P/L)", f"{stats['avg_density']:.1f}", "🧪")
with col4:
    # Severity critical highlights
    render_metric_card("Critical Alerts", f"{stats['critical_alerts']}", "🚨")

st.markdown("<br/>", unsafe_allow_html=True)

# 3. HOW IT WORKS
st.markdown("### ⚙️ How It Works")
step_col1, step_col2, step_col3, step_col4 = st.columns(4)

with step_col1:
    st.markdown(
        """
        <div class="glass-card" style="height: 100%; text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 10px;">📸</div>
            <h4 style="color: #00B4D8; margin-bottom: 10px;">1. Upload Photo</h4>
            <p style="font-size: 0.9rem; color: #90CAF9; line-height: 1.5;">
                Capture a high-res smartphone photo of a river water sample and upload it to the platform.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with step_col2:
    st.markdown(
        """
        <div class="glass-card" style="height: 100%; text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 10px;">🤖</div>
            <h4 style="color: #00B4D8; margin-bottom: 10px;">2. AI Detection</h4>
            <p style="font-size: 0.9rem; color: #90CAF9; line-height: 1.5;">
                YOLOv8 neural network instantly locates and identifies particles (fragment, fiber, pellet, film).
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with step_col3:
    st.markdown(
        """
        <div class="glass-card" style="height: 100%; text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 10px;">📈</div>
            <h4 style="color: #00B4D8; margin-bottom: 10px;">3. Density Analysis</h4>
            <p style="font-size: 0.9rem; color: #90CAF9; line-height: 1.5;">
                CSRNet estimates the particle density mapping to compute equivalent particles per liter.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with step_col4:
    st.markdown(
        """
        <div class="glass-card" style="height: 100%; text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 10px;">🗺️</div>
            <h4 style="color: #00B4D8; margin-bottom: 10px;">4. Pollution Map</h4>
            <p style="font-size: 0.9rem; color: #90CAF9; line-height: 1.5;">
                Submissions map globally onto a Folium heatmap to identify regional pollution clusters.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br/>", unsafe_allow_html=True)

# 4. RESEARCH MOTIVATION
st.markdown("### 🔬 Research Motivation")
m_col1, m_col2, m_col3 = st.columns(3)

with m_col1:
    st.markdown(
        """
        <div class="glass-card" style="height: 100%;">
            <h4 style="color: #FF5722;">8 Million Tons</h4>
            <p style="font-size: 0.9rem; color: #E0F7FA; line-height: 1.6;">
                Of plastic enters our oceans yearly, with major river channels like the Krishna and Godavari acting as primary conduits for terrestrial plastic waste.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with m_col2:
    st.markdown(
        """
        <div class="glass-card" style="height: 100%;">
            <h4 style="color: #FF5722;">Bioaccumulation</h4>
            <p style="font-size: 0.9rem; color: #E0F7FA; line-height: 1.6;">
                Microplastics (< 5mm) are ingested by aquatic organisms, carrying toxins up the food chain and eventually posing risks to human health.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with m_col3:
    st.markdown(
        """
        <div class="glass-card" style="height: 100%;">
            <h4 style="color: #FF5722;">Data Gap</h4>
            <p style="font-size: 0.9rem; color: #E0F7FA; line-height: 1.6;">
                Traditional monitoring requires expensive lab chromatography. AquaScan offers a low-cost, immediate screening tool for rapid field deployment.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br/><br/>", unsafe_allow_html=True)

# 5. CALL TO ACTION
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    if st.button("🚀 START SCANNING NOW", use_container_width=True):
        st.switch_page("pages/2_upload.py")
