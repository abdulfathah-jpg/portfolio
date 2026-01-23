import json
import pandas as pd
import altair as alt

# -----------------------------
# 1. Load JSON section/entity counts
# -----------------------------
path = "/Users/MAFmedia1/Downloads/DH25/project_2/section_entity_counts.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

# -----------------------------
# 2. Define categories and sort sections numerically
# -----------------------------
categories = list(next(iter(data.values())).keys())

def section_to_tuple(sec_id):
    return tuple(int(x) for x in sec_id.split("."))

sorted_sections = sorted(data.keys(), key=section_to_tuple)
section_index_map = {sec: i for i, sec in enumerate(sorted_sections)}

# -----------------------------
# 3. Level-1 section translated headings
# -----------------------------
# Only level-1 sections (IDs in order)
level1_section_ids = [
    "1","2","3","4","5","6","7","8","9","10",
    "11","12","13","14","15","16","17","18","19","20"
]

level1_translations = [
    "Al-Quds", "Umra", "Preparation", "Jamu’ & Qasr", "Miqat",
    "Niyyah", "To Makkah", "Masjid al-Haram", "Ka'ba Sharif", "Tawaf",
    "Zamzam", "Sa’y", "Tawaf Wida'", "Masjid an-Nabawi", "To Sacred Presence",
    "Jannat al-Baqi'", "Mazarat", "Important Adhkars", "Items to Keep in Travel", "A Special Hamla for Malayalis"
]

# Map section ID → label (only level-1 headings)
section_label_map = {}
for sec in sorted_sections:
    if sec in level1_section_ids:
        idx = level1_section_ids.index(sec)
        section_label_map[sec] = f"{sec} {level1_translations[idx]}"
    else:
        section_label_map[sec] = ""  # sub-sections have no label

# -----------------------------
# 4. Build long-form DataFrame
# -----------------------------
rows = []
for sec in sorted_sections:
    for cat in categories:
        rows.append([sec, cat, data[sec][cat], section_index_map[sec]])

df = pd.DataFrame(rows, columns=["section", "category", "value", "section_index"])

# -----------------------------
# 5. Create Altair Streamgraph
# -----------------------------
# Use labelExpr to map numeric x -> custom label
label_expr = "[\"" + '","'.join([section_label_map[s] for s in sorted_sections]) + "\"][datum.value]"

chart = (
    alt.Chart(df)
    .mark_area(interpolate="basis")  # smooth flowing layers
    .encode(
        x=alt.X(
            "section_index:Q",
            axis=alt.Axis(
                title="Section",
                values=list(range(len(sorted_sections))),
                labelExpr=label_expr,
                labelAngle=90,
                labelFontSize=10
            )
        ),
        y=alt.Y("value:Q", stack="center", title="Entity Count"),
        color=alt.Color("category:N", title="Entity Category"),
        tooltip=["section", "category", "value"]
    )
    .properties(
        width=2000,
        height=500,
        title="Streamgraph of Entity Frequencies Across Sections"
    )
)

# -----------------------------
# 6. Save to HTML
# -----------------------------
chart.save("streamgraph.html")
print("✅ Streamgraph saved as streamgraph.html — open in browser to view.")
