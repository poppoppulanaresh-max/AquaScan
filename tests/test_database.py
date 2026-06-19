import os
import tempfile
import pytest
from src.database.sqlite_client import SQLiteClient

@pytest.fixture
def temp_db():
    """Fixture to create and clean up a temporary SQLite database."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    
    client = SQLiteClient(db_path=path)
    yield client
    
    # Cleanup file
    if os.path.exists(path):
        os.remove(path)

def test_save_submission(temp_db):
    """Test saving a detection record return ID string."""
    payload = {
        'id': 'test-uuid-1',
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
    }
    
    saved_id = temp_db.save_submission(payload)
    assert saved_id == 'test-uuid-1'

def test_get_all_submissions(temp_db):
    """Test retrieving records and count increase validation."""
    initial_list = temp_db.get_all_submissions()
    assert len(initial_list) == 0
    
    payload = {
        'id': 'test-uuid-1',
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
    }
    
    temp_db.save_submission(payload)
    
    updated_list = temp_db.get_all_submissions()
    assert len(updated_list) == 1
    assert updated_list[0]['id'] == 'test-uuid-1'

def test_get_submissions_with_gps(temp_db):
    """Test that GPS query only returns submissions with valid coordinates."""
    # Submission with GPS
    payload_gps = {
        'id': 'test-gps-yes',
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
    }
    
    # Submission without GPS
    payload_no_gps = {
        'id': 'test-gps-no',
        'timestamp': '2026-06-17T18:05:00.000',
        'particle_count': 2,
        'class_counts': {'fragment': 1, 'fiber': 1, 'pellet': 0, 'film': 0},
        'density_per_liter': 20.0,
        'severity': 'low',
        'confidence': 0.90,
        'gps_lat': None,
        'gps_lon': None,
        'location_name': None,
        'is_mock': True
    }
    
    temp_db.save_submission(payload_gps)
    temp_db.save_submission(payload_no_gps)
    
    gps_only = temp_db.get_submissions_with_gps()
    assert len(gps_only) == 1
    assert gps_only[0]['id'] == 'test-gps-yes'

def test_get_statistics(temp_db):
    """Test that statistics returns the correct keys and sums."""
    payload1 = {
        'id': 'test-1',
        'timestamp': '2026-06-17T18:00:00.000',
        'particle_count': 4,
        'class_counts': {'fragment': 2, 'fiber': 2, 'pellet': 0, 'film': 0},
        'density_per_liter': 10.0,
        'severity': 'low',
        'confidence': 0.80,
        'gps_lat': 16.30,
        'gps_lon': 80.43,
        'location_name': 'Krishna River',
        'is_mock': True
    }
    
    payload2 = {
        'id': 'test-2',
        'timestamp': '2026-06-17T18:05:00.000',
        'particle_count': 110,
        'class_counts': {'fragment': 50, 'fiber': 30, 'pellet': 20, 'film': 10},
        'density_per_liter': 120.0,
        'severity': 'critical',
        'confidence': 0.90,
        'gps_lat': 16.50,
        'gps_lon': 80.64,
        'location_name': 'Godavari River',
        'is_mock': True
    }
    
    temp_db.save_submission(payload1)
    temp_db.save_submission(payload2)
    
    stats = temp_db.get_statistics()
    
    assert stats['total_scans'] == 2
    assert stats['rivers_monitored'] == 2
    assert stats['avg_density'] == 65.0
    assert stats['critical_alerts'] == 1
    assert stats['by_severity']['low'] == 1
    assert stats['by_severity']['critical'] == 1
    assert stats['by_class']['fragment'] == 52
    assert stats['by_class']['fiber'] == 32
    assert stats['by_class']['pellet'] == 20
    assert stats['by_class']['film'] == 10

def test_delete_submission(temp_db):
    """Test that a record is deleted and cannot be found."""
    payload = {
        'id': 'test-delete',
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
    }
    
    temp_db.save_submission(payload)
    assert len(temp_db.get_all_submissions()) == 1
    
    # Run delete
    status = temp_db.delete_submission('test-delete')
    assert status is True
    assert len(temp_db.get_all_submissions()) == 0
