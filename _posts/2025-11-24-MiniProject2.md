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


For my mini-project, I plan to explore the spatial mobility of Malayalee migrant-pilgrims who participate in _hamlas_—informal pilgrimage agencies run by South Asian migrants in Saudi Arabia. This work grows out of my broader ethnographic thesis, which argues that contemporary Muslim pilgrimage is not only a nationalized, highly regulated mobility but also unfolds through expansive, historically rooted itineraries animated by migrant agency. By tracing the routes taken by these _hamlas_ and the ritual places they emphasize during Hajj and Umrah, I aim to visualize how migrant pilgrims move through, around, and sometimes beyond state-defined geographies.

<!--more-->

## Corpus and Data Sources

My corpus will be a patchwork of textual, oral, and spatial data. The most significant dataset is an internal hamla guidebook used by a particular migrant-run group. This guidebook is not publicly available: organizers deliberately keep it hidden to avoid scrutiny from Saudi authorities who may disapprove of its alternative ritual geographies. Written in Malayalam, but littered with Arabic littanies, it contains brief instructions about routes, ritual sites, and some “unofficial” _ziyarah_ (visitation) practices within Mecca, Medina, and along the journey. For this project, I will digitize selected sections and treat them as a private dataset.

To use the guidebook digitally, I plan to extract place names through Named Entity Recognition (NER). Because the text is in Malayalam, this will likely require transliteration into Latin script using a Malayalam transcription model, followed by manual verification to correct OCR. Extracted place names will then be mapped onto coordinates using GeoNames API or a custom gazetteer.

![The _hamla_ guidebook]({{site.baseurl}}images/guidebook.jpeg)

As a supplementary dataset, I will draw on my ethnographic interviews with _hamla_ participants, where they recount the places they visited during their journeys. These interviews will be transcribed into English so as to make them compatible with Python-based NER tools covered in class. Their descriptions will help fill gaps in the guidebook, especially regarding contemporary travel practices, routes, and shifting preferences.

I may also incorporate contextual secondary material, including GIS layers of Saudi road networks, publicly available coordinates for major sacred and logistical sites (such as the _Miqāts_, Mina, Arafat, and the Haram), and any GPS points recorded during earlier field visits.

## Analytical Goals

My overarching goal is to understand how migrant-pilgrims spatialize their religious journeys, and how these movements diverge from the national pathways through which modern pilgrimage is regulated.

A central task will be to map the routes taken by _hamlas_—including common bus routes from Riyadh to Mecca and Medina, variations in routes during Ramadan, Eid, or weekends, and how these routes intersect with different _Miqāts_ (ritual boundary stations). Plotting these paths with Plotly Express will help visualize the structure and rhythm of migrant pilgrimage mobility.

A second objective is to identify frequently mentioned sites. By extracting place names from the guidebook and interviews, I hope to learn which places receive most attention, what forms of religious or cultural significance they hold, and if certain sensitive or informal sites appear only in the guidebook and not in interviews due to surveillance concerns.

Finally, I aim to compare formal and informal ritual geographies. Mapping the data will show how migrants creatively configure the pilgrimage landscape through alternative routes, additional ziyāra (visits), and overlooked spaces. This in turn may illuminate the persistence of premodern “vector-based” logics of pilgrimage, especially of Miqāts within migrant practice today.

## Digital Methods

Drawing on techniques from class, I plan to use NER for place extraction, with off-the-shelf models for English interviews and a manually supported process for Malayalam text involving transliteration and heuristic tagging. Coordinates will be acquired from the GeoNames API or a merged gazetteer. I will clean the data by normalizing spelling variations across Arabic, Malayalam, and English forms. Spatial visualization will be done through Plotly Express. This will potentially layer different kinds of itineraries—weekend trips, Ramadan trips, five-day packages, etc

## Anticipated Challenges

Several methodological challenges shape this project. First, the Malayalam guidebook requires OCR or transcription before any analysis can be done, and Malayalam place names often diverge from Arabic endonyms. Since no major NER models are optimized for Malayalam, considerable manual correction will be necessary.

Second, the dataset I intend to have itself is partial and sensitive. Participants may avoid naming certain sites that Saudi authorities disapprove. The result is a selective dataset, and this selectivity must be acknowledged in the further analysis.

Third, place references may be ambiguous. Some sites are known by symbolic names or informal Malayalam nicknames, and many terms blend Malayalam, Arabic, and English influences.

Finally, there are ethical concerns surrounding the visualization of sensitive routes. Certain mapped paths could inadvertently expose informal pilgrimage practices. For this mini-project, I will anonymize or generalize sensitive sites and avoid including any information that could endanger migrant communities.
