import math
from datetime import datetime
from src.utils.config import SEVERITY_COLORS

def format_timestamp(iso_str: str) -> str:
    """Formats an ISO-8601 string into a human-readable format.
    
    Args:
        iso_str (str): The datetime string in ISO format.
        
    Returns:
        str: Formatted date time string.
    """
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%B %d, %Y - %I:%M %p")
    except ValueError:
        return iso_str

def get_severity_color(severity: str) -> str:
    """Gets the corresponding hex color for a given severity level.
    
    Args:
        severity (str): 'low', 'medium', 'high', or 'critical'.
        
    Returns:
        str: Hex color code.
    """
    return SEVERITY_COLORS.get(severity.lower(), '#90CAF9')

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates the Haversine distance in kilometers between two coordinates.
    
    Args:
        lat1 (float): Latitude of coordinate 1.
        lon1 (float): Longitude of coordinate 1.
        lat2 (float): Latitude of coordinate 2.
        lon2 (float): Longitude of coordinate 2.
        
    Returns:
        float: Distance in kilometers.
    """
    R = 6371.0 # Earth's radius in kilometers
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2.0)**2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    
    return R * c
