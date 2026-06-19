import streamlit as st

# Color Palette Definitions
RIVER_BLUE = "#00B4D8"
DEEP_OCEAN = "#023E8A"
SURFACE = "#03045E"
GLASS_CARD = "rgba(0,180,216,0.08)"
TEXT_PRIMARY = "#E0F7FA"
TEXT_SECONDARY = "#90CAF9"
BORDER = "rgba(0,180,216,0.25)"

# Severity Level Colors
SEVERITY_COLORS = {
    'low': '#00C853',       # Green
    'medium': '#FFC107',    # Amber
    'high': '#FF5722',      # Orange
    'critical': '#D50000'   # Red
}

# Injected CSS stylesheet
THEME_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap');

/* Apply primary background gradient */
.stApp {
    background: linear-gradient(135deg, #03045E 0%, #023E8A 50%, #0077B6 100%) !important;
}

/* Headings typography styling */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #E0F7FA !important;
    font-weight: 700 !important;
}

/* Body and UI labels styling */
p, label, span, li {
    font-family: 'Inter', sans-serif;
    color: #E0F7FA;
}

/* Glassmorphism containers */
.glass-card {
    background: rgba(0, 180, 216, 0.08) !important;
    border: 1px solid rgba(0, 180, 216, 0.25) !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
    backdrop-filter: blur(10px) !important;
    margin-bottom: 1rem !important;
}

/* JetBrains Mono typography for scientific metrics */
.metric-value {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    color: #00B4D8 !important;
    margin-top: 5px !important;
}

.metric-label {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    color: #90CAF9 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}

/* Severity badge indicator styling */
.severity-badge {
    display: inline-block !important;
    border-radius: 20px !important;
    padding: 4px 16px !important;
    font-size: 13px !important;
    font-weight: bold !important;
    text-transform: uppercase !important;
    color: #FFFFFF !important;
    text-align: center !important;
    margin-top: 5px !important;
}

/* Water wave float animation */
@keyframes wave {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}

.wave-accent {
    animation: wave 3s ease-in-out infinite;
    display: inline-block;
}

/* Override standard streamlit input cards with glassmorphism tints */
div[data-baseweb="input"] {
    background-color: rgba(2, 62, 138, 0.4) !important;
    border: 1px solid rgba(0, 180, 216, 0.3) !important;
    border-radius: 8px !important;
}

div[data-baseweb="input"] input {
    color: #E0F7FA !important;
    font-family: 'Inter', sans-serif !important;
}

/* Buttons visual enhancements */
.stButton>button {
    background-color: #00B4D8 !important;
    color: #03045E !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.5rem 2rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(0, 180, 216, 0.4) !important;
}

.stButton>button:hover {
    background-color: #E0F7FA !important;
    color: #03045E !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(224, 247, 250, 0.6) !important;
}

.stButton>button:active {
    transform: translateY(0) !important;
}

/* Center and style tabs */
.stTabs [data-baseweb="tab-list"] {
    background-color: rgba(3, 4, 94, 0.6) !important;
    border-radius: 10px !important;
    padding: 5px !important;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #90CAF9 !important;
    font-weight: 500 !important;
}

.stTabs [aria-selected="true"] {
    color: #00B4D8 !important;
    font-weight: 700 !important;
}

/* Markdown formatting defaults */
.stMarkdown p {
    line-height: 1.6 !important;
}

/* Footers and extra clutter suppression */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
"""

def inject_theme():
    """Injects custom CSS styles and loads Google Fonts into the current page."""
    st.markdown(f"<style>{THEME_CSS}</style>", unsafe_allow_html=True)
