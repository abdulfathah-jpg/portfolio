import pandas as pd
import openrouteservice
import folium
from folium.plugins import AntPath

# Load CSV
df = pd.read_csv("pilgrimage_route_2.csv")
last_section = df['section_id'].max()

# ORS Client
API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImE4NDU5NTg1NDE2ODQ3M2ZhYzUwZWZhYWVjMzE4NzU2IiwiaCI6Im11cm11cjY0In0="  # replace with your ORS key
client = openrouteservice.Client(key=API_KEY)

# --------------------------
# Define chronological segments (correct structure!)
# --------------------------
segments = [
    ('bus', 0, 22),
    ('walk', 22, 24),
    ('bus', 24, 53),
    ('walk', 53, 57),
    ('bus', 57, last_section)
]

# --------------------------
# Helper: slice df for a segment
# --------------------------
def seg_df(start, end):
    """inclusive start, inclusive end"""
    return df[(df['section_id'] >= start) & (df['section_id'] <= end)]

# --------------------------
# Helper: convert segment to ORS-friendly coords
# --------------------------
def coords(seg):
    pts = list(zip(seg['longitude'], seg['latitude']))
    # remove consecutive dups
    pts = [pts[i] for i in range(len(pts)) if i == 0 or pts[i] != pts[i-1]]
    return pts

# --------------------------
# Route helper
# --------------------------
def ors_route(coord_list, profile):
    if len(coord_list) < 2:
        return None
    try:
        return client.directions(coordinates=coord_list, profile=profile, format='geojson')
    except Exception as e:
        print("ORS error:", e)
        return None

# --------------------------
# Create map
# --------------------------
m = folium.Map(location=[df['latitude'].iloc[0], df['longitude'].iloc[0]], zoom_start=6)

# --------------------------
# Process segments in chronological order
# --------------------------
for mode, start, end in segments:

    seg = seg_df(start, end)
    coord_lonlat = coords(seg)

    if len(coord_lonlat) < 2:
        continue

    profile = 'driving-car' if mode == 'bus' else 'foot-walking'
    route = ors_route(coord_lonlat, profile)

    if route:
        coords_latlon = [(c[1], c[0]) for c in route['features'][0]['geometry']['coordinates']]
        AntPath(
            coords_latlon,
            color='blue' if mode == 'bus' else 'green',
            weight=5,
            delay=800 if mode == 'bus' else 500
        ).add_to(m)

# --------------------------
# Add markers for each place
# --------------------------
for idx, row in df.iterrows():
    folium.Marker(
        [row['latitude'], row['longitude']],
        popup=row['place_name']
    ).add_to(m)

# Save map
m.save("pilgrimage_bus_walk_map.html")
print("✅ Fixed map saved: pilgrimage_bus_walk_map.html")
