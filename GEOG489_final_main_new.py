import sys, os
import qgis
import qgis.core
import ui_food_pantry_location
from qgis.core import *
#QgsVectorLayer, QgsApplication, QgsFeature, QgsGeometry, QgsPointXY, QgsCoordinateReferenceSystem, QgsFeatureRequest,
from PyQt5.QtWidgets import QApplication, QMainWindow, QStyle, QFileDialog, QDialog, QMessageBox, QSizePolicy, QAction
from PyQt5.QtGui import QStandardItemModel, QStandardItem,  QDoubleValidator, QIntValidator
from PyQt5.QtCore import Qt, QVariant, QMetaType
from qgis.gui import QgsMapToolPan, QgsMapToolZoom

from ui_food_pantry_location import Ui_MainWindow

# app = QApplication(sys.argv)
# qgis_prefix = os.getenv("QGIS_PREFIX_PATH")
# qgis.core.QgsApplication.setPrefixPath(qgis_prefix, True)
# qgs = qgis.core.QgsApplication([], False)
# qgs.initQgis()

# sys.path.append(os.path.join(qgis_prefix, "python", "plugins"))
# import processing
# from processing.core.Processing import Processing
# Processing.initialize()

#PROCESSING LOOK UP
# print([x.id() for x in QgsApplication.processingRegistry().algorithms() if "convert" in x.id()])
# print(processing.algorithmHelp("gdal:convertformat"))

