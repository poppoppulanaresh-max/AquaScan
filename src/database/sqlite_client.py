import sqlite3
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from src.utils.config import SQLITE_DB_PATH

class SQLiteClient:
    def __init__(self, db_path: str = None):
        """Initializes the SQLite client and creates tables if they do not exist.
        
        Args:
            db_path (str): File path for SQLite database.
        """
        self.db_path = db_path or SQLITE_DB_PATH
        
        # Ensure data directory exists
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
            
        print(f"[SQLite] Initializing database at {self.db_path}...")
        self._create_table()

    def _get_connection(self) -> sqlite3.Connection:
        """Returns a sqlite3 connection with row factory enabled."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _execute(self, query: str, params: Any = None, fetch_all: bool = False, fetch_one: bool = False, commit: bool = False) -> Any:
        """Helper to open connection, execute query, commit if needed, and guarantee close."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            if params is not None:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            if commit:
                conn.commit()
                
            if fetch_all:
                return cursor.fetchall()
            elif fetch_one:
                return cursor.fetchone()
            return cursor
        finally:
            conn.close()

    def _create_table(self):
        """Creates the submissions table if it does not exist."""
        query = """
        CREATE TABLE IF NOT EXISTS submissions (
            id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            particle_count INTEGER NOT NULL,
            fragment_count INTEGER NOT NULL,
            fiber_count INTEGER NOT NULL,
            pellet_count INTEGER NOT NULL,
            film_count INTEGER NOT NULL,
            density_per_liter REAL NOT NULL,
            severity TEXT NOT NULL,
            confidence REAL NOT NULL,
            gps_lat REAL,
            gps_lon REAL,
            location_name TEXT,
            is_mock INTEGER NOT NULL
        );
        """
        try:
            self._execute(query, commit=True)
            print("[SQLite] Database schema verified/created successfully.")
        except Exception as e:
            print(f"[SQLite] Error creating schema: {str(e)}")

    def save_submission(self, data: Dict[str, Any]) -> str:
        """Saves a detection submission to the SQLite database.
        
        Args:
            data (dict): Dictionary containing all fields matching the schema.
            
        Returns:
            str: The ID of the saved submission.
        """
        print(f"[SQLite] Saving submission {data.get('id')}...")
        query = """
        INSERT INTO submissions (
            id, timestamp, particle_count, fragment_count, fiber_count,
            pellet_count, film_count, density_per_liter, severity,
            confidence, gps_lat, gps_lon, location_name, is_mock
        ) VALUES (
            :id, :timestamp, :particle_count, :fragment_count, :fiber_count,
            :pellet_count, :film_count, :density_per_liter, :severity,
            :confidence, :gps_lat, :gps_lon, :location_name, :is_mock
        );
        """
        
        # Parse data to match schema names
        class_counts = data.get('class_counts', {})
        insert_data = {
            'id': data.get('id'),
            'timestamp': data.get('timestamp') or datetime.utcnow().isoformat(),
            'particle_count': data.get('particle_count', 0),
            'fragment_count': class_counts.get('fragment', 0),
            'fiber_count': class_counts.get('fiber', 0),
            'pellet_count': class_counts.get('pellet', 0),
            'film_count': class_counts.get('film', 0),
            'density_per_liter': data.get('density_per_liter', 0.0),
            'severity': data.get('severity', 'low'),
            'confidence': data.get('confidence', 0.0),
            'gps_lat': data.get('gps_lat'),
            'gps_lon': data.get('gps_lon'),
            'location_name': data.get('location_name'),
            'is_mock': 1 if data.get('is_mock') else 0
        }
        
        try:
            self._execute(query, insert_data, commit=True)
            print("[SQLite] Submission saved successfully.")
            return insert_data['id']
        except Exception as e:
            print(f"[SQLite] Error saving submission: {str(e)}")
            raise e

    def get_all_submissions(self) -> List[Dict[str, Any]]:
        """Retrieves all submissions from the database, sorted by timestamp descending."""
        query = "SELECT * FROM submissions ORDER BY timestamp DESC;"
        try:
            rows = self._execute(query, fetch_all=True)
            return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            print(f"[SQLite] Error fetching submissions: {str(e)}")
            return []

    def get_submissions_with_gps(self) -> List[Dict[str, Any]]:
        """Retrieves only submissions that have GPS coordinates."""
        query = "SELECT * FROM submissions WHERE gps_lat IS NOT NULL AND gps_lon IS NOT NULL ORDER BY timestamp DESC;"
        try:
            rows = self._execute(query, fetch_all=True)
            return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            print(f"[SQLite] Error fetching GPS submissions: {str(e)}")
            return []

    def get_statistics(self) -> Dict[str, Any]:
        """Calculates global aggregation statistics."""
        stats = {
            'total_scans': 0,
            'rivers_monitored': 0,
            'avg_density': 0.0,
            'critical_alerts': 0,
            'by_severity': {'low': 0, 'medium': 0, 'high': 0, 'critical': 0},
            'by_class': {'fragment': 0, 'fiber': 0, 'pellet': 0, 'film': 0}
        }
        
        try:
            # Total scans
            row = self._execute("SELECT COUNT(*) FROM submissions;", fetch_one=True)
            stats['total_scans'] = row[0] if row else 0
            
            if stats['total_scans'] > 0:
                # Unique location names
                row = self._execute("SELECT COUNT(DISTINCT location_name) FROM submissions WHERE location_name IS NOT NULL;", fetch_one=True)
                stats['rivers_monitored'] = row[0] if row else 0
                
                # Avg density
                row = self._execute("SELECT AVG(density_per_liter) FROM submissions;", fetch_one=True)
                stats['avg_density'] = float(row[0]) if row[0] is not None else 0.0
                
                # Critical counts
                row = self._execute("SELECT COUNT(*) FROM submissions WHERE severity = 'critical';", fetch_one=True)
                stats['critical_alerts'] = row[0] if row else 0
                
                # Breakdown by severity
                rows = self._execute("SELECT severity, COUNT(*) FROM submissions GROUP BY severity;", fetch_all=True)
                for r in rows:
                    if r[0] in stats['by_severity']:
                        stats['by_severity'][r[0]] = r[1]
                    
                # Breakdown by particle class sum
                row = self._execute("""
                    SELECT SUM(fragment_count), SUM(fiber_count), SUM(pellet_count), SUM(film_count)
                    FROM submissions;
                """, fetch_one=True)
                if row:
                    stats['by_class']['fragment'] = int(row[0]) if row[0] is not None else 0
                    stats['by_class']['fiber'] = int(row[1]) if row[1] is not None else 0
                    stats['by_class']['pellet'] = int(row[2]) if row[2] is not None else 0
                    stats['by_class']['film'] = int(row[3]) if row[3] is not None else 0
                    
            return stats
        except Exception as e:
            print(f"[SQLite] Error computing statistics: {str(e)}")
            return stats

    def delete_submission(self, submission_id: str) -> bool:
        """Deletes a submission by its ID.
        
        Args:
            submission_id (str): The unique ID.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        print(f"[SQLite] Deleting submission {submission_id}...")
        query = "DELETE FROM submissions WHERE id = ?;"
        try:
            cursor = self._execute(query, (submission_id,), commit=True)
            deleted = cursor.rowcount > 0
            print(f"[SQLite] Delete status: {deleted}")
            return deleted
        except Exception as e:
            print(f"[SQLite] Error deleting submission: {str(e)}")
            return False

    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """Converts a SQLite Row object to a standard submission dictionary."""
        r = dict(row)
        # Convert class counts into nested dictionary to match interface
        return {
            'id': r['id'],
            'timestamp': r['timestamp'],
            'particle_count': r['particle_count'],
            'class_counts': {
                'fragment': r['fragment_count'],
                'fiber': r['fiber_count'],
                'pellet': r['pellet_count'],
                'film': r['film_count']
            },
            'density_per_liter': r['density_per_liter'],
            'severity': r['severity'],
            'confidence': r['confidence'],
            'gps_lat': r['gps_lat'],
            'gps_lon': r['gps_lon'],
            'location_name': r['location_name'],
            'is_mock': bool(r['is_mock'])
        }
