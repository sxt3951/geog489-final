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


#PROCESSING LOOK UP
# print([x.id() for x in QgsApplication.processingRegistry().algorithms() if "convert" in x.id()])
# print(processing.algorithmHelp("gdal:convertformat"))


# HARDCODED INPUT FILES
# buildings = r"C:\Users\Sarah\Documents\GitHub\geog489-final\buildings.gpkg"
# roads = r"C:\Users\Sarah\Documents\GitHub\geog489-final\denver_streets.gpkg"
# tree_cover = r"C:\Users\Sarah\Documents\GitHub\geog489-final\tree_canopy.gpkg"
parcels = r"C:\Users\Sarah\Documents\GitHub\geog489-final\parcels.gpkg"
poverty = r"C:\Users\Sarah\Documents\GitHub\geog489-final\denver_poverty.gpkg"
pop_density = r"C:\Users\Sarah\Documents\GitHub\geog489-final\denver_popdensity.gpkg"
transit_stops = r"C:\Users\Sarah\Documents\GitHub\geog489-final\bus_stops.gpkg"
existing_pantries = r"C:\Users\Sarah\Documents\GitHub\geog489-final\pantries.gpkg"

# Create QGIS Vector Layers - we might want to create a class for this where we can check if the layer is valid
# buildings_layer = qgis.core.QgsVectorLayer(buildings, "Buildings", "ogr")
# roads_layer = qgis.core.QgsVectorLayer(roads, "Roads", "ogr")
# tree_cover_layer = qgis.core.QgsVectorLayer(tree_cover, "Tree Cover", "ogr")
parcels_layer = qgis.core.QgsVectorLayer(parcels, "Parcels", "ogr")
poverty_layer = qgis.core.QgsVectorLayer(poverty, "Poverty", "ogr")
pop_density_layer = qgis.core.QgsVectorLayer(pop_density, "Population_Density", "ogr")
transit_stops_layer = qgis.core.QgsVectorLayer(transit_stops, "Transit_Stops", "ogr")
existing_pantries_layer = qgis.core.QgsVectorLayer(existing_pantries, "Existing_Pantries", "ogr")

layers = [parcels_layer, poverty_layer, pop_density_layer, transit_stops_layer, existing_pantries_layer]

# HARDCODE AREA OF INTEREST
vrtcs = [QgsPointXY(-104.99517, 39.76876), QgsPointXY(-104.97323, 39.77292), QgsPointXY(-104.97323, 39.74882), QgsPointXY(-104.99517, 39.75144)]
aoiPolygon = QgsGeometry.fromPolygonXY([vrtcs])
aoiFeature = QgsFeature()
aoiFeature.setGeometry(aoiPolygon)
aoiLayer = qgis.core.QgsVectorLayer("Polygon?crs=epsg:4326&field=NAME:string(50)&field=TYPE:string(10)&field=AREA:double", "Area of Interest", "memory")
areaOfInterest = aoiLayer.dataProvider().addFeatures([aoiFeature])
# qgis.core.QgsVectorFileWriter.writeAsVectorFormat(aoiLayer, r"C:\Users\Sarah\Documents\GitHub\geog489-final\aoi.gpkg", "utf-8", aoiLayer.crs(), "GPKG")

#GET CLIPPED LAYERS
clipped_layers = []
for layer in layers:
    # print(layer.name())
    layerClip = processing.run("qgis:clip", {"INPUT": layer, "OVERLAY": aoiLayer, "OUTPUT": "memory:"})
    clipLayer = layerClip["OUTPUT"]
    # print(layerClip["OUTPUT"])
    reprojectcrs = processing.run("native:reprojectlayer", {"INPUT": clipLayer, "TARGET_CRS": QgsCoordinateReferenceSystem("EPSG:2232"), "OUTPUT": "memory:"})
    reprolayer = reprojectcrs["OUTPUT"]
    reprolayer.setName(f"clipped_{layer.name()}")
    clipped_layers.append(reprolayer)

print (clipped_layers)
for layer in clipped_layers:
    print(layer)


# clipped_buildings = processing.run("qgis:clip", {"INPUT": buildings_layer, "OVERLAY": aoiLayer, "OUTPUT": "clipped_buildings"})
# buildingsClip = clipped_buildings[ "OUTPUT"]
# # need to do this for all input files
# clipped_streets = processing.run("qgis:clip", {"INPUT": roads_layer, "OVERLAY": aoiLayer, "OUTPUT": "clipped_roads"})
# streetsClip = clipped_streets[ "OUTPUT"]
#


#FILTER BUILDINGS BY ATTRIBUTE SO WE JUST HAVE COMMERCIAL BUILDINGS
query = '"D_CLASS_CN" = \'COMMERCIAL-RETAIL\''
clippedParcelsLayer = [layer for layer in clipped_layers if "Parcels" in os.path.basename(layer.name())][0]
commercialBuildings = processing.run("qgis:extractbyexpression", {"INPUT": clippedParcelsLayer , "EXPRESSION": query, "OUTPUT": "memory:"})
commercialBuildingsLayer = commercialBuildings[ "OUTPUT"]

