import streamlit as st
import time
import uuid
from datetime import datetime
from PIL import Image

# Import core modules
from app.styles.theme import inject_theme
from app.components.header import render_header
from src.preprocessing.image_processor import validate_image, preprocess
from src.preprocessing.glare_removal import remove_glare
from src.preprocessing.turbidity_filter import correct_turbidity
from src.detector.detector import Detector
from src.density.density_estimator import DensityEstimator
from src.classifier.severity_classifier import SeverityClassifier
from src.reports.pdf_generator import generate_report

# Apply global styling
inject_theme()

# Render header
render_header("Upload Water Sample Image")

# Initialize models
@st.cache_resource
def load_pipelines():
    detector = Detector()
    density_estimator = DensityEstimator()
    severity_classifier = SeverityClassifier()
    return detector, density_estimator, severity_classifier

detector, density_estimator, severity_classifier = load_pipelines()

# Main Container
st.markdown("### 📤 Upload and Coordinates Input")

col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown(
        """
        <div class="glass-card" style="padding: 1rem !important;">
            <p style="font-size: 0.95rem; margin-bottom: 15px; color: #90CAF9;">
                Select a smartphone photo of the river water surface. Accepted formats: JPG, PNG, WEBP.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed"
    )

with col_right:
    # Location name selection
    location_river = st.selectbox(
        "📍 Target River / Location",
        ["Krishna River", "Godavari River", "Musi River", "Other Location"]
    )
    
    if location_river == "Other Location":
        custom_location = st.text_input("Enter custom location name", placeholder="e.g. Pennar River, AP")
        final_location = custom_location if custom_location else "Other River"
    else:
        final_location = location_river

    # Coordinate fields
    st.markdown("##### Geolocation Coords (Optional)")
    gps_enabled = st.checkbox("Attach GPS Location coordinates", value=True)
    
    if gps_enabled:
        lat_col, lon_col = st.columns(2)
        with lat_col:
            gps_lat = st.number_input(
                "Latitude", 
                value=16.3067, 
                format="%.6f",
                help="📍 Find coordinates on Google Maps -> Right-click location -> 'What's here?'"
            )
        with lon_col:
            gps_lon = st.number_input(
                "Longitude", 
                value=80.4365, 
                format="%.6f",
                help="📍 Find coordinates on Google Maps -> Right-click location -> 'What's here?'"
            )
    else:
        gps_lat, gps_lon = None, None

# Advanced Processing Settings
with st.expander("🛠️ Advanced Preprocessing & Detection Options"):
    apply_glare = st.checkbox("Remove Sun Glare (Inpaint Highlights)", value=True)
    apply_turbidity = st.checkbox("Turbidity Color Balancing (De-murk)", value=True)
    conf_val = st.slider("🔍 YOLOv8 Detector Confidence Threshold", min_value=0.05, max_value=1.00, value=0.25, step=0.05, help="Lower values increase sensitivity (find more tiny objects but might introduce noise/false detections), while higher values filter out lower confidence predictions.")

# Image Preview and Execution
if uploaded_file is not None:
    try:
        # Load image
        img = Image.open(uploaded_file)
        
        # Validate Image
        is_valid, err_msg = validate_image(img)
        if not is_valid:
            st.error(f"❌ Validation Failed: {err_msg}")
        else:
            # Display image metadata and preview
            st.markdown("### 🖼️ Uploaded Sample Preview")
            
            with st.container():
                st.markdown(
                    f"""
                    <div class="glass-card">
                        <p style="margin: 0; font-size: 0.9rem; color: #90CAF9;">
                            <b>Filename:</b> {uploaded_file.name} | <b>Dimensions:</b> {img.size[0]}x{img.size[1]} pixels
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Show preview image
                st.image(img, use_container_width=True)
                
            # Analyze Button
            if st.button("🔬 ANALYZE FOR MICROPLASTICS", use_container_width=True):
                # 1. Progress indicators
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Step 1: Preprocessing
                status_text.text("Preprocessing image (CLAHE, Denoising)...")
                progress_bar.progress(10)
                
                prepped_img = preprocess(img)
                progress_bar.progress(20)
                
                if apply_glare:
                    status_text.text("Applying glare removal filters...")
                    prepped_img = remove_glare(prepped_img)
                    progress_bar.progress(25)
                    
                if apply_turbidity:
                    status_text.text("Correcting turbidity color casts...")
                    prepped_img = correct_turbidity(prepped_img)
                    progress_bar.progress(30)
                
                # Step 2: Particle detection
                status_text.text("Running YOLOv8 microplastic particle detection...")
                progress_bar.progress(50)
                
                det_result = detector.detect(prepped_img, conf_threshold=conf_val)
                progress_bar.progress(70)
                
                # Step 3: Density estimation
                status_text.text("Estimating spatial concentration density maps...")
                progress_bar.progress(75)
                
                # Run density model
                density_map, density_val = density_estimator.estimate_density(prepped_img, det_result.particle_count)
                # Update detector density with the one from density estimator
                det_result.density_per_liter = density_val
                progress_bar.progress(85)
                
                # Step 4: Severity classification
                status_text.text("Running XGBoost severity classifier...")
                progress_bar.progress(90)
                
                severity = severity_classifier.classify(
                    det_result.particle_count,
                    det_result.density_per_liter,
                    det_result.class_counts
                )
                det_result.severity = severity
                progress_bar.progress(95)
                
                # Step 5: Report generation
                status_text.text("Generating environmental PDF report...")
                
                # Convert results to standard dict for saving/report
                result_payload = {
                    'id': str(uuid.uuid4()),
                    'timestamp': datetime.utcnow().isoformat(),
                    'particle_count': det_result.particle_count,
                    'class_counts': det_result.class_counts,
                    'density_per_liter': det_result.density_per_liter,
                    'severity': det_result.severity,
                    'confidence': det_result.confidence,
                    'gps_lat': gps_lat,
                    'gps_lon': gps_lon,
                    'location_name': final_location,
                    'is_mock': det_result.is_mock
                }
                
                pdf_bytes = generate_report(
                    det_result, 
                    img, 
                    det_result.annotated_image, 
                    gps_lat, 
                    gps_lon, 
                    final_location
                )
                
                progress_bar.progress(100)
                status_text.success("Pipeline executed successfully!")
                
                # Save variables to Session State
                st.session_state['uploaded_image'] = img
                st.session_state['detection_result'] = result_payload
                st.session_state['annotated_image'] = det_result.annotated_image
                st.session_state['gps_lat'] = gps_lat
                st.session_state['gps_lon'] = gps_lon
                st.session_state['pdf_report_bytes'] = pdf_bytes
                st.session_state['submission_id'] = None # Reset submission ID until user saves to database
                
                # 6. Quick results preview
                st.markdown("### 📊 Analysis Quick Summary")
                q_col1, q_col2, q_col3 = st.columns(3)
                
                with q_col1:
                    st.markdown(
                        f"""
                        <div class="glass-card" style="text-align: center;">
                            <div class="metric-label">Detected Particles</div>
                            <div class="metric-value">{det_result.particle_count}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with q_col2:
                    color = '#00C853'
                    if severity == 'medium': color = '#FFC107'
                    elif severity == 'high': color = '#FF5722'
                    elif severity == 'critical': color = '#D50000'
                    
                    st.markdown(
                        f"""
                        <div class="glass-card" style="text-align: center;">
                            <div class="metric-label">Severity Level</div>
                            <div class="severity-badge" style="background-color: {color}; margin-top: 15px;">
                                {severity.upper()}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with q_col3:
                    st.markdown(
                        f"""
                        <div class="glass-card" style="text-align: center;">
                            <div class="metric-label">Density (particles/L)</div>
                            <div class="metric-value">{det_result.density_per_liter:.2f}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                st.markdown("<br/>", unsafe_allow_html=True)
                if st.button("👉 VIEW FULL DETAILED RESULTS", use_container_width=True):
                    st.switch_page("pages/3_results.py")
                    
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        st.exception(e)
else:
    st.info("💡 Please upload a water sample image to begin the microplastics analysis.")
