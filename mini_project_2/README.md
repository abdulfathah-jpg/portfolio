# Data Corpus: Guidebook

The corpus for this research is an internal hamla pilgrimage guidebook used by a particular migrant-run group. It is a 40-page printed document in a structured layout, with a white background, designed as a small booklet. This guidebook conveys an alternative spatial geography and ritual mobility for the Umrah pilgrimage that differs from the formal pathways cultivated through state-led initiatives in contemporary Saudi Arabia. Although these spatial geographies are not hidden or secret, the significance attributed to them and the ritual practices associated with them distinguish the migrant pilgrimage from the highly nationalized pilgrimage promoted today, placing the practices described in the guidebook in a contested relationship with official forms.

The guidebook is written primarily in Malayalam, but frequently interspersed with Arabic litanies. It contains brief instructions on travel routes, practical tips, key ritual sites, detailed ritual procedures, litanies, supplications, and some unofficial ziyarah (visitation) practices in Mecca, Medina, and along the journey. The ethnographer scanned the document in the field and compiled it into a [PDF](https://drive.google.com/file/d/1gNUacBtfslTS9T6VOrrqgxG4Z22oXvwe/view?usp=sharing). However, the scanning quality was inconsistent, which is a significant factor when aiming for optimal OCR accuracy. However, considerable effort will go in the next weeks into extracting higher-quality images in preparation for final processing.

## Structure of the Data Corpus

The guidebook is arranged according to the successive stages of the Muslim Umrah as practiced among migrants, moving from the earliest preparations to the concluding steps. A preliminary outline of its structure is as follows:

* Cover page
  
*	Details of the hamla group that compiled the guidebook
  
*	Brief discussion of the concept and rewards of Umrah
  
*	Pre-departure rituals
  
*	Departure procedures and associated infrastructure
  
*	The concepts of Jam‘ and Qaṣr (ritual practices associated with Muslim travel)
  
*	Mīqāt (boundary points where pilgrims formally enter the state of ritual consecration)
  
*	Masjid al-Haram and the rituals associated with it (Tawaf, Sa‘y, etc.)
  
*	Detailed litanies associated with each circumambulation of the Kaaba
  
*	The Prophet’s Mosque in Medina
  
*	Other sites of ziyarah (visitation)
  
*	Key adhkār related to travel and Umrah
  
*	List of recommended personal items for the journey
  
*	Advertisements for services offered by the hamla group

The structured format, with clearly specified headings marking successive ritual stages, makes the corpus highly suitable for systematic textual analysis.

## Sample OCR: Google Docs

Because the corpus contains both Arabic and Malayalam, and because Malayalam remains only partially supported in many Digital Humanities tools, the OCR process is a significant challenge. Both languages frequently appear within the same line and complicate the transcription. Three OCR pathways were tested as potential candidates: Tesseract, Google Lens, and Google Docs. Trial runs on a few pages indicated that Google Docs’ automatic transcription produced relatively better accuracy across both scripts. It handled Arabic and Malayalam relatively well, but struggled when both scripts appeared in the same line. This will require later manual correction.

The entire corpus was therefore processed through Google Docs OCR, and the output was saved as a [text file](https://github.com/abdulfathah-jpg/portfolio/blob/master/mini_project_2/ocr_data_corpus_fathah.txt). However, a notable problem emerged in the process: when the PDF began with the coloured cover page and coloured hamla introductory page, Google Docs failed to OCR the entire document. This appears to be because Google’s OCR pipeline classifies heavily coloured or graphic pages as non-textual and therefore deems the entire PDF unsuitable for OCR. Removing the color pages and beginning OCR from the first monochrome text page resolved the issue. The cover and first page, therefore, remain non-OCRed at the present sample stage.

## Sample Textual Analyses

A key objective of Mini Project 2 is to conduct textual analysis using OpenAI’s NER capabilities to extract and classify the following:

1.	Names of revered persons: prophets, saints, or notable religious figures.
   
2.	Sacred objects, materials, and spatial elements: e.g., Hajar al-Aswad, green light, Rawdah carpet.
   
3.	Everyday objects mentioned in ritual contexts: personal items, tools, offerings.
   
4.	Ritual concepts: Jam‘, Qaṣr, Dhikr, Niyyah, Tawaf, etc.
   
5.	Affective language: patience, fear, intention, belief, doubt.
   
6.	Instructive language: forbidden, allowed, rewarding, beneficial, recommended.

The outputs of these analyses can then be stored as JSON and CSV files for further processing, including spatial and ritual mapping using QGIS and other visualization tools.

To test the corpus’s suitability, a sample NER task was run using OpenAI to extract ritual concepts and place names from the Malayalam-language portions of the text (Arabic sections largely consist of litanies and are less relevant for this analysis). The model was instructed to count each occurrence. The following code was used:

### Code for Textual Analyses:

```yaml
from openai import OpenAI
import getpass
my_api_key = getpass.getpass("Please past your key here: ")
client = OpenAI(api_key = my_api_key)

prompt = """You are an expert in Muslim Hajj pilgrimage practice and Malayalam–Arabic devotional guidebooks.
You will receive a text containing Malayalam and Arabic script.  
Your tasks:
1. Extract each and every possible ritual concepts appearing in the Malayalam portions of the text.
2. Extract each and every possible place names appearing in the Malayalam portions of the text.
Examples of ritual concepts (not exhaustive):
തവാഫ്, ഉംറ, ഇഹ്‌റാം, നിസ്കാര, ളുഹ്റ്, ദുആ, സിയാറ, etc.
Examples of place names (not exhaustive):
മക്ക, മദീന, ജന്നത്തുല്‍ ബഖീ, അറഫാ, മിന, ഹറം, etc.

Important rules:
1. Return results only in JSON
2. The JSON must contain exactly two keys:
   - "ritual_concepts": a python list of ritual words/phrases (preserve original script i.e., Malayalam).
   - "place_names": a python list of place names (preserve original script i.e., Malayalam).
3. Each occurrence should be listed separately (if a ritual concept or place name appears 5 times, include them as separate entries 5 times).
4. When a ritual concept or place name appears inside a longer phrase (e.g., because of grammar, inflection, or additional context), list it in the correct noun form as a separate entry.
5. Normalize Malayalam spelling variants and OCR-damaged variants where meaning is still clear.
6. Do not translate or explain. Only extract and normalize all mentions

Text:
"""

input_file = "/Users/MAFmedia1/Downloads/DH25/ocr_data_corpus_fathah.txt"
output_file = "/Users/MAFmedia1/Downloads/DH25/openai_output_fathah.txt"

with open (input_file, mode="r", encoding="utf-8") as file:
    text = file.read()
    
print(f"Processing {input_file} ...")

response = client.responses.create(
    model="gpt-5-nano",
    input = prompt + text
    )

data = eval(response.output_text)
ritual_concepts = data["ritual_concepts"]
place_names = data["place_names"]

print(ritual_concepts)
print(place_names)
print(f"\nDone! Extracted two separate lists saved to {output_file}")

ritual_counts = {} 

for ritual in ritual_concepts:
    if ritual not in ritual_counts:
        ritual_counts[ritual] = 1
    else:
        ritual_counts[ritual] += 1

print (ritual_counts)

place_counts = {}

for place in place_names:
    if place not in place_counts:
        place_counts[place] = 1
    else:
        place_counts[place] += 1
        
print(place_counts)
```

## Efficiency of the Sample Textual Analysis

The model successfully produced two separate lists of ritual concepts and place names, and calculated their frequencies:

```yaml
Processing /Users/MAFmedia1/Downloads/DH25/ocr_data_corpus_fathah.txt ...
['ഉಂറ', 'ഇഹ്റാം', 'ത്വവാഫ്', 'സഹാ മർവ', 'മുടി എടുക്കൽ', 'നിസ്കാരം', 'ഖസ്വ്റും', 'മീഖാത്ത്', 'ദുആ', 'വദാഇന്റെ', 'സ്വഫा മർവ', 'സംസം', 'സിയാറ', 'ഹജ്ജ്']
['അൽഖുദ്സ്', 'ICF റിയാദ്', 'മക്ക', 'മദീന', 'ബൈത്തുൽ മുഖദ്ദസിലേക്ക്', 'മസ്ജിദുൽ ഹറാം', 'മസ്ജിദുന്നബവി', 'റൗളા ശരീഫ്', 'ജന്നത്തുൽ ബഖീ', 'ഉഹ്ദ്', 'മഖാമു ഇബ്രാഹീം', 'സ്വഫാ', 'മർവ', 'മസ്ജിദുൽ ഖുബാഅ്', 'മസ്ജിദുൽ ഖിബ്ലതൈന']

Done! Extracted two separate lists saved to /Users/MAFmedia1/Downloads/DH25/openai_output_fathah.txt
{'ഉಂറ': 1, 'ഇഹ്റാം': 1, 'ത്വവാഫ്': 1, 'സഹാ മർവ': 1, 'മുടി എടുക്കൽ': 1, 'നിസ്കാരം': 1, 'ഖസ്വ്റും': 1, 'മീഖാത്ത്': 1, 'ദുആ': 1, 'വദാഇന്റെ': 1, 'സ്വഫा മർവ': 1, 'സംസം': 1, 'സിയാറ': 1, 'ഹജ്ജ്': 1}
{'അൽഖുദ്സ്': 1, 'ICF റിയാദ്': 1, 'മക്ക': 1, 'മദീന': 1, 'ബൈത്തുൽ മുഖദ്ദസിലേക്ക്': 1, 'മസ്ജിദുൽ ഹറാം': 1, 'മസ്ജിദുന്നബവി': 1, 'റൗളા ശരീഫ്': 1, 'ജന്നത്തുൽ ബഖീ': 1, 'ഉഹ്ദ്': 1, 'മഖാമു ഇബ്രാഹീം': 1, 'സ്വഫാ': 1, 'മർവ': 1, 'മസ്ജിദുൽ ഖുബാഅ്': 1, 'മസ്ജിദുൽ ഖിബ്ലതൈന': 1}
```

A comparison with manual evaluation revealed two limitations:

1.	While major instances were captured, not all ritual concepts or place names were extracted.
   
2.	The model did not consistently recognize multiple occurrences of the same term.

This limits the ability to measure prominence or frequency, which is important for mapping emphasis in ritual discourse.

Nonetheless, categorization and classification were broadly accurate: extracted items were correctly sorted into “ritual concepts” and “place names.” This means that further classification of these categories, for instance, the rituals into particular kinds, might produce more fuller list of ritual concepts. Moreover, in this sample run, OpenAI NER was applied directly to Malayalam without first translating the OCR output. Translating the text into English may improve consistency, but this would need significant manual correction after running it through Google Translate and OpenAI translation.

## Conclusion 

The Data Corpus is finite, structured, already collected, and is therefore well-suited for textual analysis. But several challenges remain: Scanning quality has to be improved, OCR quality is uneven, Malayalam-Arabic mixed lines require manual correction, and translation may be necessary for improved computational processing. A key obstacle is segmentation because Google Docs OCR does not support dividing the text according to the guidebook’s ritual-stage headings, and pre-OCR segmentation would complicate maintaining a reliable link between segments and their later translations. Given the short length of the corpus, the most effective solution is to manually add structural annotation after OCR using a lightweight schema such as OpenITI Markdown so that the text can be programmatically segmented in Python. In this way, ritual concepts, place names, and other extracted entities can be accurately mapped to their corresponding ritual stages for subsequent analysis and visualization of the pilgrimage 

