---
title: AquaScan
emoji: 🔬
colorFrom: blue
colorTo: cyan
sdk: streamlit
sdk_version: 1.28.0
app_file: app/app.py
pinned: true
license: mit
---

# AquaScan: AI-Powered River Microplastic Pollution Detection

AquaScan is an AI-powered detection and analytics system for mapping microplastic pollution in rivers. Built using Python, YOLOv8, CSRNet, XGBoost, and Streamlit, it provides automatic particle classification, severity mapping, density analysis, spatial heatmaps, and downloadable PDF reports.

## Features

- **Microplastic Count & Classification**: Detects microplastic particles in water images and classifies them into fragments, fibers, pellets, and films.
- **Severity Estimation**: Gauges the severity of pollution (`low`, `medium`, `high`, `critical`) based on density and count characteristics using an XGBoost classifier.
- **Offline SQLite DB & Cloud Supabase Integration**: Seamlessly switches to Supabase when environment variables are supplied; defaults to zero-config SQLite otherwise.
- **Spatial Heatmaps**: Captures GPS inputs and plots a dynamic geographic heatmap using Folium.
- **PDF Reports**: Generates formal PDF compliance reports using FPDF2.
- **Demo Mode fallback**: Automatic, crash-free demo mode if model weights are not loaded.

## Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Start the App**:
   ```bash
   streamlit run app/app.py
   ```
3. **Training & Advanced usage**:
   - Training notebooks are available in `notebooks/`.
   - Configurations are in `configs/`.

---
*Created by AquaScan Research Team, Andhra Pradesh, India | June 2026*
