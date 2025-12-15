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
from PyQt5.QtCore import Qt, QVariant

app = QApplication(sys.argv)
qgis_prefix = os.getenv("QGIS_PREFIX_PATH")
qgis.core.QgsApplication.setPrefixPath(qgis_prefix, True)
qgs = qgis.core.QgsApplication([], False)
qgs.initQgis()

sys.path.append(os.path.join(qgis_prefix, "python", "plugins"))
import processing
from processing.core.Processing import Processing
Processing.initialize()

#PROCESSING LOOK UP
# print([x.id() for x in QgsApplication.processingRegistry().algorithms() if "convert" in x.id()])
# print(processing.algorithmHelp("gdal:convertformat"))

parcels = r"C:\Users\Sarah\Documents\GitHub\geog489-final\parcels.gpkg"
poverty = r"C:\Users\Sarah\Documents\GitHub\geog489-final\denver_poverty.gpkg"
pop_density = r"C:\Users\Sarah\Documents\GitHub\geog489-final\denver_popdensity.gpkg"
transit_stops = r"C:\Users\Sarah\Documents\GitHub\geog489-final\bus_stops.gpkg"
existing_pantries = r"C:\Users\Sarah\Documents\GitHub\geog489-final\pantries.gpkg"

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

# print (clipped_layers)
# for layer in clipped_layers:
#     print(layer)



#FILTER BUILDINGS BY ATTRIBUTE SO WE JUST HAVE COMMERCIAL BUILDINGS
query = '"D_CLASS_CN" = \'COMMERCIAL-RETAIL\''
clippedParcelsLayer = [layer for layer in clipped_layers if "Parcels" in os.path.basename(layer.name())][0]
commercialBuildings = processing.run("qgis:extractbyexpression", {"INPUT": clippedParcelsLayer , "EXPRESSION": query, "OUTPUT": "memory:"})
commercialBuildingsLayer = commercialBuildings[ "OUTPUT"]

# IF PANTRY LOCATIONS ARE INCLUDED, GET THE MIN DISTANCE AND FIND COMMERCIAL BUILDINGS OUTSIDE OF THAT DISTANCE
clippedPantriesLayer = [layer for layer in clipped_layers if "Existing_Pantries" in os.path.basename(layer.name())][0]
pantriesBuffer = processing.run("native:buffer", {"INPUT": clippedPantriesLayer, "DISTANCE": 1000, "OUTPUT": "memory:"})
pantriesBufferLayer = pantriesBuffer[ "OUTPUT"]
commercialRefinedByPantries = processing.run("native:extractbylocation", {"INPUT": commercialBuildingsLayer, "PREDICATE": 2, "INTERSECT": pantriesBufferLayer, "OUTPUT": "memory:"})
commercialOutsidePantriesLayer = commercialRefinedByPantries[ "OUTPUT"]

#ADD FIELD TO PARCELS FOR TRANSIT SCORE, ADD THE SCORE
transit_layer = [l for l in clipped_layers if l.name() == "clipped_Transit_Stops"][0]
distanceScore = [(750, 1), (1500, 0.7), (3000, 0.3)]
buffers = []
for distance, scoreVal in distanceScore:
    transitScore = processing.run("native:buffer", {"INPUT": transit_layer, "DISTANCE": distance, "DISSOLVE": True, "OUTPUT": "memory:"})
    transitBuffer = transitScore[ "OUTPUT"]
    buffer_geom = next(transitBuffer.getFeatures()).geometry()
    buffers.append((buffer_geom, scoreVal))

commercialOutsidePantriesLayer.startEditing()

new_field = QgsField("Transit_Score", QVariant.Double)
commercialOutsidePantriesLayer.dataProvider().addAttributes([new_field])
commercialOutsidePantriesLayer.updateFields()

transitScoreIndex = commercialOutsidePantriesLayer.fields().indexOf("Transit_Score")

for parcel in commercialOutsidePantriesLayer.getFeatures():
    transit_score = 0
    for bufferGeom, score in buffers:
        if parcel.geometry().intersects(bufferGeom):
            transit_score = score
            break
    commercialOutsidePantriesLayer.changeAttributeValue(parcel.id(), transitScoreIndex, transit_score)

commercialOutsidePantriesLayer.commitChanges()

# QgsVectorFileWriter.writeAsVectorFormat(commercialOutsidePantriesLayer, r"C:\Users\Sarah\Documents\GitHub\geog489-final\commercialBuildingsWithTransitScore.gpkg", "utf-8", commercialBuildingsLayer.crs(), "GPKG")

