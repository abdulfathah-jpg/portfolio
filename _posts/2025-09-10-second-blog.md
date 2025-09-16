---
title: "al-Ṯurayyā Gazetteer and Geospatial Model of the Early Islamic World"
excerpt_separator: "<!--more-->"
categories:
  - project1
tags:
  - Synopsis
  - Gespatial Projects
image: images/romanov.png
---
Website: https://althurayya.github.io/#home

![a random image]({{site.baseurl}}images/Banner.png)

## Project Synopsis

The al-Ṯurayyā Project is a digital humanities initiative that provides a comprehensive gazetteer – a geographical dictionary – and a geospatial model detailing cartographic world of early Islamic world. The project draws on Georgette Cornu’s Atlas du monde arabo-islamique à l’époque classique: IXe-Xe siècles (Leiden: Brill, 1983) to create a database of over 2000 toponyms and route sections, coupled with a visual model to plot routes, itineraries, and networks of accessible places from each center. This ongoing project which began in 2013 and is hosted at the University of Vienna, is currently curated by Masoumeh Seydi of the University of Leipzig and Maxim Romanov of the University of Vienna. 

At the outset, the project involves remediation of a single historical source material in analog format - Cornu’s atlas - into structured data that is computationally tractable. This process required several complex modelling decisions and interpretative judgements including georeferencing the toponyms to modern coordinate systems using QGIS, metadata development, use of Python libraries such as fuzzywuzzy to match Arabic source records to entries in gazetteer, and most importantly, an unconventional transliteration scheme that is standardized using Python. Unlike more traditional transliteration that involves compound forms, the one-to-one letter representation used in al-Ṯurayyā is said to allow seamless conversion between the transliterated forms and the Arabic script. 

In the next stage of processing, complex machine learning methods, algorithmic tools, and modeling decisions are employed to visualize static geographic information as interactive networks. This primarily involved using the adjacency of route sections and place nodes, etc. to build network graphs of routes, calculating accessibility between major centers, applying algorithms such as Dijkstra to find shortest and optimal land paths, running JavaScript + Leaflet for interactive maps, and likely use of D3 for charts and panels. These processes involve intellectual models and cultural assumptions beyond simple automation, as for instance in the Dijkstra algorithm that is wired to find the shortest path with the highest number of stations and settlements along the way under the assumption that such paths are safer.  

Finally, the findings of the research are presented as a digital project that that could be easily accessed through databases like ‘Closing the Gap in Non-Latin-Script Data’ that commits themselves to OpenScience principles. The project hosts a website providing interactive maps and makes its datasets easily available for researchers through GitHub. This open format ensures that not only is the final project available for research and teaching, but that researchers could reuse and transfer the structured data using standardized JSON files and critically engage with each modelling decision. Besides a comprehensive visual map, the project website offers services such as a search panel where one could search for Arabic toponyms or its transliterated form, maps of provinces that uses specific color palette to identify route sections of and between provinces, a Pathfinding panel to model most optimal paths between two or more locations, and a Modeling panel to find the network of settlements reachable from a particular center. Further, tabs primarily serving developers on technical information on route sections and path analyses could also be found. Wholly, these three components involved in this Digital Humanities workflow aims to enrich our understanding of the spatial relationships, mobility, and connectivity that were central to the early Islamic world.
