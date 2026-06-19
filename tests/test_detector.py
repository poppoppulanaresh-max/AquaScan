import pytest
from PIL import Image
from src.detector.detector import Detector, DetectionResult

def test_mock_mode_no_crash():
    """Test that the detector initializes and runs in mock mode without crashing."""
    detector = Detector(model_path="non_existent_weights.pt")
    assert detector.mock_mode is True
    
    # Generate dummy image
    img = Image.new("RGB", (300, 300), color="blue")
    
    try:
        result = detector.detect(img)
    except Exception as e:
        pytest.fail(f"Detector crashed with exception: {str(e)}")

def test_mock_mode_returns_result():
    """Test that the mock detector returns a valid DetectionResult object."""
    detector = Detector(model_path="non_existent_weights.pt")
    img = Image.new("RGB", (300, 300), color="blue")
    result = detector.detect(img)
    
    assert isinstance(result, DetectionResult)
    assert result.is_mock is True

def test_mock_result_structure():
    """Test that DetectionResult properties match the expected types and values."""
    detector = Detector(model_path="non_existent_weights.pt")
    img = Image.new("RGB", (300, 300), color="blue")
    result = detector.detect(img)
    
    assert isinstance(result.particle_count, int)
    assert isinstance(result.class_counts, dict)
    assert isinstance(result.density_per_liter, float)
    assert isinstance(result.severity, str)
    assert isinstance(result.confidence, float)
    assert isinstance(result.bboxes, list)
    
    # Check bounds
    assert 3 <= result.particle_count <= 8
    assert 0.72 <= result.confidence <= 0.95
    assert 5.0 <= result.density_per_liter <= 150.0
    assert result.severity in ['low', 'medium', 'high', 'critical']

def test_class_counts_sum():
    """Test that the sum of counts per class equals the total particle count."""
    detector = Detector(model_path="non_existent_weights.pt")
    img = Image.new("RGB", (300, 300), color="blue")
    result = detector.detect(img)
    
    total_class_sum = sum(result.class_counts.values())
    assert total_class_sum == result.particle_count

def test_annotated_image_is_pil():
    """Test that the output annotated image is a PIL Image object."""
    detector = Detector(model_path="non_existent_weights.pt")
    img = Image.new("RGB", (300, 300), color="blue")
    result = detector.detect(img)
    
    assert isinstance(result.annotated_image, Image.Image)
    assert result.annotated_image.size == img.size
