import os
import random
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any, List
from PIL import Image, ImageDraw, ImageFont

# Import configurations
from src.utils.config import MODEL_PATH

@dataclass
class DetectionResult:
    particle_count: int
    class_counts: Dict[str, int]
    density_per_liter: float
    severity: str
    confidence: float
    annotated_image: Image.Image
    bboxes: List[Dict[str, Any]]
    is_mock: bool

class Detector:
    def __init__(self, model_path: str = None):
        """Initializes the YOLOv8 detector.
        
        If weights are not found, fallback to Mock Mode.
        """
        self.model_path = model_path or MODEL_PATH
        self.mock_mode = True
        self.model = None
        
        print(f"[Detector] Initializing. Target model path: {self.model_path}")
        
        if os.path.exists(self.model_path):
            try:
                from ultralytics import YOLO
                print(f"[Detector] Loading YOLOv8 model from {self.model_path}...")
                self.model = YOLO(self.model_path)
                self.mock_mode = False
                print("[Detector] YOLOv8 model loaded successfully.")
            except Exception as e:
                print(f"[Detector] Error loading YOLOv8 weights: {str(e)}. Falling back to MOCK_MODE = True.")
        else:
            print(f"[Detector] Weights file not found at {self.model_path}. Auto-enabling MOCK_MODE = True.")

        # Class colors defined in the design spec
        self.class_colors = {
            'fragment': '#FF5722',  # Orange
            'fiber': '#00B4D8',     # Blue
            'pellet': '#00C853',    # Green
            'film': '#FFC107'       # Amber
        }

    def detect(self, image: Image.Image, conf_threshold: float = 0.25) -> DetectionResult:
        """Runs object detection on the input image.
        
        Args:
            image (PIL.Image.Image): Input PIL Image.
            conf_threshold (float): Confidence threshold for YOLOv8 inference.
            
        Returns:
            DetectionResult: Detections and statistical outputs.
        """
        print(f"[Detector] Starting detection. Mock Mode active: {self.mock_mode}")
        if self.mock_mode:
            return self._run_mock_detection(image)
        else:
            return self._run_real_detection(image, conf_threshold)

    def _run_real_detection(self, image: Image.Image, conf_threshold: float = 0.25) -> DetectionResult:
        """Inferences using real YOLOv8 weights."""
        try:
            # Make sure image is RGB
            if image.mode != "RGB":
                image = image.convert("RGB")
                
            # Perform prediction
            results = self.model(image, conf=conf_threshold)[0]
            
            bboxes = []
            class_counts = {'fragment': 0, 'fiber': 0, 'pellet': 0, 'film': 0}
            total_conf = 0.0
            
            # Map YOLO class index to name
            names_map = results.names  # dict of class_id: name
            # If names map is empty or different, define standard mapping
            class_names = ['fragment', 'fiber', 'pellet', 'film']
            
            for box in results.boxes:
                coords = box.xyxy[0].tolist() # [x1, y1, x2, y2]
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                
                # Get class name
                raw_cls_name = names_map.get(cls_id, class_names[cls_id % len(class_names)])
                cls_name = raw_cls_name.lower()
                if cls_name not in class_counts:
                    cls_name = class_names[cls_id % len(class_names)]
                    
                class_counts[cls_name] += 1
                total_conf += conf
                
                bboxes.append({
                    'x1': coords[0],
                    'y1': coords[1],
                    'x2': coords[2],
                    'y2': coords[3],
                    'class': cls_name,
                    'conf': conf
                })
                
            particle_count = len(bboxes)
            avg_confidence = total_conf / particle_count if particle_count > 0 else 0.0
            
            # Estimate density: run density estimation logic (particles/liter)
            # Standard density conversion: particle_count * scaling factor (e.g. 15.4)
            density_per_liter = self._estimate_density(particle_count)
            
            # Classify severity
            severity = self._classify_severity(particle_count, density_per_liter)
            
            # Annotate image
            annotated_image = self._annotate_image(image, bboxes)
            
            return DetectionResult(
                particle_count=particle_count,
                class_counts=class_counts,
                density_per_liter=density_per_liter,
                severity=severity,
                confidence=avg_confidence,
                annotated_image=annotated_image,
                bboxes=bboxes,
                is_mock=False
            )
            
        except Exception as e:
            print(f"[Detector] Inference error: {str(e)}. Falling back to mock detection.")
            return self._run_mock_detection(image)

    def _run_mock_detection(self, image: Image.Image) -> DetectionResult:
        """Generates mock detection results for testing/demonstration."""
        width, height = image.size
        
        # 3 to 8 bounding boxes
        particle_count = random.randint(3, 8)
        classes = list(self.class_colors.keys())
        
        bboxes = []
        class_counts = {'fragment': 0, 'fiber': 0, 'pellet': 0, 'film': 0}
        total_conf = 0.0
        
        for _ in range(particle_count):
            cls_name = random.choice(classes)
            class_counts[cls_name] += 1
            
            # Generate random box coordinates
            box_w = random.randint(30, 80)
            box_h = random.randint(30, 80)
            x1 = random.randint(10, width - box_w - 10)
            y1 = random.randint(10, height - box_h - 10)
            x2 = x1 + box_w
            y2 = y1 + box_h
            
            conf = random.uniform(0.72, 0.95)
            total_conf += conf
            
            bboxes.append({
                'x1': float(x1),
                'y1': float(y1),
                'x2': float(x2),
                'y2': float(y2),
                'class': cls_name,
                'conf': conf
            })
            
        avg_confidence = total_conf / particle_count if particle_count > 0 else 0.0
        density_per_liter = random.uniform(5.0, 150.0)
        
        # Classify severity using standard rule-base
        severity = self._classify_severity(particle_count, density_per_liter)
        
        annotated_image = self._annotate_image(image, bboxes)
        
        return DetectionResult(
            particle_count=particle_count,
            class_counts=class_counts,
            density_per_liter=density_per_liter,
            severity=severity,
            confidence=avg_confidence,
            annotated_image=annotated_image,
            bboxes=bboxes,
            is_mock=True
        )

    def _estimate_density(self, count: int) -> float:
        """Simple density scaling: particles per liter."""
        # Simple placeholder formula: count * 1.5 + some base
        return float(count * 12.5 + random.uniform(1.0, 5.0))

    def _classify_severity(self, count: int, density: float) -> str:
        """Classifies severity level based on particle count and density.
        
        Matches the specifications in the classifier unit test requirements.
        """
        # test_low_severity: count<10, density<10 -> low
        # test_medium_severity: count 10-50 -> medium
        # test_high_severity: count 50-100 -> high
        # test_critical_severity: count>100 -> critical
        
        if count < 10 and density < 10:
            return 'low'
        elif count < 10:
            # If count is small, check density
            if density < 50:
                return 'low'
            elif density < 100:
                return 'medium'
            else:
                return 'high'
        elif 10 <= count <= 50:
            return 'medium'
        elif 51 <= count <= 100:
            return 'high'
        else:
            return 'critical'

    def _annotate_image(self, image: Image.Image, bboxes: List[Dict[str, Any]]) -> Image.Image:
        """Draws bounding boxes and labels onto the image."""
        annotated = image.copy()
        draw = ImageDraw.Draw(annotated)
        
        # Attempt to load a default font
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None
            
        for box in bboxes:
            cls_name = box['class']
            color = self.class_colors.get(cls_name, '#00B4D8')
            x1, y1, x2, y2 = box['x1'], box['y1'], box['x2'], box['y2']
            conf = box['conf']
            
            # Draw rectangle
            draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
            
            # Draw text label background
            label = f"{cls_name} {conf:.2f}"
            
            # Calculate text size (draw.textbbox is available in newer Pillow versions)
            try:
                left, top, right, bottom = draw.textbbox((x1, y1 - 15), label, font=font)
                draw.rectangle([left - 2, top - 2, right + 2, bottom + 2], fill=color)
            except AttributeError:
                # Fallback for older Pillow versions
                draw.rectangle([x1, y1 - 15, x1 + 100, y1], fill=color)
                
            # Draw text
            draw.text((x1, y1 - 15), label, fill="#FFFFFF", font=font)
            
        return annotated
