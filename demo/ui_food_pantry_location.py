# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'food_pantry_locationFmtPXf.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import Qt, QRect, QMetaObject, QCoreApplication, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMenuBar, QStatusBar, QHBoxLayout, QSizePolicy, QVBoxLayout, QGridLayout, QLineEdit, QLabel, QFrame, QToolButton, QSpacerItem, QLayout, QDialogButtonBox, QAction, QMenu, QComboBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem,  QDoubleValidator, QIntValidator, QFont
from qgis.gui import QgsMapCanvas, QgsMapToolZoom, QgsMapToolPan


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(925, 592)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.horizontalLayout_9 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(8)
        self.gridLayout.setVerticalSpacing(11)
        self.gridLayout.setContentsMargins(17, 0, 3, -1)
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(0, 30))
        self.label_6.setAcceptDrops(False)
        self.label_6.setWordWrap(True)

        self.gridLayout.addWidget(self.label_6, 12, 0, 1, 1)

        self.pantryTB = QToolButton(self.centralwidget)
        self.pantryTB.setObjectName(u"pantryTB")

        self.gridLayout.addWidget(self.pantryTB, 12, 2, 1, 1)

        self.parcelsLineEdit = QLineEdit(self.centralwidget)
        self.parcelsLineEdit.setObjectName(u"parcelsLineEdit")

        self.gridLayout.addWidget(self.parcelsLineEdit, 1, 1, 1, 1)

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_3, 9, 1, 1, 1)

        self.pop_densityLineEdit = QLineEdit(self.centralwidget)
        self.pop_densityLineEdit.setObjectName(u"pop_densityLineEdit")

        self.gridLayout.addWidget(self.pop_densityLineEdit, 7, 1, 1, 1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setSpacing(20)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_10.addWidget(self.label_10)

        self.pop_densityCB = QComboBox(self.centralwidget)
        self.pop_densityCB.setObjectName(u"pop_densityCB")

        self.horizontalLayout_10.addWidget(self.pop_densityCB)

        self.label_17 = QLabel(self.centralwidget)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setWordWrap(False)

        self.horizontalLayout_10.addWidget(self.label_17)

        self.pop_densityValLineEdit = QLineEdit(self.centralwidget)
        self.pop_densityValLineEdit.setObjectName(u"pop_densityValLineEdit")

        self.horizontalLayout_10.addWidget(self.pop_densityValLineEdit)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 20))
        self.label_2.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout_10.addWidget(self.label_2)

        self.pop_density_weightLineEdit = QLineEdit(self.centralwidget)
        self.pop_density_weightLineEdit.setObjectName(u"pop_density_weightLineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pop_density_weightLineEdit.sizePolicy().hasHeightForWidth())
        self.pop_density_weightLineEdit.setSizePolicy(sizePolicy)

        self.horizontalLayout_10.addWidget(self.pop_density_weightLineEdit)

        self.horizontalLayout_10.setStretch(0, 1)
        self.horizontalLayout_10.setStretch(1, 2)
        self.horizontalLayout_10.setStretch(2, 1)
        self.horizontalLayout_10.setStretch(3, 1)
        self.horizontalLayout_10.setStretch(4, 1)
        self.horizontalLayout_10.setStretch(5, 1)

        self.gridLayout.addLayout(self.horizontalLayout_10, 8, 1, 1, 1)

        self.AOIlineEdit = QLineEdit(self.centralwidget)
        self.AOIlineEdit.setObjectName(u"AOIlineEdit")

        self.gridLayout.addWidget(self.AOIlineEdit, 0, 1, 1, 1)

        self.parcelsLabel = QLabel(self.centralwidget)
        self.parcelsLabel.setObjectName(u"parcelsLabel")
        self.parcelsLabel.setMinimumSize(QSize(0, 30))

        self.gridLayout.addWidget(self.parcelsLabel, 1, 0, 1, 1)

        self.transitLineEdit = QLineEdit(self.centralwidget)
        self.transitLineEdit.setObjectName(u"transitLineEdit")

        self.gridLayout.addWidget(self.transitLineEdit, 10, 1, 1, 1)

        self.povertyLabel = QLabel(self.centralwidget)
        self.povertyLabel.setObjectName(u"povertyLabel")
        self.povertyLabel.setMinimumSize(QSize(0, 30))
        self.povertyLabel.setWordWrap(True)

        self.gridLayout.addWidget(self.povertyLabel, 5, 0, 1, 1)

        self.OutputlineEdit = QLineEdit(self.centralwidget)
        self.OutputlineEdit.setObjectName(u"OutputlineEdit")

        self.gridLayout.addWidget(self.OutputlineEdit, 15, 1, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 30))

        self.gridLayout.addWidget(self.label_3, 7, 0, 1, 1)

        self.povertyTB = QToolButton(self.centralwidget)
        self.povertyTB.setObjectName(u"povertyTB")

        self.gridLayout.addWidget(self.povertyTB, 5, 2, 1, 1)

        self.label_19 = QLabel(self.centralwidget)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout.addWidget(self.label_19, 0, 0, 1, 1)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_2, 3, 1, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(11)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(100, 0))
        self.label_7.setMargin(4)

        self.horizontalLayout_4.addWidget(self.label_7)

        self.transit_weightLineEdit = QLineEdit(self.centralwidget)
        self.transit_weightLineEdit.setObjectName(u"transit_weightLineEdit")
        sizePolicy.setHeightForWidth(self.transit_weightLineEdit.sizePolicy().hasHeightForWidth())
        self.transit_weightLineEdit.setSizePolicy(sizePolicy)
        self.transit_weightLineEdit.setInputMethodHints(Qt.ImhNone)

        self.horizontalLayout_4.addWidget(self.transit_weightLineEdit)


        self.gridLayout.addLayout(self.horizontalLayout_4, 11, 1, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 15, 0, 1, 1)

        self.parcelsTB = QToolButton(self.centralwidget)
        self.parcelsTB.setObjectName(u"parcelsTB")

        self.gridLayout.addWidget(self.parcelsTB, 1, 2, 1, 1)

        self.pop_densityTB = QToolButton(self.centralwidget)
        self.pop_densityTB.setObjectName(u"pop_densityTB")

        self.gridLayout.addWidget(self.pop_densityTB, 7, 2, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setSpacing(20)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_11.addWidget(self.label_5)

        self.povertyCB = QComboBox(self.centralwidget)
        self.povertyCB.setObjectName(u"povertyCB")

        self.horizontalLayout_11.addWidget(self.povertyCB)

        self.label_18 = QLabel(self.centralwidget)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_11.addWidget(self.label_18)

        self.povertyValLineEdit = QLineEdit(self.centralwidget)
        self.povertyValLineEdit.setObjectName(u"povertyValLineEdit")

        self.horizontalLayout_11.addWidget(self.povertyValLineEdit)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(100, 20))
        self.label_8.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout_11.addWidget(self.label_8)

        self.poverty_weightLineEdit = QLineEdit(self.centralwidget)
        self.poverty_weightLineEdit.setObjectName(u"poverty_weightLineEdit")

        self.horizontalLayout_11.addWidget(self.poverty_weightLineEdit)

        self.horizontalLayout_11.setStretch(0, 1)
        self.horizontalLayout_11.setStretch(1, 2)
        self.horizontalLayout_11.setStretch(2, 1)
        self.horizontalLayout_11.setStretch(3, 1)
        self.horizontalLayout_11.setStretch(4, 1)
        self.horizontalLayout_11.setStretch(5, 1)

        self.gridLayout.addLayout(self.horizontalLayout_11, 6, 1, 1, 1)

        self.transitTB = QToolButton(self.centralwidget)
        self.transitTB.setObjectName(u"transitTB")

        self.gridLayout.addWidget(self.transitTB, 10, 2, 1, 1)

        self.line_4 = QFrame(self.centralwidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_4, 14, 1, 1, 1)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 30))
        self.label_4.setMaximumSize(QSize(121, 16777215))
        self.label_4.setWordWrap(True)

        self.gridLayout.addWidget(self.label_4, 10, 0, 1, 1)

        self.povertyLineEdit = QLineEdit(self.centralwidget)
        self.povertyLineEdit.setObjectName(u"povertyLineEdit")

        self.gridLayout.addWidget(self.povertyLineEdit, 5, 1, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(50, 0))
        self.label_9.setMargin(4)

        self.horizontalLayout_6.addWidget(self.label_9)

        self.pantry_distLineEdit = QLineEdit(self.centralwidget)
        self.pantry_distLineEdit.setObjectName(u"pantry_distLineEdit")

        self.horizontalLayout_6.addWidget(self.pantry_distLineEdit)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)


        self.gridLayout.addLayout(self.horizontalLayout_6, 13, 1, 1, 1)

        self.outputTB = QToolButton(self.centralwidget)
        self.outputTB.setObjectName(u"outputTB")

        self.gridLayout.addWidget(self.outputTB, 15, 2, 1, 1)

        self.pantryLineEdit = QLineEdit(self.centralwidget)
        self.pantryLineEdit.setObjectName(u"pantryLineEdit")

        self.gridLayout.addWidget(self.pantryLineEdit, 12, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(16)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_2.addWidget(self.label_11)

        self.parcelsFieldCB = QComboBox(self.centralwidget)
        self.parcelsFieldCB.setObjectName(u"parcelsFieldCB")

        self.horizontalLayout_2.addWidget(self.parcelsFieldCB)

        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_2.addWidget(self.label_12)

        self.parcelsValueCB = QComboBox(self.centralwidget)
        self.parcelsValueCB.setObjectName(u"parcelsValueCB")

        self.horizontalLayout_2.addWidget(self.parcelsValueCB)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 3)
        self.horizontalLayout_2.setStretch(2, 1)
        self.horizontalLayout_2.setStretch(3, 3)

        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout)

        self.buttonBox = QDialogButtonBox(self.centralwidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_3.addWidget(self.buttonBox)


        self.horizontalLayout_5.addLayout(self.verticalLayout_3)


        self.horizontalLayout_9.addLayout(self.horizontalLayout_5)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 925, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
#if QT_CONFIG(tooltip)
        self.label_6.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>GeoPackage file containing existing pantry location data. </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Current Pantry \n"
"Locations File (Optional)", None))
#if QT_CONFIG(tooltip)
        self.pantryTB.setToolTip(QCoreApplication.translate("MainWindow", u"Choose GeoPackage file", None))
