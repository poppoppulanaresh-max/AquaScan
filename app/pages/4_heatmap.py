import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
from streamlit_folium import st_folium

# Import styling & helpers
from app.styles.theme import inject_theme
from app.components.header import render_header
from app.components.metric_card import render_metric_card
from src.database.repository import Repository
from src.heatmap.map_generator import generate_heatmap
from src.heatmap.statistics import calculate_spatial_stats
from src.utils.config import SEVERITY_COLORS

# Apply styles
inject_theme()

# Page title
render_header("Global Pollution Heatmap")

# Load submissions from DB
try:
    repo = Repository()
    all_gps_submissions = repo.get_submissions_with_gps()
except Exception as e:
    print(f"[Heatmap Page] DB loading error: {str(e)}")
    all_gps_submissions = []

# Guard against empty database
if not all_gps_submissions:
    st.markdown(
        """
        <div class="glass-card" style="text-align: center; padding: 3rem !important;">
            <div style="font-size: 3rem; margin-bottom: 20px;">🗺️</div>
            <h3>No GPS Spatial Data Available</h3>
            <p style="color: #90CAF9; margin-bottom: 25px;">
                There are currently no scans logged in the database that contain GPS coordinates. 
                Please upload an image, ensure "Attach GPS Location coordinates" is enabled, and save the result to the database.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("🔌 GO TO UPLOAD PAGE", use_container_width=True):
        st.switch_page("pages/2_upload.py")
    st.stop()

# Convert submissions list to DataFrame for easier filtering
df = pd.DataFrame(all_gps_submissions)
df['date_obj'] = df['timestamp'].apply(lambda x: datetime.fromisoformat(x).date() if x else date.today())

# 1. FILTER SIDEBAR
st.sidebar.markdown("### 🔍 Filter Coordinates")

# Date range filter
min_date = df['date_obj'].min()
max_date = df['date_obj'].max()
if min_date == max_date:
    min_date = min_date - pd.Timedelta(days=1)
    
date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Severity multi-select
severity_filter = st.sidebar.multiselect(
    "Severity Level",
    options=['low', 'medium', 'high', 'critical'],
    default=['low', 'medium', 'high', 'critical']
)

# Minimum density slider
min_density = st.sidebar.slider(
    "Minimum Density (P/L)",
    min_value=0.0,
    max_value=float(df['density_per_liter'].max() or 200.0),
    value=0.0,
    step=1.0
)

# Apply Filters
filtered_df = df[
    (df['severity'].str.lower().isin([s.lower() for s in severity_filter])) &
    (df['density_per_liter'] >= min_density)
]

# Apply date range filter safely (handles single date selection during picker changes)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[(filtered_df['date_obj'] >= start_date) & (filtered_df['date_obj'] <= end_date)]

# Convert back to list of dicts for generators
filtered_submissions = filtered_df.to_dict(orient='records')

# 2. STATS ROW
st.markdown("### 📈 Filtered Spatial Metrics")
spatial_stats = calculate_spatial_stats(filtered_submissions)

s_col1, s_col2, s_col3, s_col4 = st.columns(4)
with s_col1:
    render_metric_card("Mapped Scans", f"{spatial_stats['total_points']}", "📍")
with s_col2:
    render_metric_card("Most Polluted Area", f"{spatial_stats['most_polluted_river']}", "🚨")
with s_col3:
    render_metric_card("Cleanest Area", f"{spatial_stats['cleanest_area']}", "🌱")
with s_col4:
    render_metric_card("Critical Zones", f"{spatial_stats['critical_zones']}", "🔥")

st.markdown("<br/>", unsafe_allow_html=True)

# 3. FOLIUM MAP
st.markdown("### 🗺️ Geographic Pollution Map")
st.markdown(
    """
    <div class="glass-card" style="padding: 0.5rem !important; margin-bottom: 2rem;">
    """,
    unsafe_allow_html=True
)

# Generate Folium map
m = generate_heatmap(filtered_submissions)

# Render map using streamlit-folium
st_folium(m, height=600, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# 4. RECENT SUBMISSIONS TABLE
st.markdown("### 📋 Recent Logged Mapped Data")

if not filtered_submissions:
    st.info("No logs match the current filters.")
else:
    # Display clean table
    display_df = filtered_df[['timestamp', 'location_name', 'particle_count', 'density_per_liter', 'severity', 'confidence', 'is_mock']].copy()
    display_df['timestamp'] = display_df['timestamp'].apply(lambda x: x[:16].replace('T', ' '))
    display_df.rename(columns={
        'timestamp': 'Timestamp',
        'location_name': 'River Location',
        'particle_count': 'Particles Count',
        'density_per_liter': 'Density (P/L)',
        'severity': 'Severity Level',
        'confidence': 'Confidence Score',
        'is_mock': 'Is Demo Run'
    }, inplace=True)
    
    st.dataframe(
        display_df.head(10),
        use_container_width=True,
        hide_index=True
    )

st.markdown("<br/>", unsafe_allow_html=True)

# 5. RIVER DENSITY COMPARISON
st.markdown("### 📊 Pollution Concentrations across Locations")

if not filtered_submissions:
    st.info("No location comparison charts to render.")
else:
    # Group by location and get avg density
    compare_df = filtered_df.groupby('location_name')['density_per_liter'].mean().reset_index()
    compare_df.rename(columns={'location_name': 'Location / River', 'density_per_liter': 'Avg Density (P/L)'}, inplace=True)
    compare_df = compare_df.sort_values(by='Avg Density (P/L)', ascending=False)
    
    # Plotly bar chart
    fig = px.bar(
        compare_df,
        x='Avg Density (P/L)',
        y='Location / River',
        orientation='h',
        color='Avg Density (P/L)',
        color_continuous_scale=['#00C853', '#FFC107', '#FF5722', '#D50000'],
        labels={'Avg Density (P/L)': 'Average Particles per Liter'},
        template="plotly_dark"
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E0F7FA', family='Inter, sans-serif'),
        margin=dict(t=10, b=10, l=10, r=10),
        coloraxis_showscale=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