# FILTER POP DENSITY BY DENSITY
query = '"popdensity" > 15000'
clippedPopDensity = [layer for layer in clipped_layers if "Population_Density" in os.path.basename(layer.name())][0]
popDensity = processing.run("qgis:extractbyexpression", {"INPUT": clippedPopDensity , "EXPRESSION": query, "OUTPUT": "memory:"})
popDensityLayer = popDensity[ "OUTPUT"]

#ADD FIELD TO PARCELS FOR POPULATION DENSITY SCORE, ADD THE SCORE
popDensity_layer = popDensityLayer
popDensityScore = [(0, 1), (2500, 0.7), (5000, 0.3)]
buffers = []
for distance, scoreVal in popDensityScore:
    popDensityScore = processing.run("native:buffer", {"INPUT": popDensity_layer, "DISTANCE": distance, "DISSOLVE": True, "OUTPUT": "memory:"})
    popDensityBuffer = popDensityScore[ "OUTPUT"]
    buffer_geom = next(popDensityBuffer.getFeatures()).geometry()
    buffers.append((buffer_geom, scoreVal))

commercialOutsidePantriesLayer.startEditing()

new_field = QgsField("Pop_Density_Score", QVariant.Double)
commercialOutsidePantriesLayer.dataProvider().addAttributes([new_field])
commercialOutsidePantriesLayer.updateFields()

popDensityScoreIndex = commercialOutsidePantriesLayer.fields().indexOf("Pop_Density_Score")

for parcel in commercialOutsidePantriesLayer.getFeatures():
    pop_density_score = 0
    for bufferGeom, score in buffers:
        if parcel.geometry().intersects(bufferGeom):
            pop_density_score = score
            break
    commercialOutsidePantriesLayer.changeAttributeValue(parcel.id(), popDensityScoreIndex, pop_density_score)

commercialOutsidePantriesLayer.commitChanges()

# QgsVectorFileWriter.writeAsVectorFormat(commercialOutsidePantriesLayer, r"C:\Users\Sarah\Documents\GitHub\geog489-final\commercialBuildingsWithTransitScoreAndPopDensityScore.gpkg", "utf-8", commercialBuildingsLayer.crs(), "GPKG")

#CALCULATE SUITABILITY SCORE

commercialOutsidePantriesLayer.startEditing()

new_field = QgsField("Suitability", QVariant.Double)
commercialOutsidePantriesLayer.dataProvider().addAttributes([new_field])
commercialOutsidePantriesLayer.updateFields()

suitabilityIndex = commercialOutsidePantriesLayer.fields().indexOf("Suitability")

# hard-coded user input weights
transit_weight = 30
normalized_transit_weight = (transit_weight / 100)
pop_density_weight = 70
normalized_pop_density_weight = (pop_density_weight / 100)

for parcel in commercialOutsidePantriesLayer.getFeatures():
    suitability = (parcel.attribute("Transit_Score") * normalized_transit_weight) + (parcel.attribute("Pop_Density_Score") * normalized_pop_density_weight)
    commercialOutsidePantriesLayer.changeAttributeValue(parcel.id(), suitabilityIndex, suitability)

commercialOutsidePantriesLayer.commitChanges()

QgsVectorFileWriter.writeAsVectorFormat(commercialOutsidePantriesLayer, r"C:\Users\Sarah\Documents\GitHub\geog489-final\commercialBuildingsWithSuitabilityScore.gpkg", "utf-8", commercialBuildingsLayer.crs(), "GPKG")




# IF TRANSIT STOP ARE INCLUDED, GET THE USER INPUT MAX DISTANCE AND FIND COMMERCIAL BUILDINGS WITHIN THAT DISTANCE
# clippedTransitStopsLayer = [layer for layer in clipped_layers if "Transit_Stops" in os.path.basename(layer.name())][0]
# transitBuffer = processing.run("native:buffer", {"INPUT": clippedTransitStopsLayer, "DISTANCE": 500, "OUTPUT": "memory:"})
# transitBufferLayer = transitBuffer[ "OUTPUT"]
# commercialRefinedByTransit = processing.run("native:extractbylocation", {"INPUT": commercialBuildingsLayer, "PREDICATE": 0,  "INTERSECT": transitBufferLayer, "OUTPUT": "memory:"})
# commercialBuildingsLayer = commercialRefinedByTransit[ "OUTPUT"]