def findSuitableParcels():
    # parcels = r"C:\Users\Sarah\Documents\GitHub\geog489-final\parcels.gpkg"
    # poverty = r"C:\Users\Sarah\Documents\GitHub\geog489-final\denver_poverty.gpkg"
    # pop_density = r"C:\Users\Sarah\Documents\GitHub\geog489-final\denver_popdensity.gpkg"
    # transit_stops = r"C:\Users\Sarah\Documents\GitHub\geog489-final\bus_stops.gpkg"
    # existing_pantries = r"C:\Users\Sarah\Documents\GitHub\geog489-final\pantries.gpkg"

    # parcels_layer = qgis.core.QgsVectorLayer(parcels, "Parcels", "ogr")
    # poverty_layer = qgis.core.QgsVectorLayer(poverty, "Poverty", "ogr")
    # pop_density_layer = qgis.core.QgsVectorLayer(pop_density, "Population_Density", "ogr")
    # transit_stops_layer = qgis.core.QgsVectorLayer(transit_stops, "Transit_Stops", "ogr")
    # existing_pantries_layer = qgis.core.QgsVectorLayer(existing_pantries, "Existing_Pantries", "ogr")

    # layers = [parcels_layer, poverty_layer, pop_density_layer, transit_stops_layer, existing_pantries_layer]

    # HARDCODE AREA OF INTEREST
    # vrtcs = [QgsPointXY(-104.99517, 39.76876), QgsPointXY(-104.97323, 39.77292), QgsPointXY(-104.97323, 39.74882), QgsPointXY(-104.99517, 39.75144)]
    # aoiPolygon = QgsGeometry.fromPolygonXY([vrtcs])
    # aoiFeature = QgsFeature()
    # aoiFeature.setGeometry(aoiPolygon)
    # aoiLayer = qgis.core.QgsVectorLayer("Polygon?crs=epsg:4326&field=NAME:string(50)&field=TYPE:string(10)&field=AREA:double", "Area of Interest", "memory")
    # areaOfInterest = aoiLayer.dataProvider().addFeatures([aoiFeature])

    # #GET CLIPPED LAYERS
    # clipped_layers = []
    # for layer in layers:
    #     # print(layer.name())
    #     layerClip = processing.run("qgis:clip", {"INPUT": layer, "OVERLAY": aoiLayer, "OUTPUT": "memory:"})
    #     clipLayer = layerClip["OUTPUT"]
    #     # print(layerClip["OUTPUT"])
    #     reprojectcrs = processing.run("native:reprojectlayer", {"INPUT": clipLayer, "TARGET_CRS": QgsCoordinateReferenceSystem("EPSG:2232"), "OUTPUT": "memory:"})
    #     reprolayer = reprojectcrs["OUTPUT"]
    #     reprolayer.setName(f"clipped_{layer.name()}")
    #     clipped_layers.append(reprolayer)

    #FUNCTION FOR FILTERING LAYER BY QUERY AND EXTRACTING THOSE FEATURES TO A NEW MEMORY LAYER
    def filterByQuery(layersList, layerNameSearch, query):
        layer = [l for l in layersList if layerNameSearch in os.path.basename(l.name())][0] #find the layer from the list whose name contains layerNameSearch
        filteredLayer = processing.run("qgis:extractbyexpression", {"INPUT": layer , "EXPRESSION": query, "OUTPUT": "memory:"}) #use processing to extract features based on the query
        return filteredLayer["OUTPUT"] #create a new memory vector layer

    # FUNCTION TO RETURN A LIST OF BUFFER GEOMETRIES AND THEIR CORRESPONDING SCORE VALUES
    def getBufferGeometry(layer, distanceScore):
        buffers = []
        # for every distance and score in distanceScore list, create a buffer around each feature in layer using distance val
        for distance, score in distanceScore:
            buffer = processing.run("native:buffer", {"INPUT": layer, "DISTANCE": distance, "DISSOLVE": True, "OUTPUT": "memory:"}) # create the buffer around each feature, create a single geometry using dissolve = True
            bufferVectorLayer = buffer[ "OUTPUT"] # save the file to memory
            bufferGeom = next(bufferVectorLayer.getFeatures()).geometry() # get the geometry of the first feature (there should only be one)
            buffers.append((bufferGeom, score)) # append the geometry and score to the buffers list

        return buffers

    # FUNCTION TO ADD A NEW FIELD TO A PARCEL LAYER AND UPDATE THEIR VALUES BASED ON THE BUFFER GEOMETRIES
    def updateParcelLayer(parcelLayer, fieldName, bufferGeoms, weight):
        parcelLayer.startEditing() # start editing the parcel layer (this is required for memory layers)
        newField = QgsField(fieldName, QMetaType.Double) # create a new field with the specified name and type (double)
        parcelLayer.dataProvider().addAttributes([newField])
        parcelLayer.updateFields()

        fieldIndex = parcelLayer.fields().indexOf(fieldName) # find the index of the new field

        normalizeWeight = weight / 100
        # for every feature in the parcel layer, check if the feature intersects with any of the buffers, if so, assign the corresponding score value
        for parcel in parcelLayer.getFeatures():
            updatedScore = 0
            for bufferGeom, score in bufferGeoms:
                if parcel.geometry().intersects(bufferGeom):
                    updatedScore = score * normalizeWeight
                    break
            parcelLayer.changeAttributeValue(parcel.id(), fieldIndex, updatedScore)
        parcelLayer.commitChanges() #save the changes to the memory layer
        return parcelLayer

    filteredParcels = filterByQuery(clipped_layers, "Parcels", '"D_CLASS_CN" = \'COMMERCIAL-RETAIL\'')
    # IF PANTRY LOCATIONS ARE INCLUDED, GET THE MIN DISTANCE AND FIND COMMERCIAL BUILDINGS OUTSIDE OF THAT DISTANCE
    clippedPantriesLayer = [layer for layer in clipped_layers if "Existing_Pantries" in os.path.basename(layer.name())][0]
    pantriesBuffer = processing.run("native:buffer", {"INPUT": clippedPantriesLayer, "DISTANCE": 1000, "OUTPUT": "memory:"})
    pantriesBufferLayer = pantriesBuffer[ "OUTPUT"]

    parcelsXPantry = processing.run("native:extractbylocation", {"INPUT": filteredParcels, "PREDICATE": 2, "INTERSECT": pantriesBufferLayer, "OUTPUT": "memory:"})
    parcelsXPantryLayer = parcelsXPantry[ "OUTPUT"]

    transit_layer = [l for l in clipped_layers if l.name() == "clipped_Transit_Stops"][0]
    transit_buffers = getBufferGeometry(transit_layer, [(200, 1), (500, 0.7), (800, 0.3)])
    parcelsXTransitLayer = updateParcelLayer(parcelsXPantryLayer, "Transit_Score", transit_buffers, 10)

    filteredPopDensity = filterByQuery(clipped_layers, "Population_Density", '"popdensity" > 15000')
    pop_density_buffers = getBufferGeometry(filteredPopDensity, [(0, 1), (2500, 0.7), (5000, 0.3)])
    parcelsXDensityLayer = updateParcelLayer(parcelsXTransitLayer, "Pop_Density_Score", pop_density_buffers, 30)
    # QgsVectorFileWriter.writeAsVectorFormat(parcelsXDensityLayer, r"C:\Users\Sarah\Documents\GitHub\geog489-final\commercialBuildingsWithTransitScoreAndPopDensityScore.gpkg", "utf-8", parcelsXDensityLayer.crs(), "GPKG")

    filteredPoverty = filterByQuery(clipped_layers, "Poverty", '"Percent_Po" >= 20')
    poverty_buffers = getBufferGeometry(filteredPoverty, [(0, 1), (15840, .5), (26400, .2)])
    parcelsXPovertyLayer = updateParcelLayer(parcelsXDensityLayer, "Poverty_Score", poverty_buffers, 60)
    # QgsVectorFileWriter.writeAsVectorFormat(parcelsXDensityLayer, r"C:\Users\Sarah\Documents\GitHub\geog489-final\commercialBuildingsWithpovscore.gpkg", "utf-8", parcelsXDensityLayer.crs(), "GPKG")

    #CALCULATE SUITABILITY SCORE

    parcelsXPovertyLayer.startEditing()

    new_field = QgsField("Suitability", QVariant.Double)
    parcelsXPovertyLayer.dataProvider().addAttributes([new_field])
    parcelsXPovertyLayer.updateFields()

    suitabilityIndex = parcelsXPovertyLayer.fields().indexOf("Suitability")

    for parcel in parcelsXPovertyLayer.getFeatures():
        suitability = parcel.attribute("Transit_Score") + parcel.attribute("Pop_Density_Score") + parcel.attribute("Poverty_Score")
        parcelsXPovertyLayer.changeAttributeValue(parcel.id(), suitabilityIndex, suitability)

    parcelsXPovertyLayer.commitChanges()

    QgsVectorFileWriter.writeAsVectorFormat(parcelsXPovertyLayer, r"C:\Users\Sarah\Documents\GitHub\geog489-final\commercialBuildingsWithSuitabilityScore.gpkg", "utf-8", parcelsXPovertyLayer.crs(), "GPKG")

