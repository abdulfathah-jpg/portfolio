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
    return [int(x) for x in sec_id.split(".")]

section_ids = sorted(data.keys(), key=section_key)

# ---------------------------------------------------
# 3. Extract categories and build Y-matrix
# ---------------------------------------------------

categories = list(next(iter(data.values())).keys())

Y = []
for cat in categories:
    Y.append([data[sec][cat] for sec in section_ids])

Y = np.array(Y)
x = np.arange(len(section_ids))

# ---------------------------------------------------
# (A) ADDED: Wiggle baseline function
# ---------------------------------------------------

def wiggle_baseline(Y):
    L, T = Y.shape
    total = np.sum(Y, axis=0)

    slopes = np.zeros((L, T))
    slopes[:, 1:-1] = (Y[:, 2:] - Y[:, :-2]) / 2.0
    slopes[:, 0] = slopes[:, 1]
    slopes[:, -1] = slopes[:, -2]

    baseline = np.zeros(T)
    for t in range(T):
        s = 0.0
        for i in range(L):
            for j in range(i+1, L):
                s += slopes[j, t]
        baseline[t] = -s / total[t] if total[t] != 0 else 0

    baseline = np.cumsum(baseline)
    baseline -= np.mean(baseline)
    return baseline

# ---------------------------------------------------
# (B) ADDED: Compute wiggle offsets for plotting
# ---------------------------------------------------

baseline = wiggle_baseline(Y)

offsets = np.zeros_like(Y)
current = baseline.copy()
for i in range(Y.shape[0]):
    offsets[i] = current + Y[i] / 2
    current += Y[i]

# ---------------------------------------------------
# 4. Streamgraph Plot (replaces stackplot)
# ---------------------------------------------------

fig, ax = plt.subplots(figsize=(14, 7))

for i in range(Y.shape[0]):
    ax.fill_between(
        x,
        offsets[i] - Y[i],
        offsets[i],
        label=categories[i],
        alpha=0.7
    )

ax.set_title("Entity Category Counts per Section (Wiggle Streamgraph)")
ax.set_xlabel("Section")
ax.set_ylabel("Count")
ax.set_xticks(x)
ax.set_xticklabels(section_ids, rotation=45, ha="right")

ax.legend(loc="upper left")
plt.tight_layout()
plt.show()
