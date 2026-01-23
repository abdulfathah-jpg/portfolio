---
title: Migrant Pilgrimage
permalink: /migrantpilgrimage/
layout: page
image: images/Digitization.jpg
---

<!--more-->


This Mini Project explores the spatial and ritual mobility of Malayalee migrants in Saudi Arabia who participate in hamlas, informal pilgrimage agencies run by South Asian migrants themselves. This work grows out of my broader ethnographic thesis, which argues that contemporary Muslim pilgrimage is not only a nationalized, highly regulated mobility but also unfolds through expansive, historically rooted itineraries animated by migrant agency. Despite its spatial presence in a Salafi-regulated territory, these hamlas articulate ideas of spatial and ritual/religious mobility that far exceed the parameters of Salafi religious norms or the infrastructural architecture of official government-recognized pathways.

# Research Questions

This project takes up three significant questions:
1.	How does an Umrah guidebook produced by Malayalee migrants in the Gulf construct an alternative spatial geography of Umrah pilgrimage outside state-mandated geography?
2.	What ritual, spatial, and religious elements are prominent in the guidebook? How are they distributed across different sections of the guidebook? What does this tell us about the significance of certain individuals, places, and language in the migrant pilgrimage?
3.	How do different entities, such as sacred places and revered persons, relate to one another, and what networks or clusters emerge from these relationships?

# Data Corpus

The corpus for this project is an internal hamla pilgrimage guidebook used by a particular Malayalee migrant-run group in Riyadh. It is a 40-page printed document in a structured layout, with a white background and designed as a small booklet. The guidebook is written primarily in Malayalam but is also frequently interspersed with Arabic litanies. It includes brief instructions on travel routes, practical tips, key ritual sites, detailed ritual procedures, litanies, supplications, and some unofficial ziyarah (visitation) practices in Mecca, Medina, and along the journey. The ethnographer scanned the document in the field and compiled it into a PDF. However, the scanning quality was inconsistent due to ethnographic limitations and had implications for optimal OCR accuracy.
The guidebook is arranged according to the successive stages of the Muslim Umrah as practiced among migrants. In that instance, the sections of the Guidebook move successively through details of the hamla group, discussion of the concept and rewards of Umrah, pre-departure rituals, concepts of Jam‘ and Qaṣr (ritual practices associated with Muslim travel), Mīqāt (boundary points where pilgrims formally enter the state of ritual consecration), Masjid al-Haram and the rituals associated with it (Tawaf, Sa‘y, etc.), litanies associated with each circumambulation of the Kaaba, description of the Prophet’s Mosque in Medina, other sites of ziyarah (visitation), ley adhkārs related to travel, list of travel items to be taken along the journey, and concludes with advertisements on the hamla group. This structured format, with clearly specified headings marking successive ritual stages and places, makes this corpus very much suitable for systematic textual analysis.

## Step 1: Optical Character Recognition (OCR) and Annotation

Three methodological challenges had to be addressed with regard to the structure of the corpus: 1) standard OCR tools struggle in dealing with mixed script texts, particularly if they are on the same line; 2) the ethnographic setting only allows modest scanning techniques and limited time which leads to compromises on clarity that would impede OCR accuracy; 3) As noted, the guidebook’s procedural stages are nested logically inside its structure, but this nested structure must be reconstructed digitally.

### OCR Process & Rationale

For OCRing the text corpus, we tested three tools: Tesseract, Google Lens, and Google Docs. It was concluded that Google Docs OCR provided the best performance for mixed Malayalam and Arabic scripts. There were certain issues that remained after the first process. Coloured pages of the front and back cover failed the OCR process, so the processing was restarted from the first monochrome page. Moreover, manual correction was essential for fixing spelling, missing characters where scripts co-occurred, and reformatting Arabic lines. However, the original OCR output was preserved for reference.

### Structural Annotation

The structural annotation of the OCR corpus was done using OpenITI Markdown guidelines for structuring the raw text. These annotations applied four heading levels (e.g., `### |`), META tags for front/back matter, and paragraphs were flattened to one line each.

