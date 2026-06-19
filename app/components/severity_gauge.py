import plotly.graph_objects as go
import streamlit as st
from src.utils.config import SEVERITY_COLORS

def render_severity_gauge(severity: str):
    """Renders a Plotly circular indicator gauge showing pollution severity.
    
    Args:
        severity (str): 'low', 'medium', 'high', or 'critical'.
    """
    sev = severity.lower()
    score_map = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
    score = score_map.get(sev, 1)
    
    color = SEVERITY_COLORS.get(sev, '#00C853')
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {
            'text': f"Severity Status: {severity.upper()}", 
            'font': {'size': 16, 'color': color, 'family': 'Space Grotesk, sans-serif'}
        },
        gauge = {
            'axis': {
                'range': [0.5, 4.5], 
                'tickwidth': 1, 
                'tickcolor': "#90CAF9",
                'tickmode': "array",
                'tickvals': [1, 2, 3, 4],
                'ticktext': ['Low', 'Medium', 'High', 'Critical']
            },
            'bar': {'color': color, 'thickness': 0.45},
            'bgcolor': "rgba(255,255,255,0.05)",
            'borderwidth': 1.5,
            'bordercolor': "rgba(0,180,216,0.3)",
            'steps': [
                {'range': [0.5, 1.5], 'color': 'rgba(0, 200, 83, 0.1)'},
                {'range': [1.5, 2.5], 'color': 'rgba(255, 193, 7, 0.1)'},
                {'range': [2.5, 3.5], 'color': 'rgba(255, 87, 34, 0.1)'},
                {'range': [3.5, 4.5], 'color': 'rgba(213, 0, 0, 0.1)'}
            ]
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E0F7FA', family='Space Grotesk, sans-serif'),
        height=220,
        margin=dict(t=50, b=20, l=20, r=20)
    )
    
    # Hide the numeric score representation, as we only need the gauge labels
    fig.update_traces(number_font_color='rgba(0,0,0,0)')
    
    st.plotly_chart(fig, use_container_width=True)
stream = False
