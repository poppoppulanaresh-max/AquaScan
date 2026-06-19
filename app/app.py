import sys
import os
from pathlib import Path

# Prevent module shadowing by removing the script's directory from sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
while script_dir in sys.path:
    sys.path.remove(script_dir)
if '' in sys.path:
    sys.path.remove('')

# Add project root directory to sys.path
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st

# Initialize Page Configuration
st.set_page_config(
    page_title="AquaScan - AI River Microplastics Detector",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State Variables
if 'uploaded_image' not in st.session_state:
    st.session_state['uploaded_image'] = None
if 'detection_result' not in st.session_state:
    st.session_state['detection_result'] = None
if 'annotated_image' not in st.session_state:
    st.session_state['annotated_image'] = None
if 'gps_lat' not in st.session_state:
    st.session_state['gps_lat'] = 16.3067 # Default Guntur lat
if 'gps_lon' not in st.session_state:
    st.session_state['gps_lon'] = 80.4365 # Default Guntur lon
if 'submission_id' not in st.session_state:
    st.session_state['submission_id'] = None

# Inject global styles
from app.styles.theme import inject_theme
inject_theme()

# Clean up module shadowing before redirecting to sub-pages
# This deletes the shadowed single-file 'app' module from cache so that
# Python is forced to resolve the 'app' folder as a package on subsequent page imports.
if 'app' in sys.modules and not hasattr(sys.modules['app'], '__path__'):
    del sys.modules['app']

# Automatically redirect the root execution to 1_home.py
try:
    st.switch_page("pages/1_home.py")
except Exception as e:
    # If switch_page fails or is not supported in this version, render a welcome layout
    st.write("### Welcome to AquaScan!")
    st.write("Please select **Home** or **Upload** from the sidebar menu to begin.")