From this process onwards, the project used Visual Studio Code due to its robust Python workflow integration and superior handling of bilingual text compared to other editors.

## Step 2: Reconstruct Text Hierarchy with a Stack-Based Parser

The problem at this stage is how to transform a flat list of headings (`### |`, ### | |`) into a meaningful, nested tree structure that reflects the pilgrimage's procedural stages. The solution was to use a stack-based approach that processes the document line-by-line, tracking the current heading level.

Whenever Python encounters a new heading, if it is deeper (e.g., ### || after ### |`), it's nested as a child. If it is at the same level as before, the previous sibling node is closed. If it is shallower than before, the parser climbs up the tree and closes child and parent nodes. This technique, which is usually used in compilers and XML tokenizers, allows us to create a clean semantic tree rather than a flat list. 

heading_match = re.match(r'^(###\s+(\|+))\s*(.*)', line)

## Step 3: Enriching the Text with Named Entity Recognition

The parsed hierarchical structure in the above step allows for recursive, section-level analysis. Using this structure, the text of each section and subsection was sent to an OpenAl model. A domain-specific prompt was then sent to the model to extract entities into predefined categories, and the structured JSON output was attached back into the hierarchical document.

The Entity Categories extracted for the Malayalam portion of the text were: Revered Persons, Place Names, Sacred Objects, Everyday Objects, Ritual Concepts, Instructive Language

The Entity Categories extracted for the Arabic portion of the text were: Litanies & Recitations

The prompt was constantly updated to provide the best NER result. For instance, this involved 1) listing the Arabic task and Malayalam task separately as Part A and Part B, 2) providing conditions such as to list every entity in its unified noun form (despite appearing different inside phrases due to grammar, inflection, etc) to aggregate the same entities, 3) asking to preserve original script in the JSON result, etc. 

The resultant JSON file showed heading title, heading level, and the whole text under each heading, section id, and entity types. The information, for instance, the small texts now available to read under each heading, was useful to spot-check the performance accuracy of the NER 

# Visualizing Pilgrimage Journey

The objective here was to transform a linear, textual account of a sacred pilgrimage in the guidebook into an interactive, geographically accurate, and chronologically coherent digital map. A key challenge was also that the text provides the sequence of places, but not a ready-made geographic path or mode of travel. So, this step involved creating a self-explanatory and shareable visualization that brings the life journey.

### Choosing the Right Tool for the Terrain

This visualization was first attempted through QGIS. However, this created several problems: the road layers were often polygonal or missing crucial segments, the sacred spaces were not routable since QGIS lacked the required network data, and complex geometry corrections and calculations were constantly required. It was thus concluded that QGIS introduced overhead with limited analytical value

## The Breakthrough (OpenRouteService)

Open Route Services allowed a breakthrough with its free API key available to GitHub users. It allowed automated, realistic routing along roads and walkways, and handled multi-modal travel (driving and walking). An interactive and animated spatial geography of migrant pilgrimage was thus achieved through a combination of Python libraries, including Folium, and plugins such as AntPath

### Structured Data

Before the visualization could be attempted through OpenRouteServices, the place names had to be extracted into structured data. Key locations were identified from the text's headings and subheadings to map the primary stages of the ritual. The text inside these chosen one-level and two-level headings was excluded so that place mentions that come as a result of further descriptions do not complicate the spatial order. Secondly, a manual Gazetteer has to be created for Geocoding, and a PLACE_COORDS dictionary was built by manually sourcing latitude and longitude for each key site from Google Maps. Finally, the nested text structure was flattened into a clean CSV with columns: 'section_id', 'heading', 'place_name', 'latitude', 'longitude'.The initial data was in Malayalam. A challenge faced during the production of CSV was that the final file produced Malayalam text as garbled text (mojibake). The utf-8-sig was used to solve the issue by preserving Unicode and handling the BOM. For accessibility, all place names were manually transliterated into English for map labels and popups. 

# Animated Map 