# IF TRANSIT STOP ARE INCLUDED, GET THE USER INPUT MAX DISTANCE AND FIND COMMERCIAL BUILDINGS WITHIN THAT DISTANCE
clippedTransitStopsLayer = [layer for layer in clipped_layers if "Transit_Stops" in os.path.basename(layer.name())][0]
transitBuffer = processing.run("native:buffer", {"INPUT": clippedTransitStopsLayer, "DISTANCE": 500, "OUTPUT": r"C:\Users\Sarah\Documents\GitHub\geog489-final\transit_buffer.gpkg"})
transitBufferLayer = transitBuffer[ "OUTPUT"]
commercialRefinedByTransit = processing.run("native:extractbylocation", {"INPUT": commercialBuildingsLayer, "PREDICATE": 0,  "INTERSECT": transitBufferLayer, "OUTPUT": r"C:\Users\Sarah\Documents\GitHub\geog489-final\buildings_transit.gpkg"})
commercialBuildingsLayer = commercialRefinedByTransit[ "OUTPUT"]


# IF PANTRY LOCATIONS ARE INCLUDED, GET THE MIN DISTANCE AND FIND COMMERCIAL BUILDINGS OUTSIDE OF THAT DISTANCE
# for layer in clipped_layers:
#     if "Pantries" in os.path.basename(layer):
#         pantriesBuffer = processing.run("native:buffer", {"INPUT": layer, "DISTANCE": 1000, "OUTPUT": r"C:\Users\Sarah\Documents\GitHub\geog489-final\pantry_buffer.gpkg"})
#         pantriesBufferLayer = pantriesBuffer[ "OUTPUT"]
#         commercialRefinedByPantries = processing.run("native:extractbylocation", {"INPUT": commercialBuildingsLayer, "PREDICATE": 2, "INTERSECT": pantriesBufferLayer, "OUTPUT": r"C:\Users\Sarah\Documents\GitHub\geog489-final\commercialOutsidePantries.gpkg"})
#         commercialOutsidePantriesLayer = commercialRefinedByPantries[ "OUTPUT"]

# # CREATE BUILDINGS BUFFER VECTOR LAYER (FT) - distance is in map units which for hardcoded files in feet
# commercial_buildings_buffer = processing.run("native:buffer", {"INPUT": commercialBuildingsSelection, "DISTANCE": 20, "OUTPUT": "buffered_buildings"})
# bufferedBuildings = commercial_buildings_buffer[ "OUTPUT"]
# #need to do this for streets layer
# streets_buffer = processing.run("native:buffer", {"INPUT": streetsClip, "DISTANCE": 20, "OUTPUT": "streets_buffer"})
# bufferedStreets = streets_buffer[ "OUTPUT"]
#
# #building_features = buildings_layer.getFeatures()
# #buffer_radius = 20
# #featList = []
# #for f in building_features:
# #    geometry = f.geometry()
# #    buffer_geometry = geometry.buffer(buffer_radius, 8)
# #    feat = QgsFeature()
# #    feat.setGeometry(buffer_geometry)
# #    featList.append(feat)
# #buildingBufLayer = qgis.core.QgsVectorLayer("Polygon?crs=epsg:4326", "Buildings Buffer", "memory")
# #building_buffer = buildingBufLayer.dataProvider().addFeatures(featList)
# #qgis.core.QgsVectorFileWriter.writeAsVectorFormat(buildingBufLayer, r"C:\Users\Sarah\Documents\GitHub\geog489-final\buildings_buffer.gpkg", "utf-8", buildingBufLayer.crs(), "GPKG")
#
# #GET VECTOR LAYER THAT IS THE BUFFERED AREA AROUND COMMERCIAL BUILDINGS THAT IS OUTSIDE STREET BUFFER
# buildBufferSubBuildings = processing.run("native:difference", {"INPUT": bufferedBuildings , "OVERLAY": commercialBuildingsSelection, "OUTPUT": "memory:"})
# bufferSubBuildings = buildBufferSubBuildings[ "OUTPUT"]
#
# print("After building difference:", bufferSubBuildings.featureCount())
#
# bufferSubStreetBuffer = processing.run("native:difference", {"INPUT": bufferSubBuildings , "OVERLAY": bufferedStreets, "OUTPUT": "memory:"})
# bufferSubStreet = bufferSubStreetBuffer[ "OUTPUT"]
#
# print("After street difference:", bufferSubStreet.featureCount())
#
# #CREATE RASTER FROM PREVIOUS VECTOR
# extent = aoiLayer.extent()
# extent_string = f"{extent.xMinimum()},{extent.xMaximum()},{extent.yMinimum()},{extent.yMaximum()} [{aoiLayer.crs().authid()}]"
# bufferRaster = processing.run("gdal:rasterize", {"INPUT": bufferSubStreet, "FIELD": "OBJECTID", "BURN": 1, "UNITS": 1, "WIDTH": 10, "HEIGHT":10, "EXTENT": extent_string, "OUTPUT": r"C:\Users\Sarah\Documents\GitHub\geog489-final\bufferRaster.tif"})
# bufferRaster = bufferRaster[ "OUTPUT"]
# print("After rasterize:", bufferRaster)
#
# #RECLASSIFY RASTER
# reclassRaster = processing.run("native:reclassifybylayer", {"INPUT_RASTER": bufferRaster, "INPUT_TABLE": pop_density_layer, "MIN_FIELD": "popdensity", "MAX_FIELD": "popdensity", "VALUE_FIELD": "popdensity", "OUTPUT": r"C:\Users\Sarah\Documents\GitHub\geog489-final\reclassRaster.tif" })
# #this took a very long time, but ran before clipping pop_density_layer