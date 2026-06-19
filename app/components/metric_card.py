import streamlit as st

def render_metric_card(label: str, value: str, icon: str = ""):
    """Renders a reusable, highly-styled glassmorphism metric card.
    
    Args:
        label (str): The label of the metric.
        value (str): The value/score to display.
        icon (str, optional): Emoji icon.
    """
    st.markdown(
        f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <div class="metric-label">{label}</div>
                <div style="font-size: 1.3rem; opacity: 0.8;">{icon}</div>
            </div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