class MyWnd(QMainWindow):

    def __init__(self, layer):

        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.canvas = self.ui.widget
        self.canvas.setCanvasColor(Qt.white)

        self.canvas.setExtent(layer.extent())
        self.canvas.setLayers([layer])

        self.actionZoomIn = QAction("Zoom in", self)
        self.actionZoomOut = QAction("Zoom out", self)
        self.actionPan = QAction("Pan", self)

        self.actionZoomIn.setCheckable(True)
        self.actionZoomOut.setCheckable(True)
        self.actionPan.setCheckable(True)

        self.actionZoomIn.triggered.connect(self.zoomIn)
        self.actionZoomOut.triggered.connect(self.zoomOut)
        self.actionPan.triggered.connect(self.pan)

        # self.toolbar = self.addToolBar("Canvas actions")
        # self.toolbar.addAction(self.actionZoomIn)
        # self.toolbar.addAction(self.actionZoomOut)
        # self.toolbar.addAction(self.actionPan)

        # create the map tools
        self.toolPan = QgsMapToolPan(self.canvas)
        self.toolPan.setAction(self.actionPan)
        self.toolZoomIn = QgsMapToolZoom(self.canvas, False) # false = in
        self.toolZoomIn.setAction(self.actionZoomIn)
        self.toolZoomOut = QgsMapToolZoom(self.canvas, True) # true = out
        self.toolZoomOut.setAction(self.actionZoomOut)

        self.pan()


    def zoomIn(self):
        self.canvas.setMapTool(self.toolZoomIn)

    def zoomOut(self):
        self.canvas.setMapTool(self.toolZoomOut)

    def pan(self):
        self.canvas.setMapTool(self.toolPan)

    #FUNCTION TO CLIP LAYERS TO AREA OF INTEREST AND REPROJECT
