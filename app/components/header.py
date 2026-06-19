import streamlit as st
import os
from src.utils.config import MODEL_PATH

def render_header(title: str = "River Intelligence Control Center"):
    """Renders the standard page header.
    
    Checks if YOLOv8 weights exist and displays the yellow warning banner if they are missing.
    
    Args:
        title (str): Header title to display.
    """
    # 1. Determine if running in mock mode based on weights file existence
    weights_exist = os.path.exists(MODEL_PATH)
    is_mock = not weights_exist
    
    # 2. Render Demo Mode Banner at the top of the page if in mock mode
    if is_mock:
        st.markdown(
            """
            <div style="
                background-color: #FFC107;
                color: #03045E;
                padding: 10px 15px;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
                font-family: 'Inter', sans-serif;
                font-size: 14px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            ">
                🔬 Running in Demo Mode — Upload model weights to <code>models/weights/best.pt</code> for real detection
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # 3. Render Title with wave accent
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 25px;">
            <div class="wave-accent" style="font-size: 2.5rem;">🌊</div>
            <div>
                <h1 style="margin: 0; font-size: 2.2rem; font-family: 'Space Grotesk', sans-serif;">{title}</h1>
                <p style="margin: 0; color: #90CAF9; font-size: 0.95rem;">AquaScan Intelligence Hub</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
