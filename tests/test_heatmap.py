import pytest
import folium
from src.heatmap.map_generator import generate_heatmap

def test_empty_submissions():
    """Test that empty submissions list generates a default map without raising errors."""
    try:
        m = generate_heatmap([])
        assert isinstance(m, folium.Map)
    except Exception as e:
        pytest.fail(f"Empty submissions map generation crashed: {str(e)}")

def test_with_submissions():
    """Test map generation with a list of submissions containing valid GPS coordinates."""
    submissions = [
        {
            'id': 'sub-1',
            'timestamp': '2026-06-17T18:00:00.000',
            'particle_count': 5,
            'class_counts': {'fragment': 2, 'fiber': 1, 'pellet': 1, 'film': 1},
            'density_per_liter': 50.0,
            'severity': 'medium',
            'confidence': 0.85,
            'gps_lat': 16.3067,
            'gps_lon': 80.4365,
            'location_name': 'Krishna River',
            'is_mock': True
        },
        {
            'id': 'sub-2',
            'timestamp': '2026-06-17T18:10:00.000',
            'particle_count': 12,
            'class_counts': {'fragment': 6, 'fiber': 2, 'pellet': 2, 'film': 2},
            'density_per_liter': 110.0,
            'severity': 'high',
            'confidence': 0.82,
            'gps_lat': 16.5089,
            'gps_lon': 80.6412,
            'location_name': 'Godavari River',
            'is_mock': True
        }
    ]
    
    try:
        m = generate_heatmap(submissions)
        assert isinstance(m, folium.Map)
    except Exception as e:
        pytest.fail(f"Map generation with submissions crashed: {str(e)}")

def test_returns_folium_map():
    """Test that the return type of generate_heatmap is always a folium.Map."""
    m = generate_heatmap([])
    assert isinstance(m, folium.Map)

def test_filter_by_severity():
    """Test filtering submissions logic is compatible with the map data parameters."""
    submissions = [
        {
            'gps_lat': 16.30, 'gps_lon': 80.43, 'severity': 'low', 'density_per_liter': 5.0
        },
        {
            'gps_lat': 16.50, 'gps_lon': 80.64, 'severity': 'critical', 'density_per_liter': 120.0
        }
    ]
    
    # Filter for critical severity only
    filtered_subs = [s for s in submissions if s['severity'] == 'critical']
    
    assert len(filtered_subs) == 1
    assert filtered_subs[0]['gps_lat'] == 16.50
    
    # Map renders successfully with filtered subset
    m = generate_heatmap(filtered_subs)
    assert isinstance(m, folium.Map)