#endif // QT_CONFIG(tooltip)
        self.pantryTB.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.parcelsLineEdit.setToolTip(QCoreApplication.translate("MainWindow", u"GeoPackage file containing land parcels. (Currently hard-coded to filter parcels to COMMERCIAL-RETAIL)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pop_densityLineEdit.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>GeoPackage containing poverty data. (Currently hardcoded to pull data from 'popdensity' field)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_10.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The field with the population density values.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Target Field", None))
#if QT_CONFIG(tooltip)
        self.pop_densityCB.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The field with population density values. </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_17.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The population density value used to extract tracts from population density GPKG for buffering. </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Target Population Density (>=)", None))
#if QT_CONFIG(tooltip)
        self.pop_densityValLineEdit.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The population density value used to extract tracts from population density GPKG for buffering. </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pop_densityValLineEdit.setText(QCoreApplication.translate("MainWindow", u"5000", None))
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Weight to assign to population density data. Default = 30%</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Weight (1 - 100)%", None))
#if QT_CONFIG(tooltip)
        self.pop_density_weightLineEdit.setToolTip(QCoreApplication.translate("MainWindow", u"Weight to assign to population density data. Default = 30%", None))
#endif // QT_CONFIG(tooltip)
        self.pop_density_weightLineEdit.setText(QCoreApplication.translate("MainWindow", u"30", None))
