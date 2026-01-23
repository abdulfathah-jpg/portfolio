
import re

from openai import OpenAI

import getpass

my_api_key = getpass.getpass("Please past your key here: ")

client = OpenAI(api_key = my_api_key)

input_file = "/Users/MAFmedia1/Downloads/DH25/project_2/annotated_ocr_manually_corrected.txt"

with open(input_file, "r", encoding="utf-8") as f:
    full_text = f.read()

sections = re.split(r'(?=^### \| )', full_text, flags=re.MULTILINE)  #Split text by top-level headings

# Separate heading title and content

structured_sections = []                                          

for sec in sections:
    if not sec.strip():
        continue

    lines = sec.splitlines()
    heading_line = lines[0]
    content = "\n".join(lines[1:]).strip()

    heading_title = heading_line.replace("### |", "").strip()

    structured_sections.append({
        "heading": heading_title,
        "text": content
    })


prompt_template = """
You are an expert in Muslim pilgrimage practices and Malayalam–Arabic devotional guidebooks.

You will receive a SMALL SECTION of text from a pilgrimage guidebook.

Your tasks:
1. Extract all mentions of the following entity types from the Malayalam portions only:

ENTITY TYPES:
- revered_persons (Eg: സഅദുബ്നു മുആദ്(റ),നബി(സ), അബൂബക്കർ (റ))
- sacred_objects_and_spaces (Eg. ഹുജ്റ ശരീഫ്, സ്വഫാ, മതാഫും)
- everyday_objects_and_persons(Eg. സുഗന്ധം,ഭാര്യ,താടി)
- ritual_concepts (Eg. ഇഅ്തികാഫിനെ,റക്അത്,നിയ്യത്തോടെ,ളുഹ്റ്) 
- instructive_language (Eg. പരിഗണിക്കുകയില്ല, നിർബന്ധമാണ്, അനിവാര്യമാണ്,ശുദ്ധിയുണ്ടാവുക)

Rules:
1. Return results ONLY in JSON.
2. The JSON must contain exactly these six keys.
3. Each occurrence must be listed separately.
4. Normalize spelling and OCR variants.
5. Do NOT translate or explain.
6. When a ritual concept or place name appears inside a longer phrase (e.g., because of grammar, inflection, or additional context), list it in the correct noun form as a separate entry. For instance, നിയ്യത്തോടെ should be listed as നിയ്യത്ത്) 

Text:
"""

# Loop over sections and call OpenAI

all_results = []

for section in structured_sections:
    print(f"Processing section: {section['heading']}")

    response = client.responses.create(
        model="gpt-5-nano",
        input=prompt_template + section["text"]
    )

    data = eval(response.output_text)

    all_results.append({
        "heading": section["heading"],
        "entities": data
    })

print(all_results)
