import json
import csv

# Load the clean JSON
with open("ner_with_route_data.json", "r", encoding="utf-8-sig") as f:
    data = json.load(f)

sections = data["sections"]
route_meta = data["route_meta"]

# Coordinates for key places
PLACE_COORDS = {
    "റിയാദ്": (24.65789534, 46.72688078),
    "മക്ക": (21.42514493, 39.81644661),
    "മദീന": (24.4672, 39.6111),
    "മസ്ജിദുൽ ഹറാം": (21.42263927, 39.82618582),
    "മസ്ജിദുന്നബവി": (24.46755258, 39.61110182),
    "സ്വഫ": (21.4227, 39.8261),
    "മർവ": (21.4229, 39.8258),
    "ജന്നത്തുൽ ബഖീ": (24.46634571, 39.61698892),
    "മീഖാത്ത്": (21.63294280, 40.42809930),
    "കാബാ": (21.42263927, 39.82618582),
    "ഉഹ്ദ്": (24.50765006, 39.61234953),
    "മസ്ജിദുൽ ഫത്ഹ്": (24.47805478, 39.59552570),
    "മസ്ജിദുൽ ഖിബ്ലതൈൻ": (24.48435634, 39.57893474),
    "മസ്ജിദുൽ ഖുബാഅ്": (24.43954738, 39.61740799),
}

all_rows = []
section_counter = 1  # incremental ID

# Flatten headings and extract place names
def collect_places(section):
    global section_counter
    for place in section.get("heading_places", []):
        if place in PLACE_COORDS:
            lat, lon = PLACE_COORDS[place]
            all_rows.append([
                section_counter,
                section["heading"],
                place,
                lat,
                lon
            ])
    section_counter += 1
    for sub in section.get("subsections", []):
        collect_places(sub)

for sec in sections:
    collect_places(sec)

# Add start places (FRONT)
for place in route_meta["start_places"]:
    if place in PLACE_COORDS:
        lat, lon = PLACE_COORDS[place]
        all_rows.insert(0, [0, "START", place, lat, lon])

# Add end places (BACK)
for place in route_meta["end_places"]:
    if place in PLACE_COORDS:
        lat, lon = PLACE_COORDS[place]
        all_rows.append([999, "END", place, lat, lon])

# Write CSV
with open("pilgrimage_route1.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["section_id", "heading", "place_name", "latitude", "longitude"])
    writer.writerows(all_rows)

print("✅ CSV created: pilgrimage_route1.csv")
