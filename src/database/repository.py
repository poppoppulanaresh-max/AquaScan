import os
from typing import List, Dict, Any
from src.utils.config import SUPABASE_URL, SUPABASE_KEY
from src.database.sqlite_client import SQLiteClient
from src.database.supabase_client import SupabaseClient

class Repository:
    def __init__(self):
        """Unified database interface that automatically selects SQLite or Supabase.
        
        Selection is based on the presence of the SUPABASE_URL environment variable.
        """
        self.use_supabase = False
        self.client = None
        
        # Check if Supabase URL is set
        if SUPABASE_URL:
            print("[Repository] Supabase URL detected. Attempting to use Supabase...")
            client_candidate = SupabaseClient(SUPABASE_URL, SUPABASE_KEY)
            if client_candidate.is_active():
                self.client = client_candidate
                self.use_supabase = True
                print("[Repository] Database provider configured: SUPABASE.")
            else:
                print("[Repository] Supabase initialization failed. Falling back to SQLite.")
                
        if not self.use_supabase or self.client is None:
            print("[Repository] Database provider configured: SQLITE.")
            self.client = SQLiteClient()

    def save_submission(self, data: Dict[str, Any]) -> str:
        """Saves a submission using the active database client.
        
        Args:
            data (dict): The submission dictionary.
            
        Returns:
            str: Unique submission ID.
        """
        return self.client.save_submission(data)

    def get_all_submissions(self) -> List[Dict[str, Any]]:
        """Retrieves all submissions from the active database."""
        return self.client.get_all_submissions()

    def get_submissions_with_gps(self) -> List[Dict[str, Any]]:
        """Retrieves submissions that contain GPS coordinates from the active database."""
        return self.client.get_submissions_with_gps()

    def get_statistics(self) -> Dict[str, Any]:
        """Gathers aggregate statistics across submissions from the active database."""
        return self.client.get_statistics()

    def delete_submission(self, submission_id: str) -> bool:
        """Deletes a submission from the active database."""
        return self.client.delete_submission(submission_id)
