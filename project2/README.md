
### The project2 folder contains a README file explaining the folder structure and other important category folders: Code, JSON corpus, and visualization.

A.	Code: The Code folder includes code written throughout the project. It is further divided into:

    1)	NER: includes all codes written for running NER on the annotated corpus text. It includes the following files:
        -	annotated_split_ner.py
        -	annotated_split_ner_2.py
        -	annotated_split_ner_3.py (The most updated script that is taken over to the next step)
    
    2)	Open_Route: includes all codes written from the NER output to produce the visual map using Open Route Services
        -	ner_for_route.py: Parses place names from the nested JSON for use as sequential place names
        -	route_coordinates_csv.py
        -	route_coordinates_csv_2.py: creates the latest csv file of place labels, section IDs for order, coordinates, and transliterated labels. The differently numbered files above show the previous updates.
        -	pygqis_shortest_path.py: attempted to build the shortest route through QGIS.
        -	open_route_service.py
        -	open_route_service_1.py
        -	open_route_service_2.py
        -	open_route_service_3.py
        -	open_route_service_4.py: This is the latest python code creating the visual map from the earlier csv. The differently numbered files above show the previous updates.

     3)	data_for_dot: Includes all codes for producing dot raster plots 
        -	inverted_index_frequencies.py
        -	inverted_index_frequencies_3.py: the latest code to parse each entity count and section info from aggregate entity categories in nested JSON.
        -	everyday_dot_raster_1.py
        -	everyday_dot_raster_2.py: latest code producing dot raster plot for everyday objects and persons. The differently numbered files above show the previous updates.
        -	instructive_language_dot_raster_1.py
        -	instructive_language_dot_raster_2.py: latest code producing dot raster plot for instructive language. The differently numbered files above show the previous updates.
        -	place_dot_raster_1.py
        -	place_dot_raster_2.py: latest code producing dot raster plot for place names. The differently numbered files above show the previous updates.
        -	revered_persons_dot_raster_1.py
        -	revered_persons_dot_raster_2.py: latest code producing dot raster plot for revered persons. The differently numbered files above show the previous updates.
        -	ritual_dot_raster_1.py
        -	ritual_dot_raster_2.py: latest code producing dot raster plot for ritual concepts. The differently numbered files above show the previous updates.
        -	sacred_objects_dot_raster_1.py
        -	sacred_objects_dot_raster_2.py: latest code producing dot raster plot for sacred objects. The differently numbered files above show the previous updates.
     
     4) data_for_stream: includes all codes for producing the streamgraph.
        -	section_category_counts.py: creates the code to find aggregate category counts by section.
        -	streamgraph_sections.py
        -	steamgraph_sections_wiggle.py
        -	steamgraph_section_altair.py: creates the latest streamgraph using aggregate counts using Altair. Previous files show previous attempts at streamgraph creation.

B.	JSON: includes all JSON output files produced during the project
     
     1)	ner_by_section_nested.json
     
     2)	ner_by_section_nested_3.json:  The finalized OpenAI NER output stored in a nested JSON. The differently numbered files above show the    previous outputs.
     
     3)	ner_with_route_data.json: JSON with place names parsed from primarily level one and level two headings.
     
     4)	section_entity_counts.json: JSON output with entity category counts in each section for stream graph.
     
     5)	entity_index.json
     
     6)	entity_index_3.json: JSON output with the count of every entity and sections for the dot raster plot. The differently numbered files above show the previous outputs.

C.	Corpus: The files in the Corpus folder relate to the data corpus of the Mini Project. It includes the following files:

     1)	corpus_raw.pdf: The pdf file of the data corpus scanned from the ethnographic field.
     
     2)	ocr_corpus_fathah.txt: The output text file from OCRing the pdf file using Google Docs.
     
     3)	ccr_corpus_manually_corrected.txt: The manually corrected version of the OCRed output.
     
     4)	 annotated_ocr_manually_corrected.txt: The final corpus text that is structurally annotated for use in the NER process.

D. Visualization: The files in the Visualization folder show all visualization outputs from the Project in HTML format.

     1)	pilgrimage_bus_walk_map.html: visual map of pilgrimage geography
     
     2)	streamgraph.html: stream graph of category counts
     
     3)	everyday_objects_and_persons_dot_raster.html: dot raster plot of everyday objects
     
     4)	instructive_language_dot_raster.html: dot raster plot of instructive language
     
     5)	place_names_dot_raster.html: dot raster plot of place names
     
     6)	revered_persons_dot_raster.html: dot raster plot of revered persons
     
     7)	ritual_concepts_dot_raster.html: dot raster plot of ritual concepts