#if QT_CONFIG(tooltip)
        self.AOIlineEdit.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>List of coordinates to define the area of interest. Should be in the format (lat1, lon1), (lat2, lon2),...</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.AOIlineEdit.setText(QCoreApplication.translate("MainWindow", u"(39.76876, -104.99517), (39.77292, -104.97323), (39.74882, -104.97323), (39.75144, -104.99517)", None))
#if QT_CONFIG(tooltip)
        self.parcelsLabel.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>GeoPackage file containing land parcels. (Currently hard-coded to filter parcels to COMMERCIAL-RETAIL)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.parcelsLabel.setText(QCoreApplication.translate("MainWindow", u"Parcel File", None))
#if QT_CONFIG(tooltip)
        self.transitLineEdit.setToolTip(QCoreApplication.translate("MainWindow", u"GeoPackage containing transit stop data. ", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.povertyLabel.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>GeoPackage containing poverty data. (Currently hardcoded to pull data from 'Percent_Po' field)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.povertyLabel.setText(QCoreApplication.translate("MainWindow", u"Poverty Data File", None))
#if QT_CONFIG(tooltip)
        self.OutputlineEdit.setToolTip(QCoreApplication.translate("MainWindow", u"The output file of parcel data with suitability scores. ", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>GeoPackage containing poverty data. (Currently hardcoded to pull data from 'popdensity' field)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Population Density File", None))
#if QT_CONFIG(tooltip)
        self.povertyTB.setToolTip(QCoreApplication.translate("MainWindow", u"Choose GeoPackage file", None))
#endif // QT_CONFIG(tooltip)
        self.povertyTB.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.label_19.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>List of coordinates to define the area of interest. Should be in the format (lat1, lon1), (lat2, lon2),...</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Area of Interest", None))
#if QT_CONFIG(tooltip)
        self.label_7.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Weight to assign to transit stop data</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Weight (1 - 100)%", None))
#if QT_CONFIG(tooltip)
        self.transit_weightLineEdit.setToolTip(QCoreApplication.translate("MainWindow", u"Weight to assign to transit stop data", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The output file of parcel data with suitability scores. </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("MainWindow", u"Output File", None))
#if QT_CONFIG(tooltip)
        self.parcelsTB.setToolTip(QCoreApplication.translate("MainWindow", u"Choose GeoPackage file", None))
#endif // QT_CONFIG(tooltip)
        self.parcelsTB.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.pop_densityTB.setToolTip(QCoreApplication.translate("MainWindow", u"Choose GeoPackage file", None))
#endif // QT_CONFIG(tooltip)
        self.pop_densityTB.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.label_5.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The field with poverty values (i.e. percent poverty, income below poverty level, etc.)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Target Field ", None))
#if QT_CONFIG(tooltip)
        self.povertyCB.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The field with poverty values (i.e. percent poverty, income below poverty level, etc.)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_18.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The poverty value used to extract tracts from poverty GPKG for buffering. </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Target Poverty Value (>=)", None))
#if QT_CONFIG(tooltip)
        self.povertyValLineEdit.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The poverty value used to extract tracts from poverty GPKG for buffering. </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.povertyValLineEdit.setText(QCoreApplication.translate("MainWindow", u"20", None))
#if QT_CONFIG(tooltip)
        self.label_8.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Weight to assign to poverty data. Default = 70%</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Weight (1 - 100)%", None))
#if QT_CONFIG(tooltip)
        self.poverty_weightLineEdit.setToolTip(QCoreApplication.translate("MainWindow", u"Weight to assign to poverty data. Default = 70%", None))
#endif // QT_CONFIG(tooltip)
        self.poverty_weightLineEdit.setText(QCoreApplication.translate("MainWindow", u"70", None))
#if QT_CONFIG(tooltip)
        self.transitTB.setToolTip(QCoreApplication.translate("MainWindow", u"Choose GeoPackage file", None))
#endif // QT_CONFIG(tooltip)
        self.transitTB.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>GeoPackage containing transit stop data. </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Transit Stops File (Optional)", None))
#if QT_CONFIG(tooltip)
        self.povertyLineEdit.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>GeoPackage containing poverty data.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_9.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The buffer distance around existing pantries (i.e. to determine suitable parcels outside of a distance from exisitng pantries) ** This tool uses layers with map units in feet</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Min Distance (miles)", None))
#if QT_CONFIG(tooltip)
        self.pantry_distLineEdit.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The buffer distance around existing pantries (i.e. to determine suitable parcels outside of a distance from exisitng pantries) ** This tool uses layers with map units in feet</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.outputTB.setToolTip(QCoreApplication.translate("MainWindow", u"Save file to...", None))
#endif // QT_CONFIG(tooltip)
        self.outputTB.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.pantryLineEdit.setToolTip(QCoreApplication.translate("MainWindow", u"GeoPackage file containing existing pantry location data. ", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_11.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The field that contains the value to use for filtering parcels. </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Target Field", None))
#if QT_CONFIG(tooltip)
        self.parcelsFieldCB.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The field that contains the value to use for filtering parcels. </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_12.setToolTip(QCoreApplication.translate("MainWindow", u"The value to use for filtering parcels. ", None))
#endif // QT_CONFIG(tooltip)
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Target Value", None))
#if QT_CONFIG(tooltip)
        self.parcelsValueCB.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The value to use for filtering parcels. </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi








