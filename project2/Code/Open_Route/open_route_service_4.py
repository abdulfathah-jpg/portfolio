import pandas as pd
import openrouteservice
import folium
from folium.plugins import AntPath

# Load CSV with English place names
df = pd.read_csv("pilgrimage_route_2.csv")
last_section = df['section_id'].max()

# ORS Client
API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImE4NDU5NTg1NDE2ODQ3M2ZhYzUwZWZhYWVjMzE4NzU2IiwiaCI6Im11cm11cjY0In0="  # replace with your ORS key
client = openrouteservice.Client(key=API_KEY)

# --------------------------
# Define chronological segments
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
    # remove consecutive duplicates
    pts = [pts[i] for i in range(len(pts)) if i == 0 or pts[i] != pts[i-1]]
    return pts

# --------------------------
# ORS routing helper
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
# Add bus/walk routes with animation
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
# Define LayerGroups for major/minor places
# --------------------------
major_layer = folium.FeatureGroup(name="Major Places", show=True)
all_layer = folium.FeatureGroup(name="All Places", show=False)  # hidden by default

# --------------------------
# Define major section_ids to show when zoomed out
# --------------------------
major_sections = [0, 18, 22, 53,]  # <-- adjust as needed

# --------------------------
# Add markers and permanent labels
# --------------------------
for idx, row in df.iterrows():
    label_html = f'<div style="font-size: 12pt; font-weight: bold; color: black">{row["place_name"]}</div>'
    
    if row['section_id'] in major_sections:
        # Major layer
        folium.Marker(
            [row['latitude'], row['longitude']],
            popup=row['place_name'],
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(major_layer)
        folium.map.Marker(
            [row['latitude'] + 0.0003, row['longitude']],
            icon=folium.DivIcon(icon_size=(150,36), icon_anchor=(0,0), html=label_html)
        ).add_to(major_layer)
    else:
        # Minor places: add directly to map instead of FeatureGroup
        label_html = f'<div style="font-size: 10pt; font-weight: bold; color: gray">{row["place_name"]}</div>'

        # Marker icon
        folium.Marker(
            [row['latitude'], row['longitude']],
            popup=row['place_name'],
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

        # Permanent label above marker

        folium.map.Marker(
            [row['latitude'] + 0.0003, row['longitude']],
            icon=folium.DivIcon(icon_size=(150,36), icon_anchor=(0,0), html=label_html)
        ).add_to(m)




# Add layers to map
major_layer.add_to(m)
all_layer.add_to(m)

# --------------------------
# Layer Control
# --------------------------
folium.LayerControl().add_to(m)

# --------------------------
# Save map
# --------------------------
m.save("pilgrimage_bus_walk_map.html")
print("✅ Map saved: pilgrimage_bus_walk_map.html")
