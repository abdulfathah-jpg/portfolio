---
title: "Mapping Migrant-Pilgrim Mobilities: Proposal for Mini Project 2"
excerpt_separator: "<!--more-->"
categories:
  - project1
tags:
  - Projects
  - Machine Learning
  - Mini Project 2
image: images/hajj.png 
---

For my mini-project, I plan to explore the spatial and ritual mobility of Malayalee migrants in Saudi Arabia who participate in _hamlas_, informal pilgrimage agencies run by South Asian migrants themselves. This work grows out of my broader ethnographic thesis, which argues that contemporary Muslim pilgrimage is not only a nationalized, highly regulated mobility but also unfolds through expansive, historically rooted itineraries animated by migrant agency. Despite its spatial presence in a Salafi-regulated territory, these _hamlas_ articulate ideas of spatial and ritual/religious mobility that far exceed the parameters of Salafi religious norms or the infrastructural architecture of official government-recognized pathways.

<!--more-->

In this Digital Humanities Project, I use textual analyses and visual mapping of my data corpus, a pilgrim guidebook found in the ethnogrpahic field, to present a comprehensive picture of migrant pilgrimage mobility. It asks 1) What kind of places, routes, figures, emotional register, ritual concepts, instructive language, and religious objects figure in their mobility, and what is their prominence? 2) How may we visually present the mobility to chart its temporal and procedural flow and provide a narrative and experiential mapping of the guidebook. Wholly, the DH project aims at comprehensive digital mapping of this rich ethnographic document that speaks to my thesis arguments


## Data Corpus

The corpus for this research is an internal _hamla_ pilgrimage guidebook used by a particular migrant-run group. It’s a 40-page printed document in a structured layout, with white background, and in a booklet form. This guidebook is not publicly available: organizers deliberately keep it hidden to avoid scrutiny from Saudi authorities who may disapprove of its alternative ritual geographies. Written in Malayalam but littered with Arabic litanies, it contains brief instructions about routes, travel tips, ritual sites, detailed instructions on ritual acts, litanies, and supplication, and some unofficial ziyarah (visitation) practices within Mecca, Medina, and along the journey. The ethnographer has been able to scan the document from the field and compile it into a [PDF file](https://drive.google.com/file/d/1O-R-Gze3qLYc3g7K2bEmPZipYZDVAgRQ/view?usp=sharing).

![The _hamla_ guidebook]({{site.baseurl}}images/guidebook.jpeg)

## Output

The outputs of this DH workflow will include:

* A machine-readable and translated corpus of the Hamla guidebook
  
* Extracted and classified key entities, including revered persons, sacred objects, and spatial elements, everyday ritual items, ritual concepts, and affective or instructive language.
  
* Spatial mapping in QGIS visualizing pilgrimage sites, Miqats, and ritual paths, while Graphviz diagrams represent relationships between persons, objects, and ritual sequences.
  
* An interactive Twine project allows users to explore the pilgrimage journey step by step, including rituals, locations, and litanies.
   
* A glossary of technical terms in migrant pilgrimage

## Provisional Digital Workflow

I have designed a stepwise workflow to map and analyze the Hamla guidebook.

1) Digitization
   
*	Scanning: I used CamScanner, a free and easy-to-use mobile application, to scan each page of the guidebook.
  
*	OCR Conversion: The scanned images will be processed using the Tesseract OCR model via eScriptorium. This model supports both Malayalam and Arabic scripts.
  
*	The machine-readable output is then reviewed for accuracy, particularly in the case of multilingual text
  
2) Translation and Preprocessing
   
*	Translation Tools: For translating the Malayalam text to English, I use beginner-friendly options such as Google Translate and ChatGPT.
  
*	Cleaning: OCR errors, translation inconsistencies for technical terms, and page artifacts are corrected.
  
*	Segmentation: The text is divided into discrete units and regions (e.g., pre-departure, journey, travel instructions, litanies, rituals) for analysis.
  
* Translating before analysis ensures I can efficiently perform textual and visual analyses on English and Arabic while keeping the original texts for reference.
  
4) Textual Analysis Using OpenAI NER
   
*	Tool: OpenAI Named Entity Recognition (NER) in Python.
  
*	Process: The text will be processed through NER to extract and classify:
  
         1.	Names of revered persons – prophets, saints, or notable religious figures.
 	
         2.	Sacred objects, materials, and spatial elements – Hajar al-Aswad, green light, Rawdah carpet, etc.
 	
         3.	Everyday objects mentioned in rituals – personal items, tools, or offerings.
 	
         4.	Ritual concepts – Jam’, Qaṣr, Dhikr, Niyyah, Tawaf.
 	
         5.	Affective language – patience, fear, intention, belief, non-belief.
 	
         6.	Instructive language – forbidden, allowed, rewarding, beneficial, recommended.
 	
*	Output: Extracted entities are stored as JSON files and csv files for analysis, and are used for below processes with QGIS maps, Graphviz networks, and Twine flows for integrated, multi-modal visualization. A glossary will be created for technical terms related to pilgrimage, such as Mīqāt, Ihram, etc., with definitions.
  
4) Spatial Mapping

* Tool: QGIS will be used to map all the locations mentioned in the guidebook.
  
* Data Input: Place names (Miqats, Mazars, cities, other pilgrimage sites) found in json file are linked to geographic coordinates through dictionaries. Coordinates are accessed through Google Maps
  
*	Paths between locations and ritual movements are visualized, revealing patterns of pilgrimage flow and spatial relations.
  
6) Ritual and Network Visualization
   
*	Tool: Graphviz will be used to create flowcharts and network diagrams. Twine is used to create interactive, branching visualizations of the pilgrimage journey.
  
* Ritual Mapping in Graphviz: Diagrams represent ritual sequences (e.g., Tawaf → Sa’i → Jam’/Qaṣr → Dhikr). Links between revered persons, objects, and places are visualized to show relationships and interactions.
  
*	Twine Process: Each ritual step will become a node in Twine. Users can click through the nodes to explore the sequence of rituals, locations, and litanies.
  
* This will uncover patterns, experiential elements, and relational structures that are less apparent in text alone.

## Anticipated Challenges

1)	Multilingual Texts: The guidebook contains Malayalam interspersed with Arabic litanies. OCR processing may misread characters or diacritics, particularly for Malayalam text written in a particular context. This could introduce errors that propagate through the translation and NER steps.
   
2)	Translation Limitations: Automated translation tools like Google Translate and ChatGPT struggle with ritual-specific terminology, idiomatic expressions, and culturally embedded references. This will require manual verification to maintain semantic accuracy.
   
3)	Ambiguity in Ritual Terms and Entities: Names of revered persons, objects, and ritual concepts might be referenced in multiple ways or contextually. The same ritual might have different names or spellings in Malayalam and Arabic, which could challenge automated NER extraction
	
4)	Spatial Mapping: Some pilgrimage locations or unofficial ziyarah sites may not have exact geographic coordinates or may be difficult to locate. This limits the accuracy of the QGIS visualizations.
   
5)	Oversimplified Visualization:  The guidebook’s brief character leaves out several experiential elements and socio-political factors of the pilgrimage unanswered, and may require additional data mining from the ethnographic field. Depending solely upon the guidebook for visualization may simplify the complex pilgrimage experience of the migrants
   
6)	Data Privacy and Sensitivity: The guidebook is not publicly available and is deliberately hidden by organizers. Ensuring ethical handling, privacy, and security of the digitized corpus is critical.