def clipLayerToAOI(layer, name):
    vector_layer = qgis.core.QgsVectorLayer(layer, "Parcels", "ogr")
    clippedLayer = processing.run("qgis:clip", {"INPUT": vector_layer, "OVERLAY": aoiLayer, "OUTPUT": "memory:"})["OUTPUT"]
    reprojectcrs = processing.run("native:reprojectlayer", {"INPUT": clippedLayer, "TARGET_CRS": QgsCoordinateReferenceSystem("EPSG:2232"), "OUTPUT": "memory:"})["OUTPUT"]
    reprojectcrs.setName(f"clipped_{vector_layer.name()}")
    # QgsVectorFileWriter.writeAsVectorFormat(reprojectcrs, r"C:\Users\Sarah\Documents\GitHub\geog489-final\clipped_tb_test.gpkg", "utf-8", reprojectcrs.crs(), "GPKG")
    return reprojectcrs

def selectParcelGPKGfile():       # get the input file from the user and add the path to the text box
    fileName, _ = QFileDialog.getOpenFileName(mainWindow,"Select GPKG file", "","GPKG (*.gpkg)")
    if fileName:
        ui.parcelsLineEdit.setText(fileName)
        gpkgName = os.path.basename(fileName)
        clipped = clipLayerToAOI(fileName, gpkgName)
        #update the map widget to show the clipped layer
        canvas.setLayers([clipped])


if __name__ == '__main__':
    # set up QGIS application and processing environment
    app = QApplication(sys.argv)
    qgis_prefix = os.getenv("QGIS_PREFIX_PATH")
    qgis.core.QgsApplication.setPrefixPath(qgis_prefix, True)
    qgs = qgis.core.QgsApplication([], False)
    qgs.initQgis()

    sys.path.append(os.path.join(qgis_prefix, "python", "plugins"))
    import processing
    from processing.core.Processing import Processing

    Processing.initialize()

    # ==========================================
    # create app and main window + dialog GUI
    # =========================================
    # set up main window
    mainWindow = QMainWindow()
    ui = ui_food_pantry_location.Ui_MainWindow()
    ui.setupUi(mainWindow)
    # ==========================================
    # connect signals
    # ==========================================
    ui.parcelsTB.clicked.connect(selectParcelGPKGfile)
    # ui.povertyTB.clicked.connect(selectGPKGfile)
    # ui.pop_densityTB.clicked.connect(selectGPKGfile)
    # ui.transitTB.clicked.connect(selectGPKGfile)
    # ui.pantryTB.clicked.connect(selectGPKGfile)
    # ui.linearTB.clicked.connect(selectLinearOutputfile)
    # ui.arealTB.clicked.connect(selectArealOutputfile)
    # ui.buttonBox.accepted.connect(runWaterbodyExtraction)
    # ui.buttonBox.rejected.connect(mainWindow.close)
    # =======================================
    # hardcoded aoi layer
    #=======================================
    vrtcs = [QgsPointXY(-104.99517, 39.76876), QgsPointXY(-104.97323, 39.77292), QgsPointXY(-104.97323, 39.74882), QgsPointXY(-104.99517, 39.75144)]
    aoiPolygon = QgsGeometry.fromPolygonXY([vrtcs])
    aoiFeature = QgsFeature()
    aoiFeature.setGeometry(aoiPolygon)
    aoiLayer = qgis.core.QgsVectorLayer("Polygon?crs=epsg:4326&field=NAME:string(50)&field=TYPE:string(10)&field=AREA:double", "Area of Interest", "memory")
    areaOfInterest = aoiLayer.dataProvider().addFeatures([aoiFeature])
    # =======================================
    # run app
    # =======================================
    mainWindow.show()
    # win = MyWnd(layer)
    # win.show()
    sys.exit(app.exec_())


