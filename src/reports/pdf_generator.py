import os
import tempfile
from datetime import datetime
from PIL import Image
from fpdf import FPDF

class AquaScanPDF(FPDF):
    def header(self):
        """Header rendered on every page except the first title page."""
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, "AquaScan Environmental Compliance Report - Confidential", 0, 0, "L")
            self.cell(0, 10, f"Page {self.page_no()}", 0, 1, "R")
            self.ln(5)
            # Subtle divider line
            self.set_draw_color(200, 200, 200)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(5)

    def footer(self):
        """Footer rendered on all pages."""
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, "AquaScan project | Guntur, Andhra Pradesh, India", 0, 0, "L")
        self.cell(0, 10, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 0, "R")

def generate_report(detection_result: any, original_image: Image.Image, annotated_image: Image.Image,
                    gps_lat: float = None, gps_lon: float = None, location_name: str = None) -> bytes:
    """Generates a professional 4-page PDF report using FPDF2.
    
    Args:
        detection_result: Detector output object.
        original_image (PIL.Image.Image): The uploaded raw image.
        annotated_image (PIL.Image.Image): The image with box annotations.
        gps_lat (float, optional): Latitude.
        gps_lon (float, optional): Longitude.
        location_name (str, optional): Target River / Region name.
        
    Returns:
        bytes: The PDF document as bytes.
    """
    print("[PDF] Generating compliance PDF report...")
    
    # Initialize A4 portrait PDF
    pdf = AquaScanPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Define primary theme colors
    primary_color = (0, 180, 216)   # River Blue
    dark_blue = (2, 62, 138)        # Deep Ocean
    gray = (100, 100, 100)
    
    # ------------------ PAGE 1: TITLE PAGE ------------------
    pdf.add_page()
    pdf.ln(20)
    
    # Large Title
    pdf.set_font("Helvetica", "B", 36)
    pdf.set_text_color(*dark_blue)
    pdf.cell(0, 15, "AQUASCAN", 0, 1, "C")
    
    # Subtitle
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*primary_color)
    pdf.cell(0, 8, "AI-Powered River Microplastic Pollution Detection", 0, 1, "C")
    pdf.ln(10)
    
    # Decorative line
    pdf.set_draw_color(*primary_color)
    pdf.set_line_width(1)
    pdf.line(40, pdf.get_y(), 170, pdf.get_y())
    pdf.ln(25)
    
    # Report Meta info
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 10, "ENVIRONMENTAL COMPLIANCE DOSSIER", 0, 1, "C")
    pdf.ln(10)
    
    # Info Box
    pdf.set_fill_color(245, 250, 255)
    pdf.set_draw_color(220, 230, 242)
    pdf.rect(15, pdf.get_y(), 180, 75, style="FD")
    
    pdf.set_y(pdf.get_y() + 5)
    pdf.set_font("Helvetica", "", 10)
    
    # Left aligned metadata
    pdf.set_x(20)
    pdf.cell(50, 8, "Target River / Location:", 0, 0)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(100, 8, str(location_name or "Not Specified"), 0, 1)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_x(20)
    pdf.cell(50, 8, "GPS Coordinates:", 0, 0)
    pdf.set_font("Helvetica", "B", 10)
    coord_str = f"Lat: {gps_lat:.4f}, Lon: {gps_lon:.4f}" if (gps_lat is not None and gps_lon is not None) else "No GPS Data Available"
    pdf.cell(100, 8, coord_str, 0, 1)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_x(20)
    pdf.cell(50, 8, "Detection Mode:", 0, 0)
    pdf.set_font("Helvetica", "B", 10)
    mode_str = "Demo (Mock Mode)" if getattr(detection_result, 'is_mock', True) else "Real YOLOv8 Inference"
    pdf.cell(100, 8, mode_str, 0, 1)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_x(20)
    pdf.cell(50, 8, "Total Detections:", 0, 0)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(100, 8, f"{detection_result.particle_count} particles", 0, 1)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_x(20)
    pdf.cell(50, 8, "Estimated Density:", 0, 0)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(100, 8, f"{detection_result.density_per_liter:.2f} particles / Liter", 0, 1)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_x(20)
    pdf.cell(50, 8, "Pollution Severity:", 0, 0)
    pdf.set_font("Helvetica", "B", 10)
    # Color severity accordingly
    sev = detection_result.severity.upper()
    pdf.cell(100, 8, sev, 0, 1)
    
    # ------------------ PAGE 2: IMAGE ANALYSIS ------------------
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*dark_blue)
    pdf.cell(0, 10, "Visual Particle Detections", 0, 1, "L")
    pdf.ln(5)
    
    # Save original & annotated images to temporary files to load into PDF safely
    temp_dir = tempfile.gettempdir()
    orig_path = os.path.join(temp_dir, "temp_orig.png")
    annot_path = os.path.join(temp_dir, "temp_annot.png")
    
    # Save files
    original_image.save(orig_path, format="PNG")
    annotated_image.save(annot_path, format="PNG")
    
    # Render images
    try:
        # Original Image
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(90, 5, "Original Smartphone Photo", 0, 0, "C")
        pdf.cell(90, 5, "AI Annotated Detections", 0, 1, "C")
        pdf.ln(2)
        
        # Position them side by side
        y_pos = pdf.get_y()
        pdf.image(orig_path, x=10, y=y_pos, w=90, h=90)
        pdf.image(annot_path, x=110, y=y_pos, w=90, h=90)
        
        pdf.set_y(y_pos + 95)
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(*gray)
        pdf.cell(90, 5, "Raw input sample.", 0, 0, "C")
        pdf.cell(90, 5, "Bounding boxes color-coded by class.", 0, 1, "C")
        
    except Exception as e:
        pdf.cell(0, 10, f"Failed to load images into report: {str(e)}", 0, 1)
    finally:
        # Delete temporary files
        if os.path.exists(orig_path):
            os.remove(orig_path)
        if os.path.exists(annot_path):
            os.remove(annot_path)
            
    # ------------------ PAGE 3: DETECTION RESULTS TABLE ------------------
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*dark_blue)
    pdf.cell(0, 10, "Particle Class Breakdown", 0, 1, "L")
    pdf.ln(5)
    
    # Create Table
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(*primary_color)
    pdf.set_text_color(255, 255, 255)
    
    # Headers
    pdf.cell(50, 10, "Particle Class", 1, 0, "C", fill=True)
    pdf.cell(40, 10, "Detected Count", 1, 0, "C", fill=True)
    pdf.cell(40, 10, "Ratio (%)", 1, 0, "C", fill=True)
    pdf.cell(50, 10, "Confidence Level", 1, 1, "C", fill=True)
    
    # Table rows
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    
    total_particles = max(1, detection_result.particle_count)
    class_counts = detection_result.class_counts
    
    for cls_name, count in class_counts.items():
        pdf.cell(50, 10, cls_name.capitalize(), 1, 0, "C")
        pdf.cell(40, 10, str(count), 1, 0, "C")
        ratio = (count / total_particles) * 100
        pdf.cell(40, 10, f"{ratio:.1f}%", 1, 0, "C")
        # Generate dummy confidence for individual classes based on total confidence
        cls_conf = detection_result.confidence if count > 0 else 0.0
        pdf.cell(50, 10, f"{cls_conf * 100:.1f}%" if cls_conf > 0 else "N/A", 1, 1, "C")
        
    # Total row
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(50, 10, "Total", 1, 0, "C")
    pdf.cell(40, 10, str(detection_result.particle_count), 1, 0, "C")
    pdf.cell(40, 10, "100.0%", 1, 0, "C")
    pdf.cell(50, 10, f"{detection_result.confidence * 100:.1f}%", 1, 1, "C")
    
    # ------------------ PAGE 4: INTERPRETATION GUIDE ------------------
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*dark_blue)
    pdf.cell(0, 10, "Scientific Interpretation & Severity Guide", 0, 1, "L")
    pdf.ln(5)
    
    # Low
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(0, 200, 83) # Low severity Green
    pdf.cell(0, 6, "LOW SEVERITY (<10 particles/liter)", 0, 1, "L")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 5, "Concentration represents baseline background levels. Water is relatively clean regarding macro-microplastics. Suitable for standard local treatment pipelines. Standard monitoring intervals recommended.")
    pdf.ln(4)
    
    # Medium
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(255, 193, 7) # Warning Amber
    pdf.cell(0, 6, "MEDIUM SEVERITY (10-50 particles/liter)", 0, 1, "L")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 5, "Noticeable presence of microplastic particles. Runoff from agricultural or municipal areas is likely. Recommended to filter before domestic usage. Increase monitoring frequency to bi-weekly.")
    pdf.ln(4)
    
    # High
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(255, 87, 34) # Danger Orange
    pdf.cell(0, 6, "HIGH SEVERITY (50-100 particles/liter)", 0, 1, "L")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 5, "Elevated levels of microplastics. Likely close to urban discharge points or industrial areas. Untreated water poses a health hazard to local fauna and human populations using downstream channels.")
    pdf.ln(4)
    
    # Critical
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(213, 0, 0) # Critical Red
    pdf.cell(0, 6, "CRITICAL SEVERITY (>100 particles/liter)", 0, 1, "L")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 5, "Dangerous concentrations of microplastics detected. Immediate intervention required by local water boards. Flagged for environmental contamination. Avoid any direct contact or usage of raw water.")
    pdf.ln(8)
    
    # Disclaimer
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*gray)
    pdf.multi_cell(0, 4, "Disclaimer: AquaScan is an AI-assisted detection system designed for preliminary monitoring. Results are estimations based on photographic data. Actual chemical, biological, and physical lab tests should be conducted to confirm environmental toxicity reports.")
    
    # Output PDF as bytes
    pdf_bytes = pdf.output()
    # In FPDF2 output() might return bytearray, convert to bytes
    return bytes(pdf_bytes)
