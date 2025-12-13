import sys, os
import geopandas as gpd
import pandas as pd
import qgis
import qgis.core
from qgis.core import *
#QgsVectorLayer, QgsApplication, QgsFeature, QgsGeometry, QgsPointXY, QgsCoordinateReferenceSystem, QgsFeatureRequest
import sys,os
from PyQt5.QtWidgets import QApplication, QMainWindow, QStyle, QFileDialog, QDialog, QMessageBox, QSizePolicy
from PyQt5.QtGui import QStandardItemModel, QStandardItem,  QDoubleValidator, QIntValidator
from PyQt5.QtCore import Qt

app = QApplication(sys.argv)
qgis_prefix = os.getenv("QGIS_PREFIX_PATH")
qgis.core.QgsApplication.setPrefixPath(qgis_prefix, True)
qgs = qgis.core.QgsApplication([], False)
qgs.initQgis()

sys.path.append(os.path.join(qgis_prefix, "python", "plugins"))
import processing
from processing.core.Processing import Processing
Processing.initialize()
# qgis.core.QgsApplication.processingRegistry().addProvider(qgis.analysis.QgsNativeAlgorithms())

# HARDCODED INPUT FILES
buildings = r"C:\Users\Sarah\Documents\GitHub\geog489-final\buildings.gpkg"
roads = r"C:\Users\Sarah\Documents\GitHub\geog489-final\denver_streets.gpkg"
tree_cover = r"C:\Users\Sarah\Documents\GitHub\geog489-final\tree_canopy.gpkg"
pop_density = r"C:\Users\Sarah\Documents\GitHub\geog489-final\denver_popdensity.gpkg"
transit_stops = r"C:\Users\Sarah\Documents\GitHub\geog489-final\bus_stops.gpkg"
existing_pantries = r"C:\Users\Sarah\Documents\GitHub\geog489-final\pantries.gpkg"

# Create QGIS Vector Layers - we might want to create a class for this where we can check if the layer is valid
buildings_layer = qgis.core.QgsVectorLayer(buildings, "Buildings", "ogr")
roads_layer = qgis.core.QgsVectorLayer(roads, "Roads", "ogr")
tree_cover_layer = qgis.core.QgsVectorLayer(tree_cover, "Tree Cover", "ogr")
pop_density_layer = qgis.core.QgsVectorLayer(pop_density, "Population Density", "ogr")
transit_stops_layer = qgis.core.QgsVectorLayer(transit_stops, "Transit Stops", "ogr")
existing_pantries_layer = qgis.core.QgsVectorLayer(existing_pantries, "Existing Pantries", "ogr")

# HARDCODE AREA OF INTEREST
vrtcs = [QgsPointXY(-104.94510341021355, 39.68652925768433), QgsPointXY(-104.91485641232462, 39.68516620189644), QgsPointXY(-104.92112380828358, 39.66209502341533), QgsPointXY(-104.95927317499032, 39.66896474801089)]
aoiPolygon = QgsGeometry.fromPolygonXY([vrtcs])
aoiFeature = QgsFeature()
aoiFeature.setGeometry(aoiPolygon)
aoiLayer = qgis.core.QgsVectorLayer("Polygon?crs=epsg:4326&field=NAME:string(50)&field=TYPE:string(10)&field=AREA:double", "Area of Interest", "memory")
areaOfInterest = aoiLayer.dataProvider().addFeatures([aoiFeature])
# qgis.core.QgsVectorFileWriter.writeAsVectorFormat(aoiLayer, r"C:\Users\Sarah\Documents\GitHub\geog489-final\aoi.gpkg", "utf-8", aoiLayer.crs(), "GPKG")

#GET CLIPPED BUILDINGS
clipped_buildings = processing.run("qgis:clip", {"INPUT": buildings_layer, "OVERLAY": aoiLayer, "OUTPUT": "clipped_buildings"})
buildingsClip = clipped_buildings[ "OUTPUT"]
# need to do this for all input files
clipped_streets = processing.run("qgis:clip", {"INPUT": roads_layer, "OVERLAY": aoiLayer, "OUTPUT": "clipped_roads"})
streetsClip = clipped_streets[ "OUTPUT"]

#FILTER BUILDINGS BY ATTRIBUTE SO WE JUST HAVE COMMERCIAL BUILDINGS
query = '"BLDG_TYPE" = \'Commercial\''
commercial_buildings = processing.run("qgis:extractbyexpression", {"INPUT": buildingsClip, "EXPRESSION": query, "METHOD": 0 , "OUTPUT": "commercial_buildings"})
commercialBuildingsSelection = commercial_buildings[ "OUTPUT"]


# CREATE BUILDINGS BUFFER VECTOR LAYER (FT) - distance is in map units which for hardcoded files in feet
commercial_buildings_buffer = processing.run("native:buffer", {"INPUT": commercialBuildingsSelection, "DISTANCE": 20, "OUTPUT": "buffered_buildings"})
#need to do this for streets layer
streets_buffer = processing.run("native:buffer", {"INPUT": streetsClip, "DISTANCE": 10, "OUTPUT": r"C:\Users\Sarah\Documents\GitHub\geog489-final\streets_buffer.gpkg"})
#building_features = buildings_layer.getFeatures()
#buffer_radius = 20
#featList = []
#for f in building_features:
#    geometry = f.geometry()
#    buffer_geometry = geometry.buffer(buffer_radius, 8)
#    feat = QgsFeature()
#    feat.setGeometry(buffer_geometry)
#    featList.append(feat)
#buildingBufLayer = qgis.core.QgsVectorLayer("Polygon?crs=epsg:4326", "Buildings Buffer", "memory")
#building_buffer = buildingBufLayer.dataProvider().addFeatures(featList)
#qgis.core.QgsVectorFileWriter.writeAsVectorFormat(buildingBufLayer, r"C:\Users\Sarah\Documents\GitHub\geog489-final\buildings_buffer.gpkg", "utf-8", buildingBufLayer.crs(), "GPKG")

#GET VECTOR LAYER