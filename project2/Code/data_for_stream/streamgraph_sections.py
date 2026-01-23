import json
import re
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------
# 1. Load section data
# ---------------------------------------------------

path = "/Users/MAFmedia1/Downloads/DH25/project_2/section_entity_counts.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

# ---------------------------------------------------
# 2. Normalize / sort section IDs like 1, 2, 2.1, 10.3.2
# ---------------------------------------------------

def section_key(sec_id):
    # Convert "2.1.3" -> [2, 1, 3] for proper numeric sorting
    return [int(x) for x in sec_id.split(".")]

section_ids = sorted(data.keys(), key=section_key)

# ---------------------------------------------------
# 3. Extract categories and build Y-matrix
# ---------------------------------------------------

# We assume all sections have the same keys
categories = list(next(iter(data.values())).keys())

# Example: categories = [
#   "revered_persons", "place_names", ...
# ]

# Build Y arrays (list of lists)
Y = []
for cat in categories:
    Y.append([data[sec][cat] for sec in section_ids])

# Convert to NumPy for stackplot
Y = np.array(Y)

# X-axis: section indices (0,1,2,...)
x = np.arange(len(section_ids))

# ---------------------------------------------------
# 4. Streamgraph (stackplot) - centered baseline
# ---------------------------------------------------

fig, ax = plt.subplots(figsize=(14, 7))

ax.stackplot(
    x,
    Y,
    labels=categories,
    baseline="sym"   # <-- symmetric river-like baseline
)


ax.set_title("Entity Category Counts per Section")
ax.set_xlabel("Section")
ax.set_ylabel("Count")
ax.set_xticks(x)
ax.set_xticklabels(section_ids, rotation=45, ha="right")

ax.legend(loc="upper left")
plt.tight_layout()
plt.show()
