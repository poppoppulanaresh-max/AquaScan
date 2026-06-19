import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from src.utils.config import SUPABASE_URL, SUPABASE_KEY

class SupabaseClient:
    def __init__(self, url: str = None, key: str = None):
        """Initializes the Supabase client.
        
        Args:
            url (str): Supabase API URL.
            key (str): Supabase Anon Key.
        """
        self.url = url or SUPABASE_URL
        self.key = key or SUPABASE_KEY
        self.client = None
        
        print(f"[Supabase] Initializing client. Url: {self.url}")
        
        if self.url and self.key:
            try:
                from supabase import create_client
                self.client = create_client(self.url, self.key)
                print("[Supabase] Connection client created successfully.")
            except Exception as e:
                print(f"[Supabase] Initialization failed: {str(e)}")
        else:
            print("[Supabase] Missing credentials. Supabase client disabled.")

    def is_active(self) -> bool:
        """Returns True if the Supabase client is configured and initialized."""
        return self.client is not None

    def save_submission(self, data: Dict[str, Any]) -> str:
        """Saves a submission to the Supabase database."""
        if not self.is_active():
            raise RuntimeError("Supabase client is not active.")
            
        print(f"[Supabase] Uploading submission {data.get('id')}...")
        class_counts = data.get('class_counts', {})
        payload = {
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
            'is_mock': int(data.get('is_mock', False))
        }
        
        try:
            response = self.client.table('submissions').insert(payload).execute()
            print("[Supabase] Upload successful.")
            return data.get('id')
        except Exception as e:
            print(f"[Supabase] Error uploading: {str(e)}")
            raise e

    def get_all_submissions(self) -> List[Dict[str, Any]]:
        """Retrieves all submissions from Supabase sorted by timestamp descending."""
        if not self.is_active():
            return []
            
        try:
            response = self.client.table('submissions').select('*').order('timestamp', desc=True).execute()
            rows = response.data or []
            return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            print(f"[Supabase] Error fetching all: {str(e)}")
            return []

    def get_submissions_with_gps(self) -> List[Dict[str, Any]]:
        """Retrieves submissions with valid GPS coordinates."""
        if not self.is_active():
            return []
            
        try:
            response = self.client.table('submissions') \
                .select('*') \
                .not_.is_('gps_lat', 'null') \
                .not_.is_('gps_lon', 'null') \
                .order('timestamp', desc=True) \
                .execute()
            rows = response.data or []
            return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            print(f"[Supabase] Error fetching GPS submissions: {str(e)}")
            return []

    def get_statistics(self) -> Dict[str, Any]:
        """Aggregates statistics from Supabase data."""
        stats = {
            'total_scans': 0,
            'rivers_monitored': 0,
            'avg_density': 0.0,
            'critical_alerts': 0,
            'by_severity': {'low': 0, 'medium': 0, 'high': 0, 'critical': 0},
            'by_class': {'fragment': 0, 'fiber': 0, 'pellet': 0, 'film': 0}
        }
        
        if not self.is_active():
            return stats
            
        try:
            submissions = self.get_all_submissions()
            stats['total_scans'] = len(submissions)
            
            if stats['total_scans'] > 0:
                locations = set()
                total_density = 0.0
                critical_count = 0
                
                for sub in submissions:
                    if sub.get('location_name'):
                        locations.add(sub['location_name'])
                        
                    total_density += sub.get('density_per_liter', 0.0)
                    
                    sev = sub.get('severity', 'low').lower()
                    stats['by_severity'][sev] = stats['by_severity'].get(sev, 0) + 1
                    if sev == 'critical':
                        critical_count += 1
                        
                    class_counts = sub.get('class_counts', {})
                    for key in stats['by_class']:
                        stats['by_class'][key] += class_counts.get(key, 0)
                        
                stats['rivers_monitored'] = len(locations)
                stats['avg_density'] = total_density / stats['total_scans']
                stats['critical_alerts'] = critical_count
                
            return stats
        except Exception as e:
            print(f"[Supabase] Error computing statistics: {str(e)}")
            return stats

    def delete_submission(self, submission_id: str) -> bool:
        """Deletes a submission from Supabase."""
        if not self.is_active():
            return False
            
        print(f"[Supabase] Deleting submission {submission_id}...")
        try:
            self.client.table('submissions').delete().eq('id', submission_id).execute()
            print("[Supabase] Deletion successful.")
            return True
        except Exception as e:
            print(f"[Supabase] Error deleting submission: {str(e)}")
            return False

    def _row_to_dict(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Normalizes a Supabase row to match the local dict format."""
        return {
            'id': row['id'],
            'timestamp': row['timestamp'],
            'particle_count': row['particle_count'],
            'class_counts': {
                'fragment': row.get('fragment_count', 0),
                'fiber': row.get('fiber_count', 0),
                'pellet': row.get('pellet_count', 0),
                'film': row.get('film_count', 0)
            },
            'density_per_liter': row['density_per_liter'],
            'severity': row['severity'],
            'confidence': row['confidence'],
            'gps_lat': row['gps_lat'],
            'gps_lon': row['gps_lon'],
            'location_name': row['location_name'],
            'is_mock': bool(row['is_mock'])
        }
