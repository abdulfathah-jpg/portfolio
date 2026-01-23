import pandas as pd
import openrouteservice
import folium
from folium.plugins import AntPath  

# Load CSV
df = pd.read_csv("pilgrimage_route.csv")

# ORS client
API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImE4NDU5NTg1NDE2ODQ3M2ZhYzUwZWZhYWVjMzE4NzU2IiwiaCI6Im11cm11cjY0In0="  # replace with your ORS key
client = openrouteservice.Client(key=API_KEY)

# Define bus and walking segments
bus_ranges = [(0,23), (24,53), (57,999)]
walk_ranges = [(23,24), (53,57)]

def get_segment(df, ranges):
    """Return concatenated DataFrame for multiple ranges."""
    return pd.concat([df[df['section_id'].between(start, end)] for start, end in ranges])

bus_segments = get_segment(df, bus_ranges)
walk_segments = get_segment(df, walk_ranges)

# Ensure coordinates are in [lon, lat] format
def coords_list(df_segment):
    coords = list(zip(df_segment['longitude'], df_segment['latitude']))
    # convert tuples to lists
    coords = [list(c) for c in coords]
    # remove duplicates
    coords = [coords[i] for i in range(len(coords)) if i == 0 or coords[i] != coords[i-1]]
    return coords

# Function to get route from ORS with error handling
def get_route(coords, profile):
    if len(coords) < 2:
        return None  # cannot route a single point
    try:
        return client.directions(coordinates=coords, profile=profile, format='geojson')
    except openrouteservice.exceptions.ApiError as e:
        print(f"ORS error: {e}")
        return None

# Create map
m = folium.Map(location=[df['latitude'].iloc[0], df['longitude'].iloc[0]], zoom_start=6)

# Add bus routes with animation (AntPath)
bus_coords = coords_list(bus_segments)
bus_route = get_route(bus_coords, profile='driving-car')
if bus_route:
    # Extract coordinates from ORS GeoJSON ([lon, lat] -> [lat, lon])
    bus_line_coords = [(coord[1], coord[0]) for coord in bus_route['features'][0]['geometry']['coordinates']]
    # Add animated line using AntPath
    AntPath(bus_line_coords, color='blue', weight=5, delay=1000).add_to(m)

# Add walking routes (static lines)
walk_coords = coords_list(walk_segments)
walk_route = get_route(walk_coords, profile='foot-walking')
if walk_route:
    folium.GeoJson(walk_route, name="Walking Route", style_function=lambda x: {'color':'green','weight':4}).add_to(m)

# Add markers for all points
for idx, row in df.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=row['place_name']).add_to(m)

# Layer control
folium.LayerControl().add_to(m)

# Save map
m.save("pilgrimage_bus_walk_map.html")
print("✅ Map saved: pilgrimage_bus_walk_map.html")
