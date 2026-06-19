import pytest
from src.classifier.severity_classifier import SeverityClassifier

def test_low_severity():
    """Test low severity classification: count < 10 and density < 10."""
    classifier = SeverityClassifier()
    
    # Under boundary
    result = classifier.classify(count=5, density_per_liter=5.0, class_counts={})
    assert result == 'low'
    
    # Edge case exactly on boundary (count<10 and density<10)
    result = classifier.classify(count=9, density_per_liter=9.9, class_counts={})
    assert result == 'low'

def test_medium_severity():
    """Test medium severity classification: count 10 to 50."""
    classifier = SeverityClassifier()
    
    # Mid-range
    result = classifier.classify(count=25, density_per_liter=10.0, class_counts={})
    assert result == 'medium'
    
    # Boundaries
    result = classifier.classify(count=10, density_per_liter=15.0, class_counts={})
    assert result == 'medium'
    
    result = classifier.classify(count=50, density_per_liter=150.0, class_counts={})
    assert result == 'medium'

def test_high_severity():
    """Test high severity classification: count 51 to 100."""
    classifier = SeverityClassifier()
    
    # Mid-range
    result = classifier.classify(count=75, density_per_liter=20.0, class_counts={})
    assert result == 'high'
    
    # Boundaries
    result = classifier.classify(count=51, density_per_liter=80.0, class_counts={})
    assert result == 'high'
    
    result = classifier.classify(count=100, density_per_liter=200.0, class_counts={})
    assert result == 'high'

def test_critical_severity():
    """Test critical severity classification: count > 100."""
    classifier = SeverityClassifier()
    
    # Boundary and above
    result = classifier.classify(count=101, density_per_liter=300.0, class_counts={})
    assert result == 'critical'
    
    result = classifier.classify(count=150, density_per_liter=10.0, class_counts={})
    assert result == 'critical'

def test_output_is_string():
    """Test that the return type of classify is always a string."""
    classifier = SeverityClassifier()
    result = classifier.classify(count=0, density_per_liter=0.0, class_counts={})
    
    assert isinstance(result, str)
    assert result in ['low', 'medium', 'high', 'critical']
