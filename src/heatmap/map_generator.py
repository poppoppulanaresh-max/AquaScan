import folium
from folium.plugins import HeatMap
from typing import List, Dict, Any
from src.utils.config import SEVERITY_COLORS

def generate_heatmap(submissions: List[Dict[str, Any]]) -> folium.Map:
    """Generates an interactive Folium Map showing microplastic pollution heatmap and markers.
    
    Args:
        submissions (list[dict]): List of submissions containing 'gps_lat', 'gps_lon', etc.
        
    Returns:
        folium.Map: Folium Map object.
    """
    print(f"[Heatmap] Building map with {len(submissions)} points...")
    
    # Default center (India)
    default_lat, default_lon = 20.5937, 78.9629
    
    # Initialize Folium Map with CartoDB dark_matter tile layer
    m = folium.Map(
        location=[default_lat, default_lon],
        zoom_start=5,
        tiles="CartoDB dark_matter",
        control_scale=True
    )
    
    # If no submissions exist, just return the empty map
    if not submissions:
        print("[Heatmap] No submissions to display on the map.")
        return m
        
    # Filter submissions that have valid GPS data
    valid_subs = [s for s in submissions if s.get('gps_lat') is not None and s.get('gps_lon') is not None]
    
    if not valid_subs:
        print("[Heatmap] No submissions with valid GPS coordinates.")
        return m
        
    # Fit bounds if coordinates exist
    coords = [[s['gps_lat'], s['gps_lon']] for s in valid_subs]
    m.fit_bounds(coords)
    
    # Group layers
    marker_group = folium.FeatureGroup(name="Detections (Markers)")
    heatmap_group = folium.FeatureGroup(name="Pollution HeatMap", show=True)
    
    # Prepare data for HeatMap layer
    heat_data = []
    
    for sub in valid_subs:
        lat = sub['gps_lat']
        lon = sub['gps_lon']
        density = sub.get('density_per_liter', 0.0)
        severity = sub.get('severity', 'low').lower()
        color = SEVERITY_COLORS.get(severity, '#00B4D8')
        location = sub.get('location_name') or "Unknown Location"
        timestamp = sub.get('timestamp', '')
        count = sub.get('particle_count', 0)
        
        # Add to heat map data (lat, lon, weight)
        # Weight scales with density
        heat_data.append([lat, lon, density])
        
        # Create HTML Popup
        popup_html = f"""
        <div style="font-family: 'Inter', sans-serif; color: #E0F7FA; background-color: #03045E; padding: 10px; border-radius: 8px; border: 1px solid rgba(0,180,216,0.3); font-size: 12px; width: 200px;">
            <strong style="color: #00B4D8; font-size: 14px;">{location}</strong><br/>
            <hr style="border-color: rgba(0,180,216,0.2); margin: 6px 0;"/>
            <b>Severity:</b> <span style="color: {color}; font-weight: bold;">{severity.upper()}</span><br/>
            <b>Density:</b> {density:.2f} particles/L<br/>
            <b>Particle Count:</b> {count}<br/>
            <b>Date:</b> {timestamp[:10]}<br/>
        </div>
        """
        
        # Add marker to group
        folium.CircleMarker(
            location=[lat, lon],
            radius=12,
            popup=folium.Popup(popup_html, max_width=250),
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            weight=2
        ).add_to(marker_group)
        
    # Add HeatMap to Heatmap group
    if heat_data:
        HeatMap(heat_data, radius=25, blur=15, min_opacity=0.3).add_to(heatmap_group)
        
    # Add groups to map
    heatmap_group.add_to(m)
    marker_group.add_to(m)
    
    # Add Layer Control
    folium.LayerControl().add_to(m)
    
    # Add HTML Legend overlay
    legend_html = f"""
     <div style="
     position: fixed; 
     bottom: 50px; left: 50px; width: 150px; height: 130px; 
     border:2px solid rgba(0,180,216,0.3); background-color:#03045E;
     z-index:9999; font-size:11px;
     font-family: 'Inter', sans-serif;
     color: #E0F7FA;
     padding: 10px;
     border-radius: 8px;
     opacity: 0.9;
     ">
     <b style="color: #00B4D8;">Severity Legend</b><br>
     <i style="background:{SEVERITY_COLORS['low']}; width:12px; height:12px; float:left; margin-right:8px; border-radius:50%;"></i> Low<br>
     <i style="background:{SEVERITY_COLORS['medium']}; width:12px; height:12px; float:left; margin-right:8px; border-radius:50%;"></i> Medium<br>
     <i style="background:{SEVERITY_COLORS['high']}; width:12px; height:12px; float:left; margin-right:8px; border-radius:50%;"></i> High<br>
     <i style="background:{SEVERITY_COLORS['critical']}; width:12px; height:12px; float:left; margin-right:8px; border-radius:50%;"></i> Critical<br>
     </div>
     """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    print("[Heatmap] Map generation completed.")
    return m
