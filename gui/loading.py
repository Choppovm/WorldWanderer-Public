from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class WorldWandererUILoadingPage(object):
    def setupUi(self, WorldWandererLoadingPage):
        # Main window properties (dynamic depending on screen size)
        WorldWandererLoadingPage.setObjectName("WorldWandererLoadingPage")
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        WorldWandererLoadingPage.setFixedSize(int(screen.width() * 0.4), int(screen.height() * 0.4))
        WorldWandererLoadingPage.setAutoFillBackground(False)

        # Central widget: "glues" all parts together
        self.centralwidget = QtWidgets.QWidget(WorldWandererLoadingPage)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")

        # Create main horizontal layout for whole window
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(20)

        # Main frame: holds all content
        self.mainFrame = QtWidgets.QFrame(self.centralwidget)
        self.mainFrame.setAutoFillBackground(True)
        self.mainFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.mainFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.mainFrame.setLineWidth(3)
        self.mainFrame.setObjectName("mainFrame")

        # Layout for main frame (dynamic depending on window size)
        self.frameLayout = QtWidgets.QVBoxLayout(self.mainFrame)
        self.frameLayout.setContentsMargins(20, 20, 20, 20)
        self.frameLayout.setSpacing(20)

        # Loading label
        self.labelLoadingTitle = QtWidgets.QLabel(self.mainFrame)
        fontTitle = QtGui.QFont()
        fontTitle.setPointSize(18)
        fontTitle.setBold(True)
        fontTitle.setWeight(75)
        self.labelLoadingTitle.setFont(fontTitle)
        self.labelLoadingTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLoadingTitle.setWordWrap(True)
        self.labelLoadingTitle.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.labelLoadingTitle.setObjectName("labelLoadingTitle")

        # Description label
        self.labelLoadingDescription = QtWidgets.QLabel(self.mainFrame)
        fontDesc = QtGui.QFont()
        fontDesc.setPointSize(11)
        self.labelLoadingDescription.setFont(fontDesc)
        self.labelLoadingDescription.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLoadingDescription.setWordWrap(True)
        self.labelLoadingDescription.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.labelLoadingDescription.setObjectName("labelLoadingDescription")

        # Center labels vertically by adding stretchable spacers
        self.frameLayout.addStretch(1)
        self.frameLayout.addWidget(self.labelLoadingTitle)
        self.frameLayout.addWidget(self.labelLoadingDescription)
        self.frameLayout.addStretch(1)


        # Add frame to main layout
        self.mainLayout.addWidget(self.mainFrame)

        # Set central widget
        WorldWandererLoadingPage.setCentralWidget(self.centralwidget)

        # Set texts for UI elements
        self.retranslateUi(WorldWandererLoadingPage)
        QtCore.QMetaObject.connectSlotsByName(WorldWandererLoadingPage)

    # Required to set texts for UI elements
    def retranslateUi(self, WorldWandererLoadingPage):
        translate = QtCore.QCoreApplication.translate
        WorldWandererLoadingPage.setWindowTitle(translate("WorldWandererLoadingPage", "MainWindow"))
        self.labelLoadingDescription.setText(translate("WorldWandererLoadingPage", "WorldWanderer is loading. Please wait - this shouldn't take longer than a few seconds."))
        self.labelLoadingTitle.setText(translate("WorldWandererLoadingPage", "Loading..."))

# Main function to run application
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    WorldWandererLoadingPage = QtWidgets.QMainWindow()
    ui = WorldWandererUILoadingPage()
    ui.setupUi(WorldWandererLoadingPage)
    WorldWandererLoadingPage.show()
    QtCore.QTimer.singleShot(100, lambda: print("[gui/loading.py] RENDERED", flush=True)) # Tells app.py to start the web app ONLY AFTER the GUI has rendered fully
    sys.exit(app.exec_())