The animated map was produced using Open Route Services and showed the pilgrimage journey starting from Riyadh and passing successively through the Miqat of Qarn Manazil, the Haram and Ka’ba in Makkah, the Prophet’s Mosque in Medina, Jannat Al-Baqi’, the sites of Uhud, Masjid al-Fath, Masjid al-Qiblatain, Masjid al-Quba, and returning to Riyadh. 

Key design features in the Map included Blue Routes ('bus travel) animated with higher speed to represent intercity travel, Green Routes ('walk travel) animated more slowly to reflect ritual walking in sacred areas. This was outside the scope of the corpus and was achieved through ethnographic knowledge, by which the researcher manually added ranges of sections travelled through by bus or on foot. The map also had hierarchical Labels which showed major locations in large, bold labels, while minor sites had smaller, gray labels to reduce clutter while retaining information.

# Pipelines for Temporal and Structural Visualization

We developed two parallel visualization tracks to move from spatial to structural analysis, and each served a distinct analytical purpose.

A Streamgraph in ThemeRiver showing aggregated frequencies of entity categories across textual sections. It is intended to answer the prominence of categories of entities across the text and reveal their change across the flow of the text and successive pilgrimage stages. 

The Dot Raster Plot involved five separate plots of individual entity mentions, and preserved sparseness and variation across each element in the entity. It was intended to show which element contributed to the prominence of each category and in which sections they were distributed.

## Streamgraph: From Nested JSON to a Plot-Ready Long-Form Table

A Python script was required to parse aggregate counts of each category per section from the nested tree-structure JSON file and create a long-form Data Frame. A recursive function flattens the tree into the section_entity_counts.json format. To prevent lexicographical sorting errors (e.g., '10.3.2' appearing before '2.1.1'), section IDs were converted from strings to numericals for correct sorting.

For example: "10.3.2" to (10, 3, 2)

A long-form Data Frame with rows of (section_id, category, count), as it is the required format for plotting libraries.

# Interactive Streamgraph

### Visualization Code & Rationale

mark_area(interpolate="basis") was critically important for converting jagged steps into smooth, aesthetically pleasing curves.

stack="center"" creates the centred 'ThemeRiver' baseline as an alternative to standard wiggle algorithms.

Tooltips were enabled for interactive exploration of the data points. The unreadable axis labels were solved through Label rotation + width=2000, and the missing semantic context was dealt with by adding Level-1 translated labels into X-axis

The resulting HTML output was a smooth, interactive ThemeRiver streamgraph that enabled macro-level interpretation of how category prominence shifts across the narrative.

# Visualizing Every Single Mention with Dot Raster Plots

Dot Raster plots were specifically chosen because they handle sparse data: Unlike aggregated views, dot plots represent every single entity mention. This is crucial for rare entities that appear only once or twice and will ensure that they are not lost. The plot will also show the precise distribution of which entities appear in which sections without aggregation. This will reveal patterns of concentration and scarcity.

The choice also involved methodological consistency in that the same visualization structure can be applied across all entity types for easy comparison. The Python code used only required a change to the desired entity category to apply the visualization to all entity types (For instance, entity_category = "place_names")

### Processing Steps for Granular Entity Representation

The first step involved parsing from the nested original JSON file another JSON structured as: 'category→ entity→ [list of section IDs], i.e., entity_index_3.json. The particular JSON was loaded, and elements were manually transcribed and transliterated. The manual approach avoids semantic errors from automated tools, ensures ethnographic accuracy, and consistently collapses inflectional variants (e.g., different forms of the same name). Thirdly, Level-1 Sections were extracted so that we could simply section IDs for aggregation (e.g., "10.3" →"10").  Aggregate counts were found using a Counter for each entity within the broader Level-1 sections. The counts were then, finally, expanded into Dots and created a data point for each individual mention. A small amount of horizontal jitter to prevent dots from perfectly overlapping.

The tools used included Pandas for data shaping and manipulation, NumPy for calculating jitter offsets, and Altair for interactive plotting.

