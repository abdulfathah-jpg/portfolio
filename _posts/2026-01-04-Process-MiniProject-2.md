---
title: "Mini Project: On the Way"
excerpt_separator: "<!--more-->"
categories:
  - project1
tags:
  - Projects 
  - Machine Learning
  - Mini Project 2
image: images/hajj.png 
---

<!--more-->
 
For my mini-project, I am exploring the spatial and ritual mobility of Malayalee migrants in Saudi Arabia who participate in hamlas—informal pilgrimage agencies run by South Asian migrants themselves. My research asks: what places, figures, ritual concepts, emotional registers, instructive language, and religious objects shape their mobility, and how can this mobility be visually presented to narrate and map the pilgrimage experience?

## Data Corpus

The primary corpus is a 40-page internal hamla guidebook, written mostly in Malayalam with Arabic litanies interspersed. It documents alternative spatial geographies and ritual practices for Umrah that diverge from state-led pilgrimage pathways. The scanned PDF file was inconsistent in quality, requiring careful OCR and manual correction.

## OCR and Manual Correction

Since the corpus contains mixed Malayalam and Arabic content, OCR was a significant challenge:

* Tools tested: Tesseract, Google Lens, Google Docs

* Outcome: Google Docs OCR performed best overall, handling both scripts relatively well, though struggles arose when Arabic and Malayalam appeared on the same line.

* Issue: Colored pages (cover and introduction) prevented OCR; starting from the first monochrome text page resolved the problem

* Output: OCRed text saved as a text file

### Manual corrections were necessary:

* Spelling mistakes and missing characters where scripts co-occurred

* Reformatting Arabic lines to prevent confusion in text editors

* Correcting a missing heading

* All corrections done on a copy of the OCR file; the original was preserved for reference

The VC editor was used for further processing because it supports Python workflows and allows easier handling of two scripts, particularly for later JSON-based analysis.

## Annotation

Structural annotation followed [OpenITI Markdown guidelines](https://maximromanov.github.io/mARkdown/)

* Four heading levels and META annotation for front and backmatter applied

* Page numbers removed

* Paragraphs reformatted to one line each (required for Markdown)

* VC editor used instead of EditPad Pro due to Mac compatibility issues

At this stage, only structural annotation was applied

## Textual Analyses (also as data for further steps)

### Part A – Malayalam:

Extracted entities from Malayalam text only:

* Revered persons

* Place names

* Sacred objects and spaces

* Everyday objects and persons

* Ritual concepts

* Instructive language

### Part B – Arabic:

Extracted:

* Litanies, supplications, dhikr, and formulas for recitation

* Names of Qurʾānic sūras and verses explicitly instructed to be recited

Parsing was based on headings and subheadings to maintain the chronological sequence and procedural stages of the pilgrimage. Regex-based parsing supported multiple heading levels (###|, ###||, ###|||), keeping subsections nested and enabling section-wise NER extraction.

## Place-Name Extraction and Route Preparation (Pre-Visualization Step)

Before spatial visualization, I needed to extract place names in the correct pilgrimage order:

* Only headings and subheadings were used; text below headings was excluded to avoid complicating ritual-stage mapping.

* Start and end points were identified from front and back matter, annotated as meta.

* A Python script extracted place names from both headings and meta-text to construct ordered routes.

### Creating the JSON and CSV:

* A manual gazetteer (PLACE_COORDS) was defined, mapping each place name to latitude and longitude (sourced manually from Google Maps)

* Start locations and end locations inserted 

* Output: chronologically ordered pilgrimage route file (pilgrimage_route1.csv) including section_id, place_name, latitude, and longitude

### Encoding Challenges:

* Initial CSV showed garbled Malayalam text (mojibake)

* Cause: JSON in UTF-8 with potential BOM or hidden encoding issues

* Solution: wrote CSV using utf-8-sig to ignore BOM, ensuring Malayalam displays correctly in Excel and QGIS

This step ensured that the pilgrimage sequence was properly structured and ready for spatial mapping

## Spatialization and Flowing Map

### QGIS Attempt:

* Initial goal: represent real pilgrimage journeys respecting transport modes (bus and walking) and following roads

* Problems encountered:

          *  Road layers incomplete or polygonal, missing sacred spaces

          *  Pilgrimage locations not routable using standard GIS network data

* Routing tools required geometry corrections, snapping, and repeated shortest path calculations

* Conclusion: QGIS introduced overhead with limited analytical value

### OpenRouteService (ORS) implementation

Due to QGIS limitations I implemented OpenRouteService (ORS) for the pilgrimage map using free API avaialble from the site using github credentials.

* Input: chronologically ordered CSV of place names with coordinates

* Route computation handled multiple transport modes:

          * Driving → bus travel between cities

          * Foot-walking → ritual and mosque movement
  
* Output: Generated an interactive, animated [map](file:///Users/MAFmedia1/Downloads/DH25/project_2/pilgrimage_bus_walk_map.html) reflecting spatial and temporal pilgrimage flows
  
#### Tools Used:

          * Python for scripting API requests and data processing

          * ORS Python client to retrieve polylines following real roads and walkways

          * GeoJSON output for easy integration with mapping libraries

          * Folium library in Python for interactive map visualization

* Optimization: removed duplicate consecutive coordinates to prevent routing errors

#### Interactive Map Visualization in Folium:

* Markers for named pilgrimage locations, in narrative order

* Blue lines for bus routes along highways

* Green lines for walking paths within cities and ritual spaces

#### Animated travel simulation:

* Used Folium path-animation plugins such as AntPath and TimestampedGeoJson

* Routes are rendered as moving lines or time-indexed points along real roads

* Highlights mobility and transition as central elements of the pilgrimage experience, complementing the textual sequence of rituals

### Challenges Remaining:

* Walking and bus paths often run parallel; manual section range assignment  still need work

* Malayalam place names require transliteration for readability. This could be acheived through OpenAI translation endpoint (e.g., gpt-5-translate or gpt-5-xl)

## Planned: Pilgrimage Ritual Flow Diagram

The next stage focuses on ritual-temporal visualization:

         * Represent the Umrah journey as a linear or vertical flowchart showing stages in ritual order

         * Integrate entities extracted from text: section_id, headings, revered persons, place names, sacred objects and spaces, everyday objects and persons, ritual concepts, instructive language, arabic litanies and recitations
  
* Visual forms considered: Sankey diagram or vertical timeline
  
* Tools planned: Python libraries such as Matplotlib, Graphviz, or Plotly for creating flow diagrams
  
* Purpose: emphasize the pilgrimage as a ritually ordered process, not merely travel in space