#FILTER BUILDINGS BY ATTRIBUTE SO WE JUST HAVE COMMERCIAL BUILDINGS
# query = '"D_CLASS_CN" = \'COMMERCIAL-RETAIL\''
# clippedParcelsLayer = [layer for layer in clipped_layers if "Parcels" in os.path.basename(layer.name())][0]
# commercialBuildings = processing.run("qgis:extractbyexpression", {"INPUT": clippedParcelsLayer , "EXPRESSION": query, "OUTPUT": "memory:"})
# commercialBuildingsLayer = commercialBuildings[ "OUTPUT"]
# commercialRefinedByPantries = processing.run("native:extractbylocation", {"INPUT": commercialBuildingsLayer, "PREDICATE": 2, "INTERSECT": pantriesBufferLayer, "OUTPUT": "memory:"})
# commercialOutsidePantriesLayer = commercialRefinedByPantries[ "OUTPUT"]

# #ADD FIELD TO PARCELS FOR TRANSIT SCORE, ADD THE SCORE
# transit_layer = [l for l in clipped_layers if l.name() == "clipped_Transit_Stops"][0] #select the transit layer
# distanceScore = [(750, 1), (1500, 0.7), (3000, 0.3)] # defining distance, score values
# buffers = [] # creating empty buffers list
#
# # for every distance and score in distanceScore list, create a buffer around each transit stop using distance val
# for distance, scoreVal in distanceScore:
#     transitScore = processing.run("native:buffer", {"INPUT": transit_layer, "DISTANCE": distance, "DISSOLVE": True, "OUTPUT": "memory:"}) # create the buffer around each transit stop, create a single geometry using dissolve = True, save the file to memory
#     transitBuffer = transitScore[ "OUTPUT"]
#     buffer_geom = next(transitBuffer.getFeatures()).geometry()
#     buffers.append((buffer_geom, scoreVal))
#
# commercialOutsidePantriesLayer.startEditing() # start editing the memory layer
#
# #DECLARE THE NEW FIELD AND ADD IT TO THE LAYER
# new_field = QgsField("Transit_Score", QVariant.Double)
# commercialOutsidePantriesLayer.dataProvider().addAttributes([new_field])
# commercialOutsidePantriesLayer.updateFields()
#
# transitScoreIndex = commercialOutsidePantriesLayer.fields().indexOf("Transit_Score") # find the index of the new field
#
# # FOR EVERY FEATURE IN THE MEMORY LAYER, CHECK IF THE FEATURE INTERSECTS WITH ANY OF THE BUFFERS, IF SO, ASSIGN THE SCORE VALUE
# for parcel in commercialOutsidePantriesLayer.getFeatures():
#     transit_score = 0
#     for bufferGeom, score in buffers:
#         if parcel.geometry().intersects(bufferGeom):
#             transit_score = score
#             break
#     commercialOutsidePantriesLayer.changeAttributeValue(parcel.id(), transitScoreIndex, transit_score)
#
# commercialOutsidePantriesLayer.commitChanges()
#
# # QgsVectorFileWriter.writeAsVectorFormat(commercialOutsidePantriesLayer, r"C:\Users\Sarah\Documents\GitHub\geog489-final\commercialBuildingsWithTransitScore.gpkg", "utf-8", commercialBuildingsLayer.crs(), "GPKG")
#
# # FILTER POP DENSITY BY DENSITY
# query = '"popdensity" > 15000'
# clippedPopDensity = [layer for layer in clipped_layers if "Population_Density" in os.path.basename(layer.name())][0]
# popDensity = processing.run("qgis:extractbyexpression", {"INPUT": clippedPopDensity , "EXPRESSION": query, "OUTPUT": "memory:"})
# popDensityLayer = popDensity[ "OUTPUT"]
#
# #ADD FIELD TO PARCELS FOR POPULATION DENSITY SCORE, ADD THE SCORE
# popDensity_layer = popDensityLayer
# popDensityScore = [(0, 1), (2500, 0.7), (5000, 0.3)]
# buffers = []
# for distance, scoreVal in popDensityScore:
#     popDensityScore = processing.run("native:buffer", {"INPUT": popDensity_layer, "DISTANCE": distance, "DISSOLVE": True, "OUTPUT": "memory:"})
#     popDensityBuffer = popDensityScore[ "OUTPUT"]
#     buffer_geom = next(popDensityBuffer.getFeatures()).geometry()
#     buffers.append((buffer_geom, scoreVal))
#
# commercialOutsidePantriesLayer.startEditing()
#
# new_field = QgsField("Pop_Density_Score", QVariant.Double)
# commercialOutsidePantriesLayer.dataProvider().addAttributes([new_field])
# commercialOutsidePantriesLayer.updateFields()
#
# popDensityScoreIndex = commercialOutsidePantriesLayer.fields().indexOf("Pop_Density_Score")
#
# for parcel in commercialOutsidePantriesLayer.getFeatures():
#     pop_density_score = 0
#     for bufferGeom, score in buffers:
#         if parcel.geometry().intersects(bufferGeom):
#             pop_density_score = score
#             break
#     commercialOutsidePantriesLayer.changeAttributeValue(parcel.id(), popDensityScoreIndex, pop_density_score)
#
# commercialOutsidePantriesLayer.commitChanges()
#
# # QgsVectorFileWriter.writeAsVectorFormat(commercialOutsidePantriesLayer, r"C:\Users\Sarah\Documents\GitHub\geog489-final\commercialBuildingsWithTransitScoreAndPopDensityScore.gpkg", "utf-8", commercialBuildingsLayer.crs(), "GPKG")
#
# #CALCULATE SUITABILITY SCORE
#
# commercialOutsidePantriesLayer.startEditing()
#
# new_field = QgsField("Suitability", QVariant.Double)
# commercialOutsidePantriesLayer.dataProvider().addAttributes([new_field])
# commercialOutsidePantriesLayer.updateFields()
#
# suitabilityIndex = commercialOutsidePantriesLayer.fields().indexOf("Suitability")
#
# # hard-coded user input weights
# transit_weight = 30
# normalized_transit_weight = (transit_weight / 100)
# pop_density_weight = 70
# normalized_pop_density_weight = (pop_density_weight / 100)
#
# for parcel in commercialOutsidePantriesLayer.getFeatures():
#     suitability = (parcel.attribute("Transit_Score") * normalized_transit_weight) + (parcel.attribute("Pop_Density_Score") * normalized_pop_density_weight)
#     commercialOutsidePantriesLayer.changeAttributeValue(parcel.id(), suitabilityIndex, suitability)
#
# commercialOutsidePantriesLayer.commitChanges()
#
# QgsVectorFileWriter.writeAsVectorFormat(commercialOutsidePantriesLayer, r"C:\Users\Sarah\Documents\GitHub\geog489-final\commercialBuildingsWithSuitabilityScore.gpkg", "utf-8", commercialBuildingsLayer.crs(), "GPKG")



# IF TRANSIT STOP ARE INCLUDED, GET THE USER INPUT MAX DISTANCE AND FIND COMMERCIAL BUILDINGS WITHIN THAT DISTANCE
# clippedTransitStopsLayer = [layer for layer in clipped_layers if "Transit_Stops" in os.path.basename(layer.name())][0]
# transitBuffer = processing.run("native:buffer", {"INPUT": clippedTransitStopsLayer, "DISTANCE": 500, "OUTPUT": "memory:"})
# transitBufferLayer = transitBuffer[ "OUTPUT"]
# commercialRefinedByTransit = processing.run("native:extractbylocation", {"INPUT": commercialBuildingsLayer, "PREDICATE": 0,  "INTERSECT": transitBufferLayer, "OUTPUT": "memory:"})
# commercialBuildingsLayer = commercialRefinedByTransit[ "OUTPUT"]