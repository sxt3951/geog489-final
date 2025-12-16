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

import ui_food_pantry_location
import map_pop_up

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
    # COLLECT AOI INPUT COORDS AND CREATE AOI POLYGON
    def createAOIPolygon(coords1, coords2, coords3, coords4):
        coordsList = [coords1, coords2, coords3, coords4]

        # CREATE QGS POINTS FROM COORDS
        vrtcs = []
        for coord in coordsList:
            coords = coord.split(",")
            point = QgsPointXY(float(coords[0]), float(coords[1]))
            vrtcs.append(point)

        aoiPolygon = QgsGeometry.fromPolygonXY([vrtcs])
        aoiFeature = QgsFeature()
        aoiFeature.setGeometry(aoiPolygon)
        aoiLayer = qgis.core.QgsVectorLayer(
            "Polygon?crs=epsg:4326&field=NAME:string(50)&field=TYPE:string(10)&field=AREA:double", "Area of Interest",
            "memory")
        aoiLayer.dataProvider().addFeatures([aoiFeature])
        return aoiLayer

        # -104.99517, 39.76876
        # -104.97323, 39.77292
        # -104.97323, 39.74882
        # -104.99517, 39.75144

    #GET THE LAYERS FROM THE USER INPUT
    parcels = parcelsLineEdit.text()
    poverty = povertyLineEdit.text()
    pop_density = pop_densityLineEdit.text()
    transit_stops = transitLineEdit.text()
    existing_pantries = pantryLineEdit.text()

    parcels_layer = qgis.core.QgsVectorLayer(parcels, "Parcels", "ogr")
    poverty_layer = qgis.core.QgsVectorLayer(poverty, "Poverty", "ogr")
    pop_density_layer = qgis.core.QgsVectorLayer(pop_density, "Population_Density", "ogr")
    transit_stops_layer = qgis.core.QgsVectorLayer(transit_stops, "Transit_Stops", "ogr")
    existing_pantries_layer = qgis.core.QgsVectorLayer(existing_pantries, "Existing_Pantries", "ogr")

    layers = [parcels_layer, poverty_layer, pop_density_layer, transit_stops_layer, existing_pantries_layer]

    # FUNCTION TO CLIP LAYER TO AREA OF INTEREST AND REPROJECT
    def clipLayerToAOI(aoiLayer, layer, name):
        vector_layer = qgis.core.QgsVectorLayer(layer, "Parcels", "ogr")
        clippedLayer = processing.run("qgis:clip", {"INPUT": vector_layer, "OVERLAY": aoiLayer, "OUTPUT": "memory:"})[
            "OUTPUT"]
        reprojectcrs = processing.run("native:reprojectlayer",
                                      {"INPUT": clippedLayer, "TARGET_CRS": QgsCoordinateReferenceSystem("EPSG:2232"),
                                       "OUTPUT": "memory:"})["OUTPUT"]
        reprojectcrs.setName(f"clipped_{vector_layer.name()}")
        # QgsVectorFileWriter.writeAsVectorFormat(reprojectcrs, r"C:\Users\Sarah\Documents\GitHub\geog489-final\clipped_tb_test.gpkg", "utf-8", reprojectcrs.crs(), "GPKG")
        return reprojectcrs

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

    # GET CLIPPED LAYERS
    clipped_layers = []
    AreaOfInterest = createAOIPolygon(ui.coord1lineEdit.text(), ui.coord2lineEdit.text(), ui.coord3lineEdit.text(), ui.coord4lineEdit.text())
    for layer in layers:
        layerClip = processing.run("qgis:clip", {"INPUT": layer, "OVERLAY": AreaOfInterest, "OUTPUT": "memory:"})
        clipLayer = layerClip["OUTPUT"]
        reprojectcrs = processing.run("native:reprojectlayer", {"INPUT": clipLayer, "TARGET_CRS": QgsCoordinateReferenceSystem("EPSG:2232"), "OUTPUT": "memory:"})
        reprolayer = reprojectcrs["OUTPUT"]
        reprolayer.setName(f"clipped_{layer.name()}")
        clipped_layers.append(reprolayer)

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


#FUNCTION TO GET PARCEL FILE FROM USER
def selectParcelGPKGfile():       # get the input file from the user and add the path to the text box
    fileName, _ = QFileDialog.getOpenFileName(mainWindow,"Select GPKG file", "","GPKG (*.gpkg)")
    if fileName:
        ui.parcelsLineEdit.setText(fileName)

#FUNCTION TO GET THE POVERTY FILE FROM THE USER
def selectPovertyGPKGFile():
    fileName, _ = QFileDialog.getOpenFileName(mainWindow,"Select GPKG file", "","GPKG (*.gpkg)")
    if fileName:
        ui.povertyLineEdit.setText(fileName)

#FUNCTION TO GET THE POPULATION DENSITY FILE FROM THE USER
def selectPopDensityGPKGFile():
    fileName, _ = QFileDialog.getOpenFileName(mainWindow,"Select GPKG file", "","GPKG (*.gpkg)")
    if fileName:
        ui.pop_densityLineEdit.setText(fileName)

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

    # createShapefileDialog = QDialog(mainWindow)
    # createShapefileDialog_ui = gui_newshapefile.Ui_Dialog()
    # createShapefileDialog_ui.setupUi(createShapefileDialog)


    # ==========================================
    # connect signals
    # ==========================================
    ui.parcelsTB.clicked.connect(selectParcelGPKGfile)
    ui.povertyTB.clicked.connect(selectPovertyGPKGFile)
    ui.pop_densityTB.clicked.connect(selectPopDensityGPKGFile)
    ui.buttonBox.accepted.connect(createAOIPolygon)
    ui.buttonBox.rejected.connect(mainWindow.close)
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
    # =======================================
    # run app
    # =======================================
    mainWindow.show()

    # win = MyWnd(clipped_test)
    # win.show()
    sys.exit(app.exec_())
