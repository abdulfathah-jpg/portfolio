# OpenAI NER for place names from headings and meta text for OpenRoute services


import re
import json
import getpass
from openai import OpenAI

my_api_key = getpass.getpass("Please paste your OpenAI API key here: ")
client = OpenAI(api_key=my_api_key)

# READ FILE + SPLIT FRONT/BODY/BACK

input_file = "/Users/MAFmedia1/Downloads/DH25/project_2/annotated_ocr_manually_corrected.txt"

with open(input_file, "r", encoding="utf-8") as f:
    full_text = f.read()

full_text = full_text.lstrip("\ufeff")

# Split text into lines
lines = full_text.splitlines()

front_matter = []
body_lines = []
back_matter = []

found_first_heading = False

for line in lines:
    if re.match(r'^###\s+\|+', line):
        found_first_heading = True

    if not found_first_heading:
        front_matter.append(line)
    else:
        body_lines.append(line)

# Back matter = text after last heading block

while body_lines and not body_lines[-1].strip():
    back_matter.insert(0, body_lines.pop())

# PARSE HEADINGS

sections = []
stack = []

for line in body_lines:

    heading_match = re.match(r'^(###\s+(\|+))\s*(.*)', line)

    if heading_match:
        level = len(heading_match.group(2))
        heading_title = heading_match.group(3).strip()

        section = {
            "heading": heading_title,
            "level": level,
            "text": "",
            "subsections": [],
            "entities": None,
            "heading_places": []   # NEW
        }

        while stack and stack[-1]["level"] >= level:
            stack.pop()

        if stack:
            stack[-1]["subsections"].append(section)
        else:
            sections.append(section)

        stack.append(section)

    else:
        if stack:
            stack[-1]["text"] += line + "\n"

# PLACE-ONLY PROMPT

place_only_prompt = """
Extract ONLY place names from the following text. Example of place names are: റിയാദ്, മീഖാത്ത്, etc

Rules:
1. Extract place names in Malayalam script
2. Return ONLY JSON.
3. JSON must contain ONE key: "place_names"
3. Normalize spelling and OCR variants.
4. Preserve original script in the ouput i.e., Malayalam.
5. Do NOT translate or explain.
6. When a place name appears inside a longer phrase (e.g., because of grammar, inflection, or additional context), list it in the correct noun form as a separate entry. For instance, നിയ്യത്തോടെ should be listed as നിയ്യത്ത്) 

Text:
"""

# extract places from ANY small text

def extract_places(text):
    response = client.responses.create(
        model="gpt-5-nano",
        input=place_only_prompt + text
    )

    try:
        data = json.loads(response.output_text)
        return data.get("place_names", [])
    except:
        return []

# ADD PLACE EXTRACTION TO HEADINGS

def attach_heading_places(section):
    print(f"Processing heading for places: {section['heading']}") 
    section["heading_places"] = extract_places(section["heading"])

    for sub in section["subsections"]:
        attach_heading_places(sub)

for sec in sections:
    attach_heading_places(sec)

# FUNCTION: extract places from META sections

def extract_meta_places(section):
    """
    Recursively extract place names from META sections only.
    """
    meta_places = []

    if section["heading"].upper() == "META":
        meta_places = extract_places(section["text"])
        meta_places = list(set(meta_places))  # remove duplicates
        print(f"Extracted META places for section '{section['heading']}': {meta_places}")

    # Recurse into subsections in case nested META sections exist
    for sub in section["subsections"]:
        meta_places.extend(extract_meta_places(sub))

    return meta_places

# Find start_places from first META section

route_meta = {
    "start_places": [],
    "end_places": []
}

for sec in sections:
    if sec["heading"].upper() == "META":
        route_meta["start_places"] = extract_meta_places(sec)
        break

# Find end_places from last META section

for sec in reversed(sections):
    if sec["heading"].upper() == "META":
        route_meta["end_places"] = extract_meta_places(sec)
        break

print(f"Start places: {route_meta['start_places']}")
print(f"End places: {route_meta['end_places']}")

# saving all output together

output = {
    "route_meta": route_meta,
    "sections": sections
}

with open("ner_with_route_data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("✅ Done. Data ready for QGIS.")


