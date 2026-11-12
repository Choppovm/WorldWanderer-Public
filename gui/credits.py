from PyQt5 import QtCore, QtGui, QtWidgets

class WorldWandererUI(object):
    # Sets up GUI layout
    def setupUi(self, WorldWanderer):
        WorldWanderer.setObjectName("WorldWanderer")
        # Main window properties (dynamic depending on screen size)
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        WorldWanderer.setFixedSize(int(screen.width() * 0.6), int(screen.height() * 0.6))
        WorldWanderer.setAutoFillBackground(False)

        # Formats
        def textLabel(pointSize=10, box=True, alignCenter=True, wordWrap=True, lineWidth=1):
            lbl = QtWidgets.QLabel()
            font = QtGui.QFont()
            font.setPointSize(pointSize)
            lbl.setFont(font)
            if box:
                lbl.setFrameShape(QtWidgets.QFrame.Box)
                lbl.setLineWidth(lineWidth)
            if alignCenter:
                lbl.setAlignment(QtCore.Qt.AlignCenter)
            lbl.setWordWrap(bool(wordWrap))
            return lbl

        def banner(path, height=100, lineWidth=1):
            lbl = QtWidgets.QLabel()
            lbl.setFrameShape(QtWidgets.QFrame.Box)
            lbl.setLineWidth(lineWidth)
            lbl.setAlignment(QtCore.Qt.AlignCenter)
            lbl.setScaledContents(False)
            lbl.setMinimumHeight(height)
            lbl.setPixmap(
                QtGui.QPixmap(path).scaledToHeight(height, QtCore.Qt.SmoothTransformation)
            )
            return lbl

        def icon(path, size=64, lineWidth=1):
            lbl = QtWidgets.QLabel()
            lbl.setFrameShape(QtWidgets.QFrame.Box)
            lbl.setLineWidth(lineWidth)
            lbl.setAlignment(QtCore.Qt.AlignCenter)
            lbl.setPixmap(
                QtGui.QPixmap(path).scaled(size, size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            )
            return lbl

        def hLine(width=2):
            line = QtWidgets.QFrame()
            line.setFrameShape(QtWidgets.QFrame.HLine)
            line.setFrameShadow(QtWidgets.QFrame.Plain)
            line.setLineWidth(width)
            return line

        def vLine(width=2, expanding=True):
            line = QtWidgets.QFrame()
            line.setFrameShape(QtWidgets.QFrame.VLine)
            line.setFrameShadow(QtWidgets.QFrame.Plain)
            line.setLineWidth(width)
            if expanding:
                line.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
            return line

        # Central widget: "glues" all parts together
        self.centralwidget = QtWidgets.QWidget(WorldWanderer)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        WorldWanderer.setCentralWidget(self.centralwidget)

        # Create main vertical layout for whole window
        self.mainVerticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainVerticalLayout.setContentsMargins(16, 16, 16, 16)
        self.mainVerticalLayout.setSpacing(16)

        # Create main outer frame for GUI's contents with border
        self.mainFrame = QtWidgets.QFrame()
        self.mainFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.mainFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.mainFrame.setLineWidth(3)
        self.mainFrame.setObjectName("mainFrame")
        self.mainVerticalLayout.addWidget(self.mainFrame)

        # Content layout inside the main frame
        self.contentVerticalLayout = QtWidgets.QVBoxLayout(self.mainFrame)
        self.contentVerticalLayout.setContentsMargins(16, 16, 16, 16)
        self.contentVerticalLayout.setSpacing(16)

        # Title label creation
        self.title = textLabel(pointSize=28, lineWidth=2)
        self.title.setObjectName("title")
        self.contentVerticalLayout.addWidget(self.title)

        # Banners (Leaflet.js and Mapillary) row container
        self.bannersRowWidget = QtWidgets.QWidget()
        self.bannersRowLayout = QtWidgets.QHBoxLayout(self.bannersRowWidget)
        self.bannersRowLayout.setContentsMargins(0, 0, 0, 0)
        self.bannersRowLayout.setSpacing(12)

        # Leaflet.js banner
        self.leafletjsIconPlaceholder = banner("WorldWanderer-main/assets/images/bannerLogos/leafletjsLogoBanner.png")
        self.leafletjsIconPlaceholder.setObjectName("leafletjsIconPlaceholder")
        self.bannersRowLayout.addWidget(self.leafletjsIconPlaceholder)

        # Mapillary banner
        self.mapillarybannerIconPlaceholder = banner("WorldWanderer-main/assets/images/bannerLogos/mapillaryLogoBanner.png")
        self.mapillarybannerIconPlaceholder.setObjectName("mapillarybannerIconPlaceholder")
        self.bannersRowLayout.addWidget(self.mapillarybannerIconPlaceholder)

        # Add row to content layout
        self.contentVerticalLayout.addWidget(self.bannersRowWidget)

        # Banner (leaflet + mapillary) description row container
        self.bannersDescRowWidget = QtWidgets.QWidget()
        self.bannersDescRowLayout = QtWidgets.QHBoxLayout(self.bannersDescRowWidget)
        self.bannersDescRowLayout.setContentsMargins(0, 0, 0, 0)
        self.bannersDescRowLayout.setSpacing(12)

        # Leaflet.js description
        self.leafletjsDescription = textLabel(pointSize=10)
        self.leafletjsDescription.setObjectName("leafletjsDescription")
        self.bannersDescRowLayout.addWidget(self.leafletjsDescription)

        # Mapillary description
        self.mapillaryDescription = textLabel(pointSize=10)
        self.mapillaryDescription.setObjectName("mapillaryDescription")
        self.bannersDescRowLayout.addWidget(self.mapillaryDescription)

        # Add row to content layout
        self.contentVerticalLayout.addWidget(self.bannersDescRowWidget)

        # Horizontal divider
        self.horizontalLine = hLine(width=2)
        self.contentVerticalLayout.addWidget(self.horizontalLine)

        # Tech section
        self.techSectionWidget = QtWidgets.QWidget()
        self.techGrid = QtWidgets.QGridLayout(self.techSectionWidget)
        self.techGrid.setContentsMargins(0, 0, 0, 0)
        self.techGrid.setHorizontalSpacing(12)
        self.techGrid.setVerticalSpacing(8)

        # Left column (OSM)
        self.osmRowWidget = QtWidgets.QWidget()
        self.osmRowLayout = QtWidgets.QHBoxLayout(self.osmRowWidget)
        self.osmRowLayout.setContentsMargins(0, 0, 0, 0)
        self.osmRowLayout.setSpacing(8)

        self.osmIconPlaceholder = icon("WorldWanderer-main/assets/images/iconLogos/osmLogo.png")
        self.osmIconPlaceholder.setObjectName("osmIconPlaceholder")
        self.osmRowLayout.addWidget(self.osmIconPlaceholder)

        self.osmTitleHYPERLINK = textLabel(pointSize=8)
        self.osmTitleHYPERLINK.setObjectName("osmTitleHYPERLINK")
        self.osmRowLayout.addWidget(self.osmTitleHYPERLINK)

        # Right column (PyQt)
        self.pyqtRowWidget = QtWidgets.QWidget()
        self.pyqtRowLayout = QtWidgets.QHBoxLayout(self.pyqtRowWidget)
        self.pyqtRowLayout.setContentsMargins(0, 0, 0, 0)
        self.pyqtRowLayout.setSpacing(8)

        self.pyqtIconPlaceholder = icon("WorldWanderer-main/assets/images/iconLogos/pyqtLogo.png")
        self.pyqtIconPlaceholder.setObjectName("pyqtIconPlaceholder")
        self.pyqtRowLayout.addWidget(self.pyqtIconPlaceholder)

        self.pyqtTitleHYPERLINK = textLabel(pointSize=8)
        self.pyqtTitleHYPERLINK.setObjectName("pyqtTitleHYPERLINK")
        self.pyqtRowLayout.addWidget(self.pyqtTitleHYPERLINK)

        # Vertical divider
        self.verticalLine = vLine(width=2, expanding=True)

        # Descriptions
        self.osmDescription = textLabel(pointSize=8)
        self.osmDescription.setObjectName("osmDescription")
        self.osmDescription.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.pyqtDescription = textLabel(pointSize=8)
        self.pyqtDescription.setObjectName("pyqtDescription")
        self.pyqtDescription.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        # Assemble grid columns
        self.techGrid.addWidget(self.osmRowWidget, 0, 0)
        self.techGrid.addWidget(self.verticalLine, 0, 1, 2, 1)
        self.techGrid.addWidget(self.pyqtRowWidget, 0, 2)

        self.techGrid.addWidget(self.osmDescription, 1, 0)
        self.techGrid.addWidget(self.pyqtDescription, 1, 2)

        # Equal column width for 0 and 2
        self.techGrid.setColumnStretch(0, 1)
        self.techGrid.setColumnStretch(2, 1)

        self.contentVerticalLayout.addWidget(self.techSectionWidget)

        # Horizontal divider
        self.horizontalLine2 = hLine(width=2)
        self.contentVerticalLayout.addWidget(self.horizontalLine2)

        # Icons row container
        self.iconsRowWidget = QtWidgets.QWidget()
        self.iconsRowLayout = QtWidgets.QHBoxLayout(self.iconsRowWidget)
        self.iconsRowLayout.setContentsMargins(0, 0, 0, 0)
        self.iconsRowLayout.setSpacing(16)

        # Python icon label
        self.pythonIconPlaceholder = icon("WorldWanderer-main/assets/images/iconLogos/pythonLogo.png")
        self.pythonIconPlaceholder.setObjectName("pythonIconPlaceholder")
        self.iconsRowLayout.addWidget(self.pythonIconPlaceholder)

        # JavaScript icon label
        self.javascriptIconPlaceholder = icon("WorldWanderer-main/assets/images/iconLogos/javascriptLogo.png")
        self.javascriptIconPlaceholder.setObjectName("javascriptIconPlaceholder")
        self.iconsRowLayout.addWidget(self.javascriptIconPlaceholder)

        # HTML icon label
        self.htmlIconPlaceholder = icon("WorldWanderer-main/assets/images/iconLogos/htmlLogo.png")
        self.htmlIconPlaceholder.setObjectName("htmlIconPlaceholder")
        self.iconsRowLayout.addWidget(self.htmlIconPlaceholder)

        # CSS icon label
        self.cssIconPlaceholder = icon("WorldWanderer-main/assets/images/iconLogos/cssLogo.png")
        self.cssIconPlaceholder.setObjectName("cssIconPlaceholder")
        self.iconsRowLayout.addWidget(self.cssIconPlaceholder)

        # Add row to content layout
        self.contentVerticalLayout.addWidget(self.iconsRowWidget)

        # Icon descriptions row container
        self.iconDescRowWidget = QtWidgets.QWidget()
        self.iconDescRowLayout = QtWidgets.QHBoxLayout(self.iconDescRowWidget)
        self.iconDescRowLayout.setContentsMargins(0, 0, 0, 0)
        self.iconDescRowLayout.setSpacing(16)

        # Python description label
        self.pythonDescription = textLabel(pointSize=8)
        self.pythonDescription.setObjectName("pythonDescription")
        self.iconDescRowLayout.addWidget(self.pythonDescription)

        # JavaScript description label
        self.javascriptDescription = textLabel(pointSize=8)
        self.javascriptDescription.setObjectName("javascriptDescription")
        self.iconDescRowLayout.addWidget(self.javascriptDescription)

        # HTML description label
        self.htmlDescription = textLabel(pointSize=8)
        self.htmlDescription.setObjectName("htmlDescription")
        self.iconDescRowLayout.addWidget(self.htmlDescription)

        # CSS description label
        self.cssDescription = textLabel(pointSize=8)
        self.cssDescription.setObjectName("cssDescription")
        self.iconDescRowLayout.addWidget(self.cssDescription)

        # Add row to content layout
        self.contentVerticalLayout.addWidget(self.iconDescRowWidget)

        # Horizontal divider
        self.horizontalLine3 = hLine(width=2)
        self.contentVerticalLayout.addWidget(self.horizontalLine3)

        # Create container for return button
        self.buttonRowWidget = QtWidgets.QWidget()
        self.buttonRowLayout = QtWidgets.QHBoxLayout(self.buttonRowWidget)
        self.buttonRowLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonRowLayout.setSpacing(12)

        # Return button
        self.returnToMainMenuButton = QtWidgets.QPushButton()
        self.returnButtonFont = QtGui.QFont()
        self.returnButtonFont.setPointSize(14)
        self.returnToMainMenuButton.setFont(self.returnButtonFont)
        self.returnToMainMenuButton.setObjectName("returnToMainMenuButton")
        self.returnToMainMenuButton.clicked.connect(self.returnToMenuBackend)
        self.buttonRowLayout.addStretch(1)
        self.buttonRowLayout.addWidget(self.returnToMainMenuButton)
        self.buttonRowLayout.addStretch(1)
        self.contentVerticalLayout.addWidget(self.buttonRowWidget)

        # Set GUI's text
        self.retranslateUi(WorldWanderer)
        QtCore.QMetaObject.connectSlotsByName(WorldWanderer)

    def returnToMenuBackend(self):
        print("[gui/credits.py] RETURNTOMENU", flush=True) # Tells app.py to return to main menu
        QtWidgets.QApplication.quit()

    # Required to set GUI's text
    def retranslateUi(self, WorldWanderer):
        translate = QtCore.QCoreApplication.translate
        WorldWanderer.setWindowTitle(translate("WorldWanderer", "MainWindow"))
        self.title.setText(translate("WorldWanderer", "Credits"))
        self.leafletjsDescription.setText(translate("WorldWanderer", "Backend for rendering OpenStreetMap"))
        self.mapillaryDescription.setText(translate("WorldWanderer", "Backend for rendering OpenStreetMap"))
        self.osmTitleHYPERLINK.setText(translate("WorldWanderer", "OpenStreetMap (+ Contributors)"))
        self.pyqtTitleHYPERLINK.setText(translate("WorldWanderer", "PyQt"))
        self.osmDescription.setText(translate("WorldWanderer", "Service used for maps (combined with Leaflet.js)"))
        self.pyqtDescription.setText(translate("WorldWanderer", "Main python library for handling GUIs"))
        self.pythonDescription.setText(translate("WorldWanderer", "Main backend"))
        self.javascriptDescription.setText(translate("WorldWanderer", "Web backend"))
        self.htmlDescription.setText(translate("WorldWanderer", "Web layout"))
        self.cssDescription.setText(translate("WorldWanderer", "Web styling"))
        self.returnToMainMenuButton.setText(translate("WorldWanderer", "Return to Main Menu"))

# Run GUI
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WorldWanderer = QtWidgets.QMainWindow()
    ui = WorldWandererUI()
    ui.setupUi(WorldWanderer)
    WorldWanderer.show()
    sys.exit(app.exec_())
