import pandas as pd
import openrouteservice
import folium

# Load CSV
df = pd.read_csv("pilgrimage_route.csv")

# ORS client
API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImE4NDU5NTg1NDE2ODQ3M2ZhYzUwZWZhYWVjMzE4NzU2IiwiaCI6Im11cm11cjY0In0="
client = openrouteservice.Client(key=API_KEY)

# Decide travel type for each segment
# Example: section_id 0-22 -> bus, 22-24 -> walk
# Bus segments
bus_ranges = [(0,23), (24,999)]  # adjust so end is exclusive
bus_segments = pd.concat([df[df['section_id'].between(start, end, inclusive="both")] for start,end in bus_ranges])

# Walk segments
walk_ranges = [(23,24), (53,57)]
walk_segments = pd.concat([df[df['section_id'].between(start, end, inclusive="both")] for start,end in walk_ranges])

# Function to get route from ORS
def get_route(coords, profile):
    return client.directions(coordinates=coords, profile=profile, format='geojson')

# Create map
m = folium.Map(location=[df['latitude'].iloc[0], df['longitude'].iloc[0]], zoom_start=6)

# Add bus route
bus_coords = list(zip(bus_segments['longitude'], bus_segments['latitude']))
bus_route = get_route(bus_coords, profile='driving-car')
folium.GeoJson(bus_route, name="Bus Route", style_function=lambda x: {'color':'blue','weight':4}).add_to(m)

# Add walking route
walk_coords = list(zip(walk_segments['longitude'], walk_segments['latitude']))
walk_route = get_route(walk_coords, profile='foot-walking')
folium.GeoJson(walk_route, name="Walking Route", style_function=lambda x: {'color':'green','weight':4}).add_to(m)

# --------------------------------------------------
## Animated Bus

from folium.plugins import AntPath

# Extract coordinates from bus_route GeoJSON
bus_line_coords = [(coord[1], coord[0]) for coord in bus_route['features'][0]['geometry']['coordinates']]

# Add animated line to map
AntPath(bus_line_coords, 
        color='blue', 
        weight=5, 
        delay=1000).add_to(m)

# --- Add moving marker with timestamps ---

from folium.plugins import TimestampedGeoJson

features = []
for i, (lat, lon) in enumerate(bus_line_coords):
    features.append({
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lon, lat]},
        "properties": {"time": f"2025-12-30T12:{i:02d}:00", "popup": f"Bus {i}"}
    })

TimestampedGeoJson({
    "type": "FeatureCollection",
    "features": features
}, period='PT1M', add_last_point=True, auto_play=True).add_to(m)

# --------------------------------------------------
## Add markers with sequence number
for i, row in enumerate(df.itertuples(), start=1):
    folium.Marker(
        [row.latitude, row.longitude],
        popup=f"{i}. {row.place_name}",  # shows sequential number + place name
        tooltip=f"{i}. {row.place_name}"  # shows on hover
    ).add_to(m)
# --------------------------------------------------

# Layer control
folium.LayerControl().add_to(m)

# Save map
m.save("pilgrimage_bus_walk_map.html")
print("✅ Map saved: pilgrimage_bus_walk_map.html")

from folium.plugins import AntPath

# Extract coordinates from bus_route GeoJSON
bus_line_coords = [(coord[1], coord[0]) for coord in bus_route['features'][0]['geometry']['coordinates']]

# Add animated line
AntPath(bus_line_coords, 
        color='blue', 
        weight=5, 
        delay=1000).add_to(m)

