from qgis.core import QgsProject, QgsProcessingFeatureSourceDefinition
import processing

# --- INPUT LAYERS ---
network_layer = QgsProject.instance().mapLayersByName("highway_lines")[0]  # your road network
points_layer = QgsProject.instance().mapLayersByName("snap_geometry_layer")[0]  # snapped points

# --- SORT POINTS BY section/order ID ---
points = [f for f in points_layer.getFeatures()]
points_sorted = sorted(points, key=lambda f: f['section_id'])  # make sure 'section_id' exists

# --- OUTPUT ---
output_lines = []

# --- LOOP THROUGH POINT PAIRS ---
for i in range(len(points_sorted)-1):
    start_feat = points_sorted[i]
    end_feat = points_sorted[i+1]

    params = {
        'INPUT': QgsProcessingFeatureSourceDefinition(network_layer.id(), True),
        'START_POINT': start_feat.geometry().asPoint(),
        'END_POINT': end_feat.geometry().asPoint(),
        'STRATEGY': 0,  # shortest path
        'TOLERANCE': 10,
        'OUTPUT': 'TEMPORARY_OUTPUT'
    }

    result = processing.run("native:shortestpathpointtopoint", params)
    output_lines.append(result['OUTPUT'])

# --- MERGE ALL SEGMENTS INTO ONE LAYER ---
merge_params = {
    'LAYERS': output_lines,
    'CRS': network_layer.crs(),
    'OUTPUT': '/Users/MAFmedia1/Downloads/DH25/project_2/pilgrimage_route_final.gpkg'
}

processing.run("native:mergevectorlayers", merge_params)

print("✅ Continuous road-following line created: pilgrimage_route_final.gpkg")
