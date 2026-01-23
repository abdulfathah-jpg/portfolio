import json

# ---------------------------------------------
# 1. LOAD NER OUTPUT
# ---------------------------------------------

input_file = "ner_by_section_nested.json"

with open(input_file, "r", encoding="utf-8") as f:
    sections = json.load(f)

# ---------------------------------------------
# 2. RECURSIVE WALK FUNCTION
# ---------------------------------------------

def walk_sections(section, index):
    sec_id = section.get("section_id")

    # Extract entities
    entities = section.get("entities", {})
    for category, values in entities.items():
        for v in values:
            index.setdefault(category, {})
            index[category].setdefault(v, [])
            index[category][v].append(sec_id)

    # Walk children
    for sub in section.get("subsections", []):
        walk_sections(sub, index)

# ---------------------------------------------
# 3. BUILD INVERTED INDEX
# ---------------------------------------------

entity_index = {}

for sec in sections:
    walk_sections(sec, entity_index)

# ---------------------------------------------
# 4. Adding Frequencies
# ---------------------------------------------

for category, items in entity_index.items():
    for entity, sec_ids in items.items():
        entity_index[category][entity] = {
            "sections": sec_ids,
            "count": len(sec_ids)
        }


# ---------------------------------------------
# 5. SAVE RESULTS
# ---------------------------------------------

output_file = "entity_index.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(entity_index, f, ensure_ascii=False, indent=2)

print(f"✓ Entity index successfully saved to {output_file}")