The design choices involved increasing dot size (mark_circle (size = 180), and adding more visible red/rose colour range showing prominence in a single section

All categories (Place names, Ritual concepts, Sacred objects, Revered persons, Everyday objects/persons) were visualized except Arabic litanies, which were excluded from visualization due to their length and extreme sparsity, which are not useful for further analyses

## Two Additions to Usual Dot Raster Plots

The Dot Raster plot was modified by two additions: a summary panel and a line connecting entities across sections. 

The summary panel of top entities makes it easier to answer “what is prominent” without manually counting dots

The red lines behind dots for entities with >1 mention help us trace distribution patterns for a given entity across multiple sections

line_df = dot_df.groupby(...).filter(lambda x: len(x) > 1)

# Findings

Due to the limited scope of this Mini Project, this blog intends to answer the second question raised in the beginning, i.e.,

What ritual, spatial, and religious elements are prominent in the guidebook? How are they distributed across different sections of the guidebook? What does this tell us about the significance of certain individuals, places, and language in the migrant pilgrimage?
This will be attempted by combining macro-patterns and micro-details as visualized through Streamgraph and Dot Raster Plots. The high-level ‘weather patterns’ offered by streamgraph could be fruitfully related to the microscopic details offered by  Dot Raster Plots.

It is evident from the streamgraph that the sections of the pilgrimage guidebook could be understood as a tripartite structure involving Preparation Phase (early sections), Ritual Performance Phase (middle sections), and Remembrance and Reflection Phase (final sections). It reifies our hypothesis that the guidebook is thus organized as a ritual lifecycle rather than as a narrative or thematic encyclopedia of the Umrah pilgrimage. The concentration of entities related to everyday objects, instructive language, and ritual concepts in the Preparation Phase suggests a strong emphasis on bodily discipline and readiness before embarking on primary rituals. The ritual performance stage shows a high concentration of ritual concepts, but also place names, the continued presence of instructional language, and a slow increase in mention of sacred objects. Arabic litanies appear as long, lone entities and indicate long moments of heightened recitations without social interruptions. The remembrance phrase shows a decline in ritual concepts and instructive language, and a marked increase in mention of revered persons and sacred objects. This shows a stage in which attention shifts to emotional engagement with sacred history. 

•	Ritual concepts are evenly distributed, but as expected, there are repeated mentions of ihram, niyyat, rakaʿat, sunnat, and umrah, and a high concentration in Jamʿ & Qasr and Tawaf sections. While these points suggest ritual intensity, overall ritual could be framed as a condition of the guidebook, rather than as an event
•	The distribution of Arabic litanies indicates long moments when sacred speech is a requirement, and they function as ritual punctuations rather than narrative content in the guidebook.
•	Different singularly mentioned place names are concentrated in sections on Miqat and Mazarat (sites of visitation), while there is frequent mention across the text of Masjid al-Haram, Safa, and Marwa. 
•	Among the Revered Persons, the Prophet’s name is mentioned for a disproportionate seventeen times (seconded by Ibrahim, mentioned three times) and is evenly distributed. This shows the inextricability of the individuals, particularly the prophetic exemplar, as the structuring feature of pilgrimage in the vision of Malayalee migrants as a predominantly Sunni-Sufi community. The high concentration of revered persons at sections on Jannat al-Baqi’ and Mazarat further reifies this hierarchy of religious memory. The absence of revered persons, mostly from procedural and ritual sections, additionally shows how personalities function less as legal authorities and more as objects of remembrance in this text
•	The domination of instructional terms like obligation, recite, to do, bear in mind, carry out, and its concentration primarily in the Preparation section, and secondarily in Tawaf and Sa’y sections, suggests that guidebook’s authority is expressed primarily through imperative language. It is particularly concerned at discipline of pilgrims as they depart and with errors that are bound to invalidate the ritual.
•	A high concentration of everyday objects in the Items to Keep in Travel section is expected. The largest count for Hair might indicate its seamless presence not just in travel-related matters, but also primarily in the pilgrimage ritual of removing hair. 
