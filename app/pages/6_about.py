import streamlit as st
from app.styles.theme import inject_theme
from app.components.header import render_header

# Apply styles
inject_theme()

# Title
render_header("Project Methodology & Details")

# 1. PROJECT STORY
st.markdown("### 📖 The AquaScan Story")
st.markdown(
    """
    <div class="glass-card">
        <p style="font-size: 1rem; line-height: 1.7; color: #E0F7FA; margin-bottom: 15px;">
            AquaScan was conceived in <b>Guntur, Andhra Pradesh, India</b>, by a student developer aiming to address a 
            critical environmental crisis. The local river channels—specifically the <b>Krishna River</b>, <b>Godavari River</b>, 
            and <b>Musi River</b>—are essential lifelines for agricultural, municipal, and ecological systems in AP. 
            However, these waterways suffer from rising microplastic debris accumulation.
        </p>
        <p style="font-size: 1rem; line-height: 1.7; color: #E0F7FA;">
            Traditional testing protocols involve mass spectrometry or micro-Raman spectroscopy. These methods, 
            while highly accurate, require transport to specialized laboratory centers, expensive machinery, and 
            days of waiting time. AquaScan solves this latency by introducing a low-cost, AI-powered smartphone screening 
            framework. It enables NGOs, student teams, and local government water boards to log immediate, geotagged 
            pollution indicators directly in the field.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# 2. ARCHITECTURE DIAGRAM
st.markdown("### 🏗️ ML Pipeline Architecture")
st.markdown(
    """
    <div class="glass-card" style="font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; line-height: 1.5; color: #00B4D8; overflow-x: auto; background-color: rgba(3, 4, 94, 0.4) !important;">
    [Smartphone Photo Upload] <br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼<br>
    [Image Preprocessing Pipeline] ───► Denoise (fastNlMeans) & Contrast (CLAHE)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├──────────────────────────────────┐<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼<br>
    [YOLOv8 Particle Detector] &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[CSRNet Density Estimator]<br>
    &nbsp;&nbsp;(Identifies BBoxes & Classes) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(Dilated CNN count map)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─────────────────┬────────────────┘<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[XGBoost Severity Classifier]<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(low/medium/high/critical)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Reporting & Visualization]<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(Streamlit, Folium Map, FPDF2 Report)<br>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br/>", unsafe_allow_html=True)

# 3. RESEARCH NOVELTY
st.markdown("### 🔬 Scientific Novelty")
n_col1, n_col2, n_col3 = st.columns(3)

