import plotly.graph_objects as go
import streamlit as st
from typing import Dict

def render_particle_chart(class_counts: Dict[str, int]):
    """Renders a Plotly donut chart representing particle type distributions.
    
    Uses exact theme colors for slices, with a transparent card background.
    
    Args:
        class_counts (dict): Dictionary mapping class names ('fragment', 'fiber', etc.) to count.
    """
    labels = list(class_counts.keys())
    values = list(class_counts.values())
    
    # Class colors mapped to exact specifications
    colors_map = {
        'fragment': '#FF5722',  # Orange
        'fiber': '#00B4D8',     # Blue
        'pellet': '#00C853',    # Green
        'film': '#FFC107'       # Amber
    }
    
    colors = [colors_map.get(l.lower(), '#90CAF9') for l in labels]
    
    # If all values are zero, show a placeholder single-color donut
    if sum(values) == 0:
        labels = ["No Particles"]
        values = [1]
        colors = ["rgba(255,255,255,0.15)"]
        
    fig = go.Figure(data=[go.Pie(
        labels=[l.capitalize() for l in labels],
        values=values,
        hole=.5,
        textinfo='percent+value' if sum(values) > 0 else 'none',
        marker=dict(colors=colors, line=dict(color='#03045E', width=2)),
        hoverinfo='label+value+percent'
    )])
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E0F7FA', family='Inter, sans-serif', size=11),
        showlegend=True,
        margin=dict(t=20, b=20, l=10, r=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(color='#90CAF9')
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
