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


#PROCESSING LOOK UP
# print([x.id() for x in QgsApplication.processingRegistry().algorithms() if "convert" in x.id()])
# print(processing.algorithmHelp("gdal:convertformat"))

def findSuitableParcels():

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
            features = list(bufferVectorLayer.getFeatures())
            if not features:
                continue
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

    #GET THE LAYERS FROM THE USER INPUT
    parcels = ui.parcelsLineEdit.text()
    poverty = ui.povertyLineEdit.text()
    povertyValue = ui.povertyValLineEdit.text()
    povertyWeight = int(ui.poverty_weightLineEdit.text())
    pop_density = ui.pop_densityLineEdit.text()
    pop_densityValue = ui.pop_densityValLineEdit.text()
    pop_densityWeight = int(ui.pop_density_weightLineEdit.text())
    transit_stops = ui.transitLineEdit.text()
    transitWeight = ui.transit_weightLineEdit.text()
    existing_pantries = ui.pantryLineEdit.text()
    pantry_distance = ui.pantry_distLineEdit.text()
    aoiPolygon = ui.AOIlineEdit.text()
    outputFile = ui.OutputlineEdit.text()

    # CREATE THE AOI LAYER FROM THE USER INPUT
    coordPairs = aoiPolygon.split("),") # split the string by the closing parenthesis
    vrtcs = []
    # loop through coordsList and create QgsPointXY objects
    for pair in coordPairs:
        pair = pair.replace("(", "").replace(")", "").strip() # replace the opening and closing parenthesis and strip whitespace
        yCoord, xCoord = pair.split(",") # split the string by the comma
        x, y = float(xCoord.strip()), float(yCoord.strip()) # switch the order of the coordinates
        vrtcs.append(QgsPointXY(x, y))
    aoiPolygon = QgsGeometry.fromPolygonXY([vrtcs]) # create a polygon from the list of QgsPointXY objects
    aoiFeature = QgsFeature() # create a new feature
    aoiFeature.setGeometry(aoiPolygon) # set the geometry of the feature to the polygon created above
    aoiLayer = qgis.core.QgsVectorLayer("Polygon?crs=epsg:4326&field=NAME:string(50)&field=TYPE:string(10)&field=AREA:double", "Area of Interest", "memory") # create a new memory layer with the specified fields
    areaOfInterest = aoiLayer.dataProvider().addFeatures([aoiFeature]) # add the feature to the layer


    # CONVERT THE LAYERS TO QGIS VECTOR LAYERS
    parcels_layer = qgis.core.QgsVectorLayer(parcels, "Parcels", "ogr")
    poverty_layer = qgis.core.QgsVectorLayer(poverty, "Poverty", "ogr")
    pop_density_layer = qgis.core.QgsVectorLayer(pop_density, "Population_Density", "ogr")
    if transit_stops != "": # if the user input is not empty, create a new QGIS vector layer
        transit_stops_layer = qgis.core.QgsVectorLayer(transit_stops, "Transit_Stops", "ogr")
    else:
        transit_stops_layer = None
    if existing_pantries != "": # if the user input is not empty, create a new QGIS vector layer
        existing_pantries_layer = qgis.core.QgsVectorLayer(existing_pantries, "Existing_Pantries", "ogr")
    else:
        existing_pantries_layer = None

    layers = [parcels_layer, poverty_layer, pop_density_layer, transit_stops_layer, existing_pantries_layer]

    #GET CLIPPED LAYERS
    clipped_layers = []

    # loop through layers and clip them to the AOI, reproject them to EPSG:2232, and add them to the clipped_layers list
    for layer in layers:
        if layer is None:
            continue
        layerClip = processing.run("qgis:clip", {"INPUT": layer, "OVERLAY": aoiLayer, "OUTPUT": "memory:"})["OUTPUT"]
        # clipLayer = layerClip["OUTPUT"]
        reprojectcrs = processing.run("native:reprojectlayer", {"INPUT": layerClip, "TARGET_CRS": QgsCoordinateReferenceSystem("EPSG:2232"), "OUTPUT": "memory:"})["OUTPUT"]
        reprojectcrs.setName(f"clipped_{layer.name()}")
        clipped_layers.append(reprojectcrs)

    # find the parcels that are commercial retail buildings - this is a hardcoded variable for now
    filteredParcels = filterByQuery(clipped_layers, "Parcels", '"D_CLASS_CN" = \'COMMERCIAL-RETAIL\'')

    # IF PANTRY LOCATIONS ARE INCLUDED, GET THE MIN DISTANCE AND FIND COMMERCIAL BUILDINGS OUTSIDE OF THAT DISTANCE
    if existing_pantries == "":
        updatedParcels = filteredParcels

    else:
        # find the pantries layer
        clippedPantriesLayer = [layer for layer in clipped_layers if "Existing_Pantries" in os.path.basename(layer.name())][0]
        # buffer the pantries layer by the specified distance and create a new memory layer
        pantriesBuffer = processing.run("native:buffer", {"INPUT": clippedPantriesLayer, "DISTANCE": float(pantry_distance)*5280,
                                                          "OUTPUT": "memory:"})
        pantriesBufferLayer = pantriesBuffer["OUTPUT"]
        # extract the parcels that are outside of the pantries buffer, predicate = 2 indicates we are extracting by disjoint aka featurs that do NOT intersect the buffer
        parcelsXPantry = processing.run("native:extractbylocation",
                                        {"INPUT": filteredParcels, "PREDICATE": 2, "INTERSECT": pantriesBufferLayer,
                                         "OUTPUT": "memory:"})
        updatedParcels = parcelsXPantry["OUTPUT"]

    #IF TRANSIT LAYER IS INCLUDED, CREATE BUFFERS AND ASSIGN SCORE VALUES TO PARCELS THAT INTERSECT WITH THEM
    if transit_stops == "":
        updatedParcels = updatedParcels

    else:
        # find the transit layer
        transit_layer = [l for l in clipped_layers if l.name() == "clipped_Transit_Stops"][0]
        # create the buffers and assign scores
        transit_buffers = getBufferGeometry(transit_layer, [(200, 1), (500, 0.7), (800, 0.3)])
        updatedParcels = updateParcelLayer(updatedParcels, "Transit_Score", transit_buffers, int(transitWeight))

    #CREATE BUFFERS AROUND POVERTY TRACTS AND ASSIGN SCORE VALUES TO THE PARCELS THAT INTERSECT WITH THEM
    # filter to only use tracts with a poverty % greater than the user input
    povertyQuery = f'"Percent_Po" >= {povertyValue}'
    # filter layer so that we are only using tracts that represent the query in our buffer function
    filteredPoverty = filterByQuery(clipped_layers, "Poverty", povertyQuery)
    # create the buffers and assign scores
    poverty_buffers = getBufferGeometry(filteredPoverty, [(0, 1), (15840, .5), (26400, .2)])
    updatedParcels = updateParcelLayer(updatedParcels, "Poverty_Score", poverty_buffers, povertyWeight)

    # CREATE BUFFERS AROUND POPDENSITY BLOCKS AND ASSIGN SCORE VALUES TO PARCELS THAT INTERSECT WITH THEM
    # filter to only use blocks with a pop density greater than the user iput
    popDensityQuery = f'"popdensity" > {pop_densityValue}'
    # filter layer so that we are only using blocks that represent the query in our buffer function
    filteredPopDensity = filterByQuery(clipped_layers, "Population_Density", popDensityQuery)
    # create the buffers and assign scores
    pop_density_buffers = getBufferGeometry(filteredPopDensity, [(0, 1), (2500, 0.7), (5000, 0.3)])
    updatedParcels = updateParcelLayer(updatedParcels, "Pop_Density_Score", pop_density_buffers, pop_densityWeight)

    #CALCULATE SUITABILITY SCORE\
    updatedParcels.startEditing()

    # create a new suitability field
    new_field = QgsField("Suitability", QVariant.Double)
    updatedParcels.dataProvider().addAttributes([new_field])
    updatedParcels.updateFields()

    # find the index of the suitability field
    suitabilityIndex = updatedParcels.fields().indexOf("Suitability")

    #find the index of the transit_score field
    transitIndex = updatedParcels.fields().indexOf("Transit_Score")

    # loop through parcels and calculate the suitability score
    for parcel in updatedParcels.getFeatures():
        suitability = parcel.attribute("Pop_Density_Score") + parcel.attribute("Poverty_Score")
        # if there is a transit layer, add the transit score to the suitability score
        if transitIndex != -1:
            suitability += suitability + parcel.attribute("Transit_Score")
        updatedParcels.changeAttributeValue(parcel.id(), suitabilityIndex, suitability)

    updatedParcels.commitChanges()

    QgsVectorFileWriter.writeAsVectorFormat(updatedParcels, outputFile, "utf-8", updatedParcels.crs(), "GPKG")


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

