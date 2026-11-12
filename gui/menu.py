from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
import sys

class WorldWandererUI(object):
    def setupUi(self, WorldWanderer):
        # Main window properties (dynamic depending on screen size)
        WorldWanderer.setObjectName("WorldWanderer")
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        WorldWanderer.setFixedSize(int(screen.width() * 0.6), int(screen.height() * 0.6))

        # # Central widget: "glues" all parts together
        self.centralwidget = QtWidgets.QWidget(WorldWanderer)
        WorldWanderer.setCentralWidget(self.centralwidget)

        # Create main layout for whole window
        mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Title label
        self.label = QtWidgets.QLabel("WorldWanderer")
        font = QtGui.QFont()
        font.setPointSize(44)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        mainLayout.addWidget(self.label)

        # Play button
        self.pushButton1 = QtWidgets.QPushButton("Play")
        self.pushButton1.setFont(QtGui.QFont("", 21))
        self.pushButton1.clicked.connect(self.playButtonBackend)
        
        mainLayout.addWidget(self.pushButton1)

        # Row for Leaderboard and Credits buttons
        row1 = QtWidgets.QHBoxLayout()
        self.pushButton3 = QtWidgets.QPushButton("Credits")
        self.pushButton3.setFont(QtGui.QFont("", 21))
        self.pushButton3.clicked.connect(self.creditsButtonBackend)
        self.pushButton2 = QtWidgets.QPushButton("Leaderboard")
        self.pushButton2.setFont(QtGui.QFont("", 18))
        self.pushButton2.clicked.connect(self.leaderboardButtonBackend)
        row1.addWidget(self.pushButton3)
        row1.addWidget(self.pushButton2)
        mainLayout.addLayout(row1)

        # GitHub Repository button
        self.pushButton4 = QtWidgets.QPushButton("Open-Source GitHub Repository")
        self.pushButton4.setFont(QtGui.QFont("", 16))
        self.pushButton4.clicked.connect(self.githubrepoButtonBackend)
        mainLayout.addWidget(self.pushButton4)

        # Set text for UI elements
        self.retranslateUi(WorldWanderer)
        QtCore.QMetaObject.connectSlotsByName(WorldWanderer)

    # Required to set text for UI elements
    def retranslateUi(self, WorldWanderer):
        translate = QtCore.QCoreApplication.translate
        WorldWanderer.setWindowTitle(translate("WorldWanderer", "WorldWanderer: Main Menu"))
    
    def playButtonBackend(self):
        print("[gui/menu.py] PLAYBUTTONCLICKED") # Tells app.py to close main menu and go through loading process
        QtWidgets.QApplication.quit()
    
    def creditsButtonBackend(self):
        print("[gui/menu.py] CREDITSBUTTONCLICKED") # Tells app.py to close main menu and open gui/credits.py
        QtWidgets.QApplication.quit()
    
    def leaderboardButtonBackend(self):
        print("[gui/menu.py] LEADERBOARDBUTTONCLICKED") # Tells app.py to close main menu and open gui/credits.py
        QtWidgets.QApplication.quit()
    
    def githubrepoButtonBackend(self):
        url = QUrl("https://github.com/Choppovm/WorldWanderer")
        QDesktopServices.openUrl(url)
        return

# Main function to run the application.
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    WorldWanderer = QtWidgets.QMainWindow()
    ui = WorldWandererUI()
    ui.setupUi(WorldWanderer)
    WorldWanderer.show()
    sys.exit(app.exec_())
