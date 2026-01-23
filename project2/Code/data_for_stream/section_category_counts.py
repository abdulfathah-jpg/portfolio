import json

# ---------------------------------------------
# 1. LOAD NER OUTPUT
# ---------------------------------------------

input_file = "ner_by_section_nested.json"

with open(input_file, "r", encoding="utf-8") as f:
    sections = json.load(f)


# ---------------------------------------------
# 2. RECURSIVE WALK
# ---------------------------------------------

def walk_sections(section, counts):
    sec_id = section.get("section_id")
    
    # Ensure section_id entry exists
    if sec_id not in counts:
        counts[sec_id] = {
            "revered_persons": 0,
            "place_names": 0,
            "sacred_objects_and_spaces": 0,
            "everyday_objects_and_persons": 0,
            "ritual_concepts": 0,
            "instructive_language": 0,
            "arabic_litanies_and_recitations": 0
        }
    
    # Count items in each category
    entities = section.get("entities", {})
    
    for category in counts[sec_id].keys():
        values = entities.get(category, [])
        counts[sec_id][category] += len(values)

    # Recurse into subsections
    for sub in section.get("subsections", []):
        walk_sections(sub, counts)


# ---------------------------------------------
# 3. BUILD COUNTS
# ---------------------------------------------

section_counts = {}

for sec in sections:
    walk_sections(sec, section_counts)


# ---------------------------------------------
# 4. SAVE OUTPUT
# ---------------------------------------------

output_file = "section_entity_counts.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(section_counts, f, ensure_ascii=False, indent=2)

print(f"✓ Section/entity totals saved to {output_file}")
