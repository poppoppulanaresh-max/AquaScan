import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Import styling & clients
from app.styles.theme import inject_theme
from app.components.header import render_header
from src.database.repository import Repository
from src.utils.config import SEVERITY_COLORS

# Apply styles
inject_theme()

# Page title
render_header("Global Trend Analytics")

# Load all submissions
try:
    repo = Repository()
    submissions = repo.get_all_submissions()
except Exception as e:
    print(f"[Analytics Page] DB loading error: {str(e)}")
    submissions = []

# Guard against empty database
if not submissions:
    st.markdown(
        """
        <div class="glass-card" style="text-align: center; padding: 3rem !important;">
            <div style="font-size: 3rem; margin-bottom: 20px;">📊</div>
            <h3>No Analytics Data Available</h3>
            <p style="color: #90CAF9; margin-bottom: 25px;">
                There are currently no scans saved in the database. 
                Please upload an image, run the detection, and click "Save Record to Database" to generate trends.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("🔌 GO TO UPLOAD PAGE", use_container_width=True):
        st.switch_page("pages/2_upload.py")
    st.stop()

# Load into DataFrame
df = pd.DataFrame(submissions)
df['date'] = df['timestamp'].apply(lambda x: x[:10])

# 1. TIME SERIES TRENDS
st.markdown("### 📈 Pollution Concentration Trends Over Time")
time_df = df.groupby('date').agg(
    scans_count=('id', 'count'),
    avg_density=('density_per_liter', 'mean')
).reset_index()

# Multi-axis chart or side by side
col_t1, col_t2 = st.columns(2)
with col_t1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("##### Average Density over Time")
    fig_line = px.line(
        time_df, x='date', y='avg_density',
        labels={'date': 'Date', 'avg_density': 'Avg Density (P/L)'},
        markers=True, template="plotly_dark"
    )
    fig_line.update_traces(line_color='#00B4D8', marker=dict(color='#023E8A'))
    fig_line.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E0F7FA', family='Inter, sans-serif')
    )
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_t2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("##### Daily Scan Submissions")
    fig_bar = px.bar(
        time_df, x='date', y='scans_count',
        labels={'date': 'Date', 'scans_count': 'Scans Count'},
        template="plotly_dark"
    )
    fig_bar.update_traces(marker_color='#90CAF9')
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E0F7FA', family='Inter, sans-serif')
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# 2. SEVERITY DISTRIBUTION & CLASS DISTRIBUTION
st.markdown("### 📊 Pollution Profiles & Classes")
col_d1, col_d2 = st.columns(2)

with col_d1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("##### Submissions by Severity Level")
    
    # Value counts
    sev_df = df['severity'].value_counts().reset_index()
    sev_df.columns = ['Severity', 'Count']
    
    # Map colors
    colors = [SEVERITY_COLORS.get(s.lower(), '#90CAF9') for s in sev_df['Severity']]
    
    fig_pie = px.pie(
        sev_df, values='Count', names='Severity',
        color='Severity', color_discrete_map=SEVERITY_COLORS,
        hole=0.4, template="plotly_dark"
    )
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E0F7FA', family='Inter, sans-serif'),
        showlegend=True
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_d2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("##### Total Detected Particle Types")
    
    # Calculate sum of classes
    class_sums = {'fragment': 0, 'fiber': 0, 'pellet': 0, 'film': 0}
    for sub in submissions:
        counts = sub.get('class_counts', {})
        for key in class_sums:
            class_sums[key] += counts.get(key, 0)
            
    class_df = pd.DataFrame(list(class_sums.items()), columns=['Class', 'Total Count'])
    class_df = class_df.sort_values(by='Total Count', ascending=True)
    
    # Class colors mapped to exact specifications
    class_colors_map = {
        'fragment': '#FF5722',  # Orange
        'fiber': '#00B4D8',     # Blue
        'pellet': '#00C853',    # Green
        'film': '#FFC107'       # Amber
    }
    
    colors = [class_colors_map.get(c, '#90CAF9') for c in class_df['Class']]
    
    fig_class = go.Figure(go.Bar(
        x=class_df['Total Count'],
        y=[c.capitalize() for c in class_df['Class']],
        orientation='h',
        marker=dict(color=colors, line=dict(color='#03045E', width=1.5))
    ))
    
    fig_class.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E0F7FA', family='Inter, sans-serif'),
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)')
    )
    st.plotly_chart(fig_class, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# 3. DENSITY HISTOGRAM & LOCATION TABLE
st.markdown("### 🔬 Concentration Distribution & Rankings")
col_b1, col_b2 = st.columns(2)

with col_b1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("##### Concentration Density Distribution (P/L)")
    fig_hist = px.histogram(
        df, x='density_per_liter',
        nbins=20, labels={'density_per_liter': 'Density (Particles / Liter)'},
        template="plotly_dark"
    )
    fig_hist.update_traces(marker_color='#00B4D8', marker_line_color='#023E8A', marker_line_width=1.5)
    fig_hist.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E0F7FA', family='Inter, sans-serif')
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_b2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("##### Location Avg Concentration Ranking")
    
    # Rank by density
    rank_df = df.groupby('location_name')['density_per_liter'].mean().reset_index()
    rank_df.columns = ['River Location', 'Avg Density (P/L)']
    rank_df = rank_df.sort_values(by='Avg Density (P/L)', ascending=False)
    
    st.dataframe(
        rank_df,
        use_container_width=True,
        hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