#FUNCTION TO GET THE TRANSPORTATION STOPS FILE FROM THE USER
def selectTransitGPKGFile():
    fileName, _ = QFileDialog.getOpenFileName(mainWindow,"Select GPKG file", "","GPKG (*.gpkg)")
    if fileName:
        ui.transitLineEdit.setText(fileName)

#FUNCTION TO GET THE PANTRY LOCATIONS FILE FROM THE USER
def selectPantryGPKGFile():
    fileName, _ = QFileDialog.getOpenFileName(mainWindow,"Select GPKG file", "","GPKG (*.gpkg)")
    if fileName:
        ui.pantryLineEdit.setText(fileName)

def selectAOIFile():
    fileName, _ = QFileDialog.getOpenFileName(mainWindow,"Select GPKG file", "","GPKG (*.gpkg)")
    if fileName:
        ui.AOIlineEdit.setText(fileName)

def selectOutputfile():    # get the output filename for areal features from the user and add the path to the text box
    fileName, _ = QFileDialog.getSaveFileName(mainWindow, "Save new output file as", "", "GPKG (*.gpkg)")
    if fileName:
        ui.OutputlineEdit.setText(fileName)

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
    mainWindow.ui = ui

    # ==========================================
    # connect signals
    # ==========================================
    ui.parcelsTB.clicked.connect(selectParcelGPKGfile)
    ui.povertyTB.clicked.connect(selectPovertyGPKGFile)
    ui.pop_densityTB.clicked.connect(selectPopDensityGPKGFile)
    ui.transitTB.clicked.connect(selectTransitGPKGFile)
    ui.pantryTB.clicked.connect(selectPantryGPKGFile)
    ui.outputTB.clicked.connect(selectOutputfile)
    ui.buttonBox.accepted.connect(findSuitableParcels)
    ui.buttonBox.rejected.connect(mainWindow.close)
    ui.actionExit.triggered.connect(mainWindow.close)
    # =======================================
    # run app
    # =======================================
    mainWindow.show()

    sys.exit(app.exec_())
