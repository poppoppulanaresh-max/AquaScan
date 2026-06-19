from typing import List, Dict, Any

def calculate_spatial_stats(submissions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculates spatial statistics from submissions for the dashboard.
    
    Args:
        submissions (list[dict]): Submissions records list.
        
    Returns:
        dict: Summary statistics including cleanest, dirtiest locations, and critical alerts.
    """
    stats = {
        'total_points': 0,
        'most_polluted_river': "N/A",
        'cleanest_area': "N/A",
        'critical_zones': 0
    }
    
    if not submissions:
        return stats
        
    stats['total_points'] = len(submissions)
    
    # Group by location name
    loc_groups = {}
    critical_count = 0
    
    for sub in submissions:
        loc = sub.get('location_name')
        if not loc:
            continue
            
        density = sub.get('density_per_liter', 0.0)
        severity = sub.get('severity', 'low').lower()
        
        if severity == 'critical':
            critical_count += 1
            
        if loc not in loc_groups:
            loc_groups[loc] = []
        loc_groups[loc].append(density)
        
    stats['critical_zones'] = critical_count
    
    # Calculate averages per location
    if loc_groups:
        loc_averages = {loc: sum(densities)/len(densities) for loc, densities in loc_groups.items()}
        
        # Sort locations by average density
        sorted_locs = sorted(loc_averages.items(), key=lambda x: x[1])
        
        stats['cleanest_area'] = f"{sorted_locs[0][0]} ({sorted_locs[0][1]:.1f} P/L)"
        stats['most_polluted_river'] = f"{sorted_locs[-1][0]} ({sorted_locs[-1][1]:.1f} P/L)"
        
    return stats
