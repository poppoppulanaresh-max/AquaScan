import streamlit as st
import io
import plotly.graph_objects as go

# Import styling & components
from app.styles.theme import inject_theme
from app.components.header import render_header
from app.components.metric_card import render_metric_card
from app.components.severity_gauge import render_severity_gauge
from app.components.particle_chart import render_particle_chart
from src.database.repository import Repository
from src.utils.config import SEVERITY_COLORS

# Apply styles
inject_theme()

# Page title
render_header("Detection Results Analysis")

# 1. Guard against empty session state
if 'detection_result' not in st.session_state or st.session_state['detection_result'] is None:
    st.markdown(
        """
        <div class="glass-card" style="text-align: center; padding: 3rem !important;">
            <div style="font-size: 3rem; margin-bottom: 20px;">⚠️</div>
            <h3>No Active Scan Data Found</h3>
            <p style="color: #90CAF9; margin-bottom: 25px;">
                You must upload a water sample image and run the detection pipeline before viewing results.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("🔌 GO TO UPLOAD PAGE", use_container_width=True):
        st.switch_page("pages/2_upload.py")
    st.stop()

# Retrieve values from Session State
result = st.session_state['detection_result']
original_img = st.session_state['uploaded_image']
annotated_img = st.session_state['annotated_image']
pdf_bytes = st.session_state.get('pdf_report_bytes')
gps_lat = st.session_state.get('gps_lat')
gps_lon = st.session_state.get('gps_lon')

# Render additional mock banner if the results are mock-based
if result.get('is_mock'):
    st.warning("🔬 Displaying simulated results. Upload model weights to models/weights/best.pt for live detection.")

# 2. IMAGE COMPARISON ROW
st.markdown("### 🖼️ Visual Analysis")
img_col1, img_col2 = st.columns(2)

with img_col1:
    st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
    st.image(original_img, caption="Original Smartphone Photo", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with img_col2:
    st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
    st.image(annotated_img, caption="Annotated AI Detections", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# 3. DETAILED METRICS & CHARTS GRID
st.markdown("### 📊 Detections Dashboard")
grid_col_left, grid_col_right = st.columns([1, 1])

with grid_col_left:
    # 5 Key Metrics in 2 columns
    st.markdown("##### Particle Class Quantifications")
    class_counts = result.get('class_counts', {})
    
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        render_metric_card("Total Particles", f"{result['particle_count']}", "🔍")
        render_metric_card("Fragments count", f"{class_counts.get('fragment', 0)}", "🔸")
        render_metric_card("Fibers count", f"{class_counts.get('fiber', 0)}", "🧵")
    with m_col2:
        render_metric_card("Pellets count", f"{class_counts.get('pellet', 0)}", "🟢")
        render_metric_card("Films count", f"{class_counts.get('film', 0)}", "📄")
        
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Density display
    st.markdown("##### Est. Concentration Density")
    density = result['density_per_liter']
    severity = result['severity']
    color = SEVERITY_COLORS.get(severity.lower(), '#00B4D8')
    
    st.markdown(
        f"""
        <div class="glass-card" style="text-align: center;">
            <div class="metric-label">Estimated density per liter</div>
            <div class="metric-value" style="font-size: 2.5rem !important;">{density:.2f} P/L</div>
            <div class="severity-badge" style="background-color: {color}; margin-top: 15px;">
                SEVERITY: {severity.upper()}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with grid_col_right:
    # Severity Gauge
    st.markdown("##### Severity Indicator")
    st.markdown('<div class="glass-card" style="padding: 0.5rem !important;">', unsafe_allow_html=True)
    render_severity_gauge(severity)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Donut Chart
    st.markdown("##### Composition Ratios")
    st.markdown('<div class="glass-card" style="padding: 0.5rem !important;">', unsafe_allow_html=True)
    render_particle_chart(class_counts)
    st.markdown('</div>', unsafe_allow_html=True)

# Confidence score indicator
st.markdown("##### Detection Confidence Level")
conf = result['confidence']
fig_conf = go.Figure(go.Bar(
    x=[conf * 100],
    y=["Confidence"],
    orientation='h',
    marker=dict(color='#00B4D8', line=dict(color='#023E8A', width=1.5)),
    text=[f"{conf * 100:.1f}%"],
    textposition='auto',
    hoverinfo='none'
))
fig_conf.update_layout(
    xaxis=dict(range=[0, 100], gridcolor='rgba(0,180,216,0.1)', tickfont=dict(color='#90CAF9')),
    yaxis=dict(showticklabels=False),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#E0F7FA', family='JetBrains Mono'),
    height=80,
    margin=dict(t=5, b=5, l=5, r=5)
)
st.plotly_chart(fig_conf, use_container_width=True)

# Geolocation details
st.markdown("##### Geolocation Metadata")
if gps_lat is not None and gps_lon is not None:
    st.markdown(
        f"""
        <div class="glass-card">
            📍 <b>Location Name:</b> {result.get('location_name', 'Not Provided')} &nbsp;&nbsp;|&nbsp;&nbsp; 
            🧭 <b>Coordinates:</b> {gps_lat:.6f}, {gps_lon:.6f}
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <div class="glass-card" style="color: #90CAF9;">
            📍 No GPS location coordinate data attached to this water sample.
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br/>", unsafe_allow_html=True)

# 4. DOWNLOADS AND DB SAVES
st.markdown("### 💾 Report & Data Storage")
actions_col1, actions_col2 = st.columns(2)

with actions_col1:
    if pdf_bytes:
        st.download_button(
            label="📄 DOWNLOAD PDF REPORT",
            data=pdf_bytes,
            file_name=f"aquascan_report_{result['id'][:8]}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    else:
        st.button("📄 DOWNLOAD PDF REPORT (N/A)", disabled=True, use_container_width=True)

with actions_col2:
    # Check if submission was already saved
    if st.session_state.get('submission_id') is not None:
        st.button(f"✅ RECORD SAVED IN DATABASE", disabled=True, use_container_width=True)
        st.success(f"Data stored successfully! Reference ID: {st.session_state['submission_id']}")
    else:
        if st.button("💾 SAVE RECORD TO DATABASE", use_container_width=True):
            with st.spinner("Saving results to database..."):
                try:
                    repo = Repository()
                    saved_id = repo.save_submission(result)
                    st.session_state['submission_id'] = saved_id
                    st.rerun() # Rerun page to update the button state to disabled
                except Exception as e:
                    st.error(f"Failed to save record to database: {str(e)}")