with n_col1:
    st.markdown(
        """
        <div class="glass-card" style="height: 100%;">
            <div style="font-size: 1.5rem; margin-bottom: 10px;">📐</div>
            <h4 style="color: #00B4D8; margin-bottom: 8px;">Hybrid Counting</h4>
            <p style="font-size: 0.88rem; color: #E0F7FA; line-height: 1.5;">
                Combines sparse regression boxes (YOLO) with dense dilated density maps (CSRNet) to ensure robust 
                particle counts even when particulates overlap.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with n_col2:
    st.markdown(
        """
        <div class="glass-card" style="height: 100%;">
            <div style="font-size: 1.5rem; margin-bottom: 10px;">⚡</div>
            <h4 style="color: #00B4D8; margin-bottom: 8px;">Sub-Minute Processing</h4>
            <p style="font-size: 0.88rem; color: #E0F7FA; line-height: 1.5;">
                Fully automated pipeline preprocesses, predicts, logs, maps, and generates downloadable 
                environmental compliance PDFs in under 10 seconds.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with n_col3:
    st.markdown(
        """
        <div class="glass-card" style="height: 100%;">
            <div style="font-size: 1.5rem; margin-bottom: 10px;">🌐</div>
            <h4 style="color: #00B4D8; margin-bottom: 8px;">Crowdsourced GIS</h4>
            <p style="font-size: 0.88rem; color: #E0F7FA; line-height: 1.5;">
                Decentralized structure allows field surveyors to append offline GPS data, creating an interactive, 
                dynamic global map of river pollution.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br/>", unsafe_allow_html=True)

# 4. TECH STACK
st.markdown("### 🛠️ Technology Stack")
st.markdown(
    """
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 25px;">
        <div class="glass-card" style="text-align: center; margin: 0 !important; padding: 1rem !important;">
            <b style="color: #00B4D8;">Frontend</b><br/>Streamlit
        </div>
        <div class="glass-card" style="text-align: center; margin: 0 !important; padding: 1rem !important;">
            <b style="color: #00B4D8;">Computer Vision</b><br/>YOLOv8 (Ultralytics)
        </div>
        <div class="glass-card" style="text-align: center; margin: 0 !important; padding: 1rem !important;">
            <b style="color: #00B4D8;">Density Engine</b><br/>CSRNet (PyTorch)
        </div>
        <div class="glass-card" style="text-align: center; margin: 0 !important; padding: 1rem !important;">
            <b style="color: #00B4D8;">Classifier</b><br/>XGBoost Multi-Class
        </div>
        <div class="glass-card" style="text-align: center; margin: 0 !important; padding: 1rem !important;">
            <b style="color: #00B4D8;">Database</b><br/>SQLite & Supabase
        </div>
        <div class="glass-card" style="text-align: center; margin: 0 !important; padding: 1rem !important;">
            <b style="color: #00B4D8;">GIS Mapping</b><br/>Folium & CartoDB
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 5. FIELD METHODOLOGY
st.markdown("### 📋 Field Sampling Guide")
st.markdown(
    """
    <div class="glass-card" style="line-height: 1.6;">
        <b>To achieve maximum accuracy in AI model detections, follow these sampling rules:</b><br/>
        <ol style="margin-left: 20px; color: #E0F7FA; font-size: 0.95rem;">
            <li><b>Lighting:</b> Capture photos in diffuse daylight. Avoid direct glare or strong surface reflections from the sun.</li>
            <li><b>Framing:</b> Hold the smartphone camera parallel to the water container (about 15-20 cm away). Avoid capturing container edges.</li>
            <li><b>Volume:</b> Filter exactly 1 Liter of river water through a fine mesh paper and place the filtrate in a clean petri dish. Photo should cover the petri dish base.</li>
            <li><b>Turbidity:</b> If water is murky/turbid, make sure to enable the "Turbidity Color Balancing" preprocessor option in the app.</li>
        </ol>
    </div>
    """,
    unsafe_allow_html=True
)

# 6. FUTURE ROADMAP & AUTHOR INFO
st.markdown("### 🗺️ Future Roadmap & Development Team")
col_road, col_auth = st.columns(2)

with col_road:
    st.markdown(
        """
        <div class="glass-card" style="height: 100%;">
            <h4 style="color: #00B4D8; margin-bottom: 10px;">Roadmap</h4>
            <ul style="margin-left: 20px; color: #E0F7FA; font-size: 0.9rem; line-height: 1.6;">
                <li>Deploy real-time edge inference on Android/iOS via ONNX runtime.</li>
                <li>Incorporate multispectral image sensors for polymer type identification (PET/HDPE/PVC).</li>
                <li>Integrate automated drone water samplers with AquaScan APIs.</li>
                <li>Build temporal prediction models for seasonal runoff variations.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_auth:
    st.markdown(
        """
        <div class="glass-card" style="height: 100%;">
            <h4 style="color: #00B4D8; margin-bottom: 10px;">Author Information</h4>
            <p style="font-size: 0.92rem; line-height: 1.6; color: #E0F7FA;">
                <b>Developer:</b> Student Developer, Guntur, Andhra Pradesh, India<br/>
                <b>Affiliation:</b> Department of Computer Science & Environmental Studies, AP, India<br/>
                <b>Project Phase:</b> Academic Demonstration v1.0<br/>
                <b>Target Rivers:</b> Krishna, Godavari, Musi
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br/>", unsafe_allow_html=True)

# 8. GITHUB LINK BUTTON
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown(
        """
        <a href="https://github.com/BlueGuard-AI/AquaScan" target="_blank" style="text-decoration: none;">
            <button style="
                width: 100%;
                background-color: #023E8A;
                color: #E0F7FA;
                border: 1px solid rgba(0,180,216,0.5);
                border-radius: 8px;
                padding: 10px;
                font-family: 'Space Grotesk', sans-serif;
                font-weight: bold;
                font-size: 1rem;
                cursor: pointer;
                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
            " onmouseover="this.style.backgroundColor='#00B4D8'; this.style.color='#03045E';" onmouseout="this.style.backgroundColor='#023E8A'; this.style.color='#E0F7FA';">
                💻 VIEW ON GITHUB
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )
