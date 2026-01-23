import json
import pandas as pd
import numpy as np
from collections import Counter
import altair as alt

# -----------------------------
# 1. Load JSON entity data
# -----------------------------
path = "/Users/MAFmedia1/Downloads/DH25/project_2/entity_index_3.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

# -----------------------------
# 2. Level-1 section mapping
# -----------------------------
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

parent_label_map = {sec: label for sec, label in zip(level1_section_ids, level1_translations)}

def get_parent(sec):
    return sec.split(".")[0]

# -----------------------------
# 3. Transliteration maps for all entity categories
# -----------------------------
# Only a subset shown; replace ... with full transliteration maps
# 3. Transliteration maps for all entity categories
translit_maps = {
    "place_names": {
    "അൽഖുദ്സ്": "Al-Quds", "റിയാദ്": "Riyadh", "സഫാ": "Safa", "മർവ": "Marwa",
    "മീഖാത്": "Miqat", "ദുൽഹുലൈഫ": "Dhul-Hulayfah", "മക്ക": "Makkah",
    "താഇഫ്": "Ta'if", "മദീന": "Madinah", "ഖർനുൽ മനാസ്": "Qarn al-Manas",
    "മീഖാത്ത്": "Miqat", "ഹറമ": "Haram", "മസ്ജിദുൽ ഹറാം": "Masjid al-Haram",
    "ബാബുസ്സലാമ്": "Bab al-Salam", "കാബാലയം": "Ka'ba", "കഅ്ബ": "Ka'ba",
    "മഖാം": "Maqam", "ഹറാം": "Haram", "സ്വഫാ": "Safa", "മർവ്വ": "Marwa",
    "കഅബാ ശരീഫ്": "Ka'ba Sharif", "മഖാമു ഇബ്രാഹീം": "Maqam Ibrahim",
    "മക്കാ ശരീഫിൽ": "Makkah Sharif", "റൗളാ ശരീഫ്": "Rawdha Sharif",
    "മസ്ജിദുന്നബവി": "Masjid an-Nabawi", "ഹുജ്റ ശരീഫ്": "Hujra Sharif",
    "പുണ്യഖബർ": "Holy Tomb", "ബഖീഇലെ": "Baqi'",
    "ജന്നത്തുൽ ബഖീഅ്": "Jannat al-Baqi'", "ഉഹ്ദ്": "Uhd", "കാബാ ശരീഫ്":"Ka'ba Sharif",
    "ജബലു റുമാത്ത്": "Jabal Rumath", "മസ്ജിദുൽ ഫത്ഹ്": "Masjid al-Fath",
    "കഅബാ ശരീഫ":"Ka'ba Sharif",
    "ഖൻദഖ്": "Khandakh", "ബൈത്തുൽ മുഖദ്ദസിലേക്ക്": "Bayt al-Muqaddas",
    "മസ്ജിദു ബനൂ സലമ": "Masjid Banu Salam", "മസ്ജിദുൽ ഖിബ്ലത Hein": "Masjid al-Qiblathain",
    "മസ്ജിദുൽ ഖ ubാഅ്": "Masjid al-Quba'", "മദീൻ": "Madyan"
    },
    "ritual_concepts": {
        "ഉംറ": "Umrah",
        "ഇഹ്റാം": "Ihram",
        "ത്വവാഫ്": "Tawaf",
        "സഅ്യ്": "Sa’y",
        "ദുആ": "Dua",
        "പ്രതിജ്ഞ": "Pledge",
        "റക്അത്": "Rak'at",
        "സ്വലാത്": "Salat",
        "ദിക്ര്": "Dhikr",
        "ജംഉം": "Jumu’ah",
        "ഖസ്റ്": "Qasr",
        "റക्अത്": "Rak'at",
        "നിയ്യത്ത്": "Niyyat",
        "നിസ്കാരം": "Daily Prayer",
        "ഖിബ്ലാക്ക്": "Qiblah",
        "അദാആയി": "Ada'",
        "ജംഅ്": "Jam’",
        "ഇശാഉം": "Isha’",
        "മഗ്രിബ്": "Maghrib",
        "ലുഹ്റ്": "Dhuhr",
        "ഇശാ": "Isha'",
        "ഇഷാ": "Isha'",
        "ഇഹ്രാം": "Ihram",
        "തൽബിയത്ത്": "Talbiyah",
        "വസ്ത്രധാരണം": "Wearing Garments",
        "ഹറാമം": "Haram",
        "ശൃംഗാരം": "Flirting",
        "വേട്ട": "Hunting",
        "ഇബാദത്തുകൾ": "Acts of Worship",
        "സുന്നത്ത്": "Sunnat",
        "ഇഅ്തികാഫ്": "I’tikaf",
        "തഹിയ്യത്ത": "Tahiyyat",
        "നിയ്യത്തില്‍": "Niyyat",
        "ഹജ്ജ്": "Hajj",
        "ഉമ്ര": "Umrah",
        "ശുദ്ധി": "Purification",
        "ഇള്ത്തിബാഅ്": "Idhtiba’",
        "റമൽ": "Ramal",
        "ദിക്രുകൾ": "Adhkars",
        "റക्अത്ത്": "Rak'at",
        "ഉദ്ദേശ്യം": "Intention",
        "സunni": "Sunni",
        "സുന്നത്തം": "Sunnat",
        "നിർബന്ധം": "Obligation",
        "ഹിജ്റ്": "Hijr",
        "സലാം": "Salam",
        "സിയാറത്ത്": "Ziyarat",
        "സിയാറത്തും": "Ziyarat",
        "പ്രാർത്ഥനകൾ": "Prayers",
        "ഹംല": "Hamla"
    },
    "everyday_objects_and_persons": {
        "മുടി": "Hair",
        "മാതാപിതാക്കൾ": "Parents",
        "ഭാര്യ": "Wife",
        "മക്കൾ": "Children",
        "ഗുരുവര്യന്മാർ": "Teachers",
        "നഖം": "Nails",
        "മീശ": "Moustache",
        "താടി": "Beard",
        "കക്ഷരോമം": "Pubic Hair",
        "ഗുഹ്യരോമം": "Private Hair",
        "ശരീരം": "Body",
        "റൂം": "Room",
        "വാഹനം": "Vehicle",
        "യാത്രക്കാരൻ": "Traveler",
        "ഇമാമോട്": "Imam",
        "അസ്വരം": "Asr",
        "അസ്വറ": "Asr",
        "ചെരിപ്പ്": "Slippers",
        "ചരട്": "String",
        "മടമ്പ്": "Heel of the Foot",
        "ബെൽറ്റ്": "Belt",
        "ഷൂ": "Shoes",
        "വാച്ച്": "Watch",
        "ഉമ്മ": "Mother",
        "ഉപ്പ": "Father",
        "സഹോദരൻ": "Brother",
        "സുഗന്ധം": "Perfume",
        "വസ്ത്രം": "Clothes",
        "പച്ച ലൈറ്റ്": "Green Light",
        "ലൈറ്റുകൾ": "Lights",
        "പുരുഷന്മാർ": "Men",
        "വാതിൽ": "Door",
        "സ്ത്രീകൾ": "Women",
        "തൂണുകൾ": "Pillars",
        "വെളളപെയിന്റ്": "White Paint",
        "കാർപ്പെറ്റ്": "Carpet",
        "മിമ്പറ": "Mimbar",
        "പിതൃ": "Paternal",
        "രോഗി": "Patient",
        "സ്വഹാബിമാർ": "Sahabah",
        "ഇംറഉൽ ഖൈസ്": "Imru’ al-Qais",
        "കുല്സൂം": "Kulsum",
        "ഉംറ തുണി": "Umrah Garment",
        "സാദാ ഡ്രസ്സ്": "Casual Dress",
        "തൊപ്പി": "Cap",
        "തോർത്ത് മുണ്ട്": "Bathing Towel)",
        "ലുങ്കി": "Lungi",
        "ബ്രഷ്": "Brush",
        "സോപ്പ്": "Soap",
        "പേസ്റ്റ്": "Toothpaste",
        "പണ്ഡിത": "Scholar",
        "ഫാമിലികൾ": "Families"
    },
    "sacred_objects": {
        "سوُرَةُ الْكَافِرُونَ": "Surah Al-Kafirun",
        "سوُرَةُ اْلإخْلاَصْ": "Surah Al-Ikhlas",
        "മതാഫ്": "Mataf",
        "ഹജ്രുൽ അസ്വദ്": "Hajr al-Aswad",
        "കാബ്ബ്": "Ka'ba",
        "കാബ ശരീഫിന്റെ": "Ka'ba Sharif",
        "ഖുർആൻ": "Quran",
        "ഹജറുൽ അസ്വദ്": "Hajr al-Aswad",
        "സ്വഫാ": "Safa",
        "മർവ": "Marwa",
        "സ്വർണ പാത്തി": "Golden Spout",
        "ഹുജ്റ ശരീഫ": "Hujra Sharif",
        "ഖബർ ശരീഫ": "Qabr Sharif"
    },
    "revered_persons": {
        "അബയാർ അലി": "Abayar Ali",
        "സൈലുൽ കബീർ": "Saylul Kabir",
        "നൂഹ്": "Noah",
        "ഇബ്രാഹീം": "Ibrahim",
        "ഇസ്മാഈൽ": "Ismail",
        "നബി(സ)": "Prophet (S)",
        "ഹബീബ് മുത്ത് മുഹമ്മദ് മുസ്തഫാ(സ)": "Habib the Pearl Muhammad Mustafa (S)",
        "നബി": "Prophet",
        "റസൂലുല്ലാഹി": "Rasulullah",
        "അബൂബക്കർ": "Abu Bakr",
        "ഉമർ": "Umar",
        "നebi(സ)": "Prophet (S)",
        "ഉസ്മാനുബ്നു അഫ്ഫാൻ(റ)": "Uthman ibn Affan (R)",
        "സഅദുബ്നു മുആദ്(റ)": "Sa’d ibn Mu’adh (R)",
        "അബൂ സഈദിനിൽ ഖുത്രി(റ)": "Abu Sa’id al-Khudri (R)",
        "അബ്ദുറഹ്മാനുബ്നു ഔഫ്(റ)": "Abdurrahman ibn Auf (R)",
        "സഅദുബ്നു അബീവഖാസ്(റ)": "Sa’d ibn Abi Waqas (R)",
        "ഫാത്വിമ ബീവി(റ)": "Fatimah Beevi (R)",
        "ഇബ്റാഹീം(റ)": "Ibrahim (R)",
        "ഉമ്മുഖുൽസൂം(റ)": "Ummu Kulthum (R)",
        "സൈനബ്(റ)": "Zainab (R)",
        "ಆಯിഷ(റ)": "Aisha (R)",
        "ഹഫ്സ്വ:(റ)": "Hafsah (R)",
        "മാരിയഃ(റ)": "Maria (R)",
        "സൗദ(റ)": "Sauda (R)",
        "സൈനബ് ബിൻതു ജഹ്ഷ്": "Zainab bint Jahsh",
        "ഉമ്മുസലമ(റ)": "Ummu Salama (R)",
        "സഫിയ്യ(റ)": "Safiyyah (R)",
        "ജുവൈരിയ്യ(റ)": "Juwayriyya (R)",
        "ഉമ്മു ഹബീബ(റ)": "Ummu Habib (R)",
        "സൈനബ് ബിൻതു ഖുസൈമ(റ)": "Zainab bint Khuzaymah (R)",
        "ഹസൻ(റ)": "Hasan (R)",
        "റസൂലുല്ലാഹി(സ)": "Rasulullah (S)",
        "സയ്യിദു ശുഹദാഅ് ഹംസ(റ)": "Sayyid Shuhada Hamza (R)",
        "അബ്ദുല്ലാഹിബ്നു ജഹ്ശ്(റ)": "Abdullah ibn Jahsh (R)",
        "മിസ्अബ്ദु ഉമർ(റ)": "Mis’ab Umar (R)",
        "മഹാനുഭാവനായ ശമ്മാസ് ബ്നു ഉസ്മാൻ (റ)": "Respected Shammas ibn Usman (R)",
        "സ്വഹാബികളും": "Sahabah",
        "ജാബിർ(റ)": "Jabir (R)",
        "റസൂൽ കരീം(സ)": "Rasul Kareem (S)",
        "நബി(ச)": "Prophet (S)",
        "മുആദു ബ്നു ജബൽ": "Mu’ad ibn Jabal",
        "ಆയിഷ(റ)": "Aisha (R)",
        "ഇબ്റാഹീം(റ)": "Ibrahim (R)",
        
        
    },
    "instructive_language": {
        "നിർബന്ധം": "Obligation",
        "അനിവാര്യ": "Necessary",
        "നീക്കം ചെയ്യുക": "Remove",
        "മുറിക്കുക": "Chop",
        "വെട്ടുക": "Cut",
        "നന്നാക്കുക": "Fix",
        "വൃത്തിയാക്കുക": "Clean",
        "ഓതൽ": "Recite Quran",
        "ചൊല്ലുക": "Recite",
        "ഉപേക്ഷിക്കുക": "Abandon",
        "വർദ്ധിപ്പിക്കുക": "Increase",
        "പാടില്ല": "Not Allowed",
        "കരുതൽ": "Bear in Mind",
        "കരുതണം": "Bear in Mind",
        "നിർവ്വഹിക്കൽ": "Carry Out",
        "നിർവഹിക്കുക": "Carry Out",
        "കരുതുക": "Bear in Mind",
        "അവസാനിക്കാതിരിക്കുക": "Do Not Stop",
        "നിർവഹിക്കൽ": "Carry Out",
        "നിർവഹിക്കേണ്ടتمام": "To be Carried Out",
        "ഉപയോഗിക്കുക": "Use",
        "നിക്കൽ": "Stand",
        "ആദ്യം ചെയ്യേണ്ടത്": "First Task",
        "ഉണ്ടാവാതിരിക്കുക": "Do Not Have",
        "നടന്നു കൊണ്ടായിരിക്കുക": "Keep Walking",
        "നിസ്കരിക്കേണ്ടത്": "To be Prayed",
        "വിട്ടു കടക്കുക": "Pass Through",
        "നടത്തം ആരംഭിക്കുക": "Start Walking",
        "പൂർത്തിയാക്കുക": "Complete",
        "ശേഷമായിരിക്കുക": "Do After",
        "ചെയ്യൽ": "To Do",
        "ചെയ്യുക": "To Do",
        "ഉത്സാഹിക്കണം": "Encourage",
        "പറയണം": "Must Speak",
        "ശ്രദ്ധിക്കണം": "Must Pay Attention",
        "നിർക്കുമ്പോൾ": "While Standing"
    }
}


# -----------------------------
# 4. User selects entity category
# -----------------------------
entity_category = "revered_persons"  # change to desired category
category_data = data[entity_category]
translit_map = translit_maps[entity_category]

# -----------------------------
# 5. Flatten data into rows
# -----------------------------
rows = []
for entity_ml, info in category_data.items():
    entity_en = translit_map.get(entity_ml, entity_ml)
    
    # Handle 'sections' key if exists
    sections = info.get("sections") if isinstance(info, dict) and "sections" in info else []
    
    # Flatten nested dicts (ritual_concepts may have nested dict)
    if not sections and isinstance(info, dict):
        stack = [(info, [])]
        sections = []
        while stack:
            current, path = stack.pop()
            if isinstance(current, dict):
                for k, v in current.items():
                    stack.append((v, path + [k]))
            else:
                sections.append(".".join(path))
    
    parent_counts = Counter(get_parent(sec) for sec in sections)
    for parent, cnt in parent_counts.items():
        if parent in parent_label_map:
            rows.append({
                "entity_en": entity_en,
                "entity_ml": entity_ml,
                "parent": int(parent),
                "label": parent_label_map[parent],
                "count": cnt
            })

df = pd.DataFrame(rows)

# -----------------------------
# 6. Expand counts → dots with horizontal jitter
# -----------------------------
dots = []
for _, row in df.iterrows():
    for i in range(row["count"]):
        jitter = np.random.uniform(-0.25, 0.25)
        dots.append({
            "entity_en": row["entity_en"],
            "entity_ml": row["entity_ml"],
            "parent_jitter": row["parent"] + jitter,
            "parent": row["parent"],
            "parent_label": f"{row['parent']} {row['label']}"
        })

dot_df = pd.DataFrame(dots)

# -----------------------------
# 7. Y-axis ordering
# -----------------------------
entity_order = sorted(dot_df["entity_en"].unique())
dot_df["entity_en"] = pd.Categorical(dot_df["entity_en"], categories=entity_order, ordered=True)

# -----------------------------
# 8. Lines connecting same entity across sections
# -----------------------------
# Only entities with >1 mention
line_df = dot_df.groupby("entity_en").filter(lambda x: len(x) > 1)

# -----------------------------
# 9. X-axis order for level-1 sections
# -----------------------------
section_order = [f"{sec} {label}" for sec, label in zip(level1_section_ids, level1_translations)]

# -----------------------------
# 10. Dot raster chart
# -----------------------------
dots_chart = (
    alt.Chart(dot_df)
    .mark_circle(size=80)
    .encode(
        x=alt.X("parent_label:O", sort=section_order,
                axis=alt.Axis(title="Level-1 Section", titleFontSize=16, titleFontWeight="bold",
                              labelAngle=90, labelFontSize=14, labelFontWeight="bold")),
        y=alt.Y("entity_en:N", sort=entity_order,
                axis=alt.Axis(title=f"{entity_category.replace('_',' ').title()} (Transliterated)",
                              titleFontSize=16, titleFontWeight="bold",
                              labelFontSize=14, labelFontWeight="bold")),
        tooltip=["entity_ml", "entity_en", "parent_label"]
    )
)

# -----------------------------
# 11. Lines connecting dots (perfectly aligned)
# -----------------------------
lines_chart = (
    alt.Chart(line_df)
    .mark_line(color="red", opacity=0.7)
    .encode(
        x=alt.X("parent_label:O", sort=section_order),
        y=alt.Y("entity_en:N", sort=entity_order),
        detail="entity_en:N"
    )
)

# -----------------------------
# 12. Combine charts
# -----------------------------
final_chart = dots_chart + lines_chart
final_chart = final_chart.properties(
    width=2000,
    height=30 * len(entity_order),
    title=f"Dot Raster Plot of {entity_category.replace('_',' ').title()} Mentions"
)

# -----------------------------
# 13. Save chart
# -----------------------------
final_chart.save(f"{entity_category}_dot_raster.html")
print(f"✅ Saved as {entity_category}_dot_raster.html — open in browser to view.")
