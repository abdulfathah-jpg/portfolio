import re
import json
import getpass
from openai import OpenAI

# --------------------------------------------------
# 1. API SETUP
# --------------------------------------------------

my_api_key = getpass.getpass("Please paste your OpenAI API key here: ")
client = OpenAI(api_key=my_api_key)

# --------------------------------------------------
# 2. READ INPUT FILE
# --------------------------------------------------

input_file = "/Users/MAFmedia1/Downloads/DH25/project_2/annotated_ocr_manually_corrected.txt"

with open(input_file, "r", encoding="utf-8") as f:
    full_text = f.read()
full_text = full_text.lstrip("\ufeff")

# --------------------------------------------------
# 3. PARSE OPENITI HEADINGS (MULTI-LEVEL)
# --------------------------------------------------
# Supports:
# ### |     → level 1
# ### ||    → level 2
# ### |||   → level 3
# etc.

sections = []
stack = []

for line in full_text.splitlines():

    heading_match = re.match(r'^(###\s+(\|+))\s*(.*)', line)

    if heading_match:
        level = len(heading_match.group(2))
        heading_title = heading_match.group(3).strip()

        section = {
            "heading": heading_title,
            "level": level,
            "text": "",
            "subsections": [],
            "entities": None
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

# --------------------------------------------------
# 4. NER PROMPT (STRICT + CONSISTENT KEYS)
# --------------------------------------------------


prompt_template = """
You are an expert in Muslim pilgrimage practices and Malayalam–Arabic devotional guidebooks.

You will receive a SMALL SECTION of text from a pilgrimage guidebook.

Your tasks:
PART A — Malayalam analysis
Extract all mentions of the following entity types from the Malayalam portions only:

ENTITY TYPES:
- revered_persons (Eg. സഅദുബ്നു മുആദ്(റ),നബി(സ), അബൂബക്കർ (റ))
- place_names (Eg. ഉഹ്ദ്, ദുൽഹുലൈഫ(അബയാർ അലി,മസ്ജിദുൽ ഹറാം)
- sacred_objects_and_spaces (Eg. ഹുജ്റ ശരീഫ്, സ്വഫാ, മതാഫ്)
- everyday_objects_and_persons(Eg. സുഗന്ധം,ഭാര്യ,താടി, റൂം, വാഹനം)
- ritual_concepts (Eg. ഇഅ്തികാഫ്,റക്അത്,നിയ്യത്ത്,ളുഹ്റ്) 
- instructive_language (Eg. പരിഗണിക്കുക, നിർബന്ധം, അനിവാര്യം,ശുദ്ധിയുണ്ടാവുക)

Rules for PART A:

1. Extract from Malayalam text only.
2. Each occurrence must be listed separately.
3. Normalize spelling and OCR variants.
4. Preserve original script in the ouput i.e., Malayalam.
5. Do NOT translate or explain.
6. When a ritual concept or place name appears inside a longer phrase (e.g., because of grammar, inflection, or additional context), list it in the correct noun form as a separate entry. For instance, നിയ്യത്തോടെ should be listed as നിയ്യത്ത്) 

PART B — Arabic liturgical content
Extract ALL Arabic-script text that functions as either:
- a litany, supplication, dhikr, or formula to be recited (Eg. لَبَّيْكَ أَللَّهُمَّ لَبَّيْكَ لَبَّيْكَ لا شَريكَ لَكَ لَبَّيْكَ إِنَّ الْحَمْدَ وَالنِّعْمَةَ لَكَ وَالْمُلْكَ لاَ شَريكَ لَكَ) 
- the name of a Qurʾānic sūrah or verse explicitly instructed to be recited (Eg.  قُلْ أَعُوذُ بِرَبِّ النَّاسُ) 

Rules for Part B
1. Extract ONLY Arabic-script text.
2. Include full litany text exactly as written (do not normalize).
3. Include Arabic names of sūrahs even if mentioned within Malayalam sentences.
4. Preserve original script in the ouput i.e., Arabic.
5. Do NOT extract Arabic text that is biographical or non-ritual.


OUTPUT FORMAT:

1. Return results only in JSON 
2. The JSON MUST contain ONLY the following SEVEN keys and NO OTHERS:
- revered_persons
- place_names
- sacred_objects_and_spaces
- everyday_objects_and_persons
- ritual_concepts
- instructive_language
- arabic_litanies_and_recitations
If a category has no items, return an empty list.
3. Each value must be a list

Text:
"""

# --------------------------------------------------
# 5. RECURSIVE NER FUNCTION
# --------------------------------------------------

def run_ner_on_section(section, section_id):

    print(f"Processing section {section_id}: {section['heading']}")

    response = client.responses.create(
        model="gpt-5-nano",
        input=prompt_template + section["text"]
    )

    try:
        data = json.loads(response.output_text)
    except json.JSONDecodeError:
        print("⚠️ JSON parsing error. Storing empty entity lists.")
        data = {
            "revered_persons": [],
            "sacred_objects_and_spaces": [],
            "everyday_objects_and_persons": [],
            "ritual_concepts": [],
            "instructive_language": [],
            "unclassified": []
        }

    section["entities"] = data
    section["section_id"] = section_id

    for i, sub in enumerate(section["subsections"], start=1):
        run_ner_on_section(sub, f"{section_id}.{i}")

# --------------------------------------------------
# 6. RUN NER ON ALL SECTIONS
# --------------------------------------------------

for i, sec in enumerate(sections, start=1):
    run_ner_on_section(sec, str(i))

# --------------------------------------------------
# 7. SAVE FINAL OUTPUT
# --------------------------------------------------

output_file = "ner_by_section_nested.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(sections, f, ensure_ascii=False, indent=2)

print(f"\n✅ NER completed. Output saved to {output_file}")
