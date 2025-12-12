import geopandas as gpd
import pandas as pd
import qgis
import qgis.core
from qgis.core import QgsVectorLayer, QgsApplication
import sys,os
from PyQt5.QtWidgets import QApplication, QMainWindow, QStyle, QFileDialog, QDialog, QMessageBox, QSizePolicy
from PyQt5.QtGui import QStandardItemModel, QStandardItem,  QDoubleValidator, QIntValidator
from PyQt5.QtCore import Qt

app = QApplication(sys.argv)
qgis_prefix = os.getenv("QGIS_PREFIX_PATH")
qgs = qgis.core.QgsApplication([], False)
qgs.initQgis()


# HARDCODED INPUT FILES
buildings = r"C:\Users\Sarah\Documents\GitHub\geog489-final\buildings.gpkg"
roads = r"C:\Users\Sarah\Documents\GitHub\geog489-final\streets.gpkg"
tree_cover = r"C:\Users\Sarah\Documents\GitHub\geog489-final\tree_canopy.gpkg"
pop_density = r"C:\Users\Sarah\Documents\GitHub\geog489-final\popdensity.gpkg"
transit_stops = r"C:\Users\Sarah\Documents\GitHub\geog489-final\bus_stops.gpkg"
existing_pantries = r"C:\Users\Sarah\Documents\GitHub\geog489-final\pantries.gpkg"

# Create QGIS Vector Layers - we might want to create a class for this where we can check if the layer is valid
buildings_layer = qgis.core.QgsVectorLayer(buildings, "Buildings", "ogr")
roads_layer = qgis.core.QgsVectorLayer(roads, "Roads", "ogr")
tree_cover_layer = qgis.core.QgsVectorLayer(tree_cover, "Tree Cover", "ogr")
pop_density_layer = qgis.core.QgsVectorLayer(pop_density, "Population Density", "ogr")
transit_stops_layer = qgis.core.QgsVectorLayer(transit_stops, "Transit Stops", "ogr")
existing_pantries_layer = qgis.core.QgsVectorLayer(existing_pantries, "Existing Pantries", "ogr")

