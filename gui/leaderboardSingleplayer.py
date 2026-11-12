from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
import sys
import sqlite3

class WorldWandererUI(object):
    def setupUi(self, WorldWanderer):
        WorldWanderer.setObjectName("WorldWanderer")

        # Main window properties (dynamic depending on screen size)
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        WorldWanderer.setFixedSize(int(screen.width() * 0.8), int(screen.height() * 0.8))
        WorldWanderer.setAutoFillBackground(False)

        # Central widget: container for all UI elements
        self.centralWidget = QtWidgets.QWidget(WorldWanderer)
        WorldWanderer.setCentralWidget(self.centralWidget)

        # Root vertical layout: holds header + database contents
        self.rootLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.rootLayout.setContentsMargins(16, 16, 16, 16)
        self.rootLayout.setSpacing(16)

        # Header frame: contains return button + title
        self.headerFrame = QtWidgets.QFrame(self.centralWidget)
        self.headerFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.headerFrame.setLineWidth(3)
        self.headerLayout = QtWidgets.QHBoxLayout(self.headerFrame)

        # Return to menu button
        self.returnToMenuButton = QtWidgets.QPushButton(self.headerFrame)
        self.returnToMenuFont = QtGui.QFont()
        self.returnToMenuFont.setPointSize(10)
        self.returnToMenuButton.setFont(self.returnToMenuFont)
        self.returnToMenuButton.setObjectName("returnToMenuButton")
        self.returnToMenuButton.clicked.connect(lambda: self.buttonHandler("returnToMenu"))
        self.headerLayout.addWidget(self.returnToMenuButton)
        self.headerLayout.addStretch(1)

        # Title label
        self.titleLabel = QtWidgets.QLabel(self.headerFrame)
        self.titleLabelFont = QtGui.QFont()
        self.titleLabelFont.setPointSize(28)
        self.titleLabel.setFont(self.titleLabelFont)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.titleLabel.setLineWidth(2)
        self.titleLabel.setObjectName("titleLabel")
        self.headerLayout.addWidget(self.titleLabel, stretch=3)
        self.headerLayout.addStretch(1)

        # Add header to root layout
        self.rootLayout.addWidget(self.headerFrame)

        # Database Section Frame: holds database viewer + selector (also has layout)
        self.databaseSectionFrame = QtWidgets.QFrame(self.centralWidget)
        self.databaseSectionFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.databaseSectionFrame.setLineWidth(3)
        self.databaseSectionLayout = QtWidgets.QVBoxLayout(self.databaseSectionFrame)

        # Layout for being able to select what database to view
        self.databaseSelector = QtWidgets.QLabel(self.databaseSectionFrame)
        self.databaseSelector.setFrameShape(QtWidgets.QFrame.Box)
        self.databaseSelector.setLineWidth(2)
        self.databaseSelectorLayout = QtWidgets.QHBoxLayout(self.databaseSelector)

        # Button for displaying each database
        self.databaseUserData = self.createDatabaseButton("dbUserData", "dbuserdata")
        self.databaseLeaderboard = self.createDatabaseButton("dbLeaderboard", "dbleaderboard")

        # Table for displaying database
        self.currentDatabaseTable = QTableWidget(self.databaseSectionFrame)
        self.currentDatabaseTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.currentDatabaseTable.setFrameShape(QtWidgets.QFrame.Box)
        self.currentDatabaseTable.setLineWidth(2)

        # Database display backend
        currentSelectedTable = "N/A" # current database selected
        self.loadData(currentSelectedTable)

        # Add each component to respective parent widgets
        self.databaseSectionLayout.addWidget(self.databaseSelector, stretch=1)
        self.databaseSectionLayout.addWidget(self.currentDatabaseTable, stretch=9)
        self.rootLayout.addWidget(self.databaseSectionFrame)

        # Translate UI text
        self.retranslateUi(WorldWanderer)
        QtCore.QMetaObject.connectSlotsByName(WorldWanderer)
    
    # Create a button in self.databaseSelector
    def createDatabaseButton(self, objectName, text):
        button = QtWidgets.QPushButton(self.databaseSelector)
        font = QtGui.QFont()
        font.setPointSize(12)
        button.setFont(font)
        button.setObjectName(objectName)
        button.clicked.connect(lambda _, t=text: self.buttonHandler(t)) # Lambda used to defer execution until the button is clicked

        self.databaseSelectorLayout.addWidget(button)
        return button

    # Function that handles showing databases
    def buttonHandler(self, button):
        if button == "returnToMenu":
            print("[gui/leaderboardSingleplayer.py] RETURNTOMENU", flush=True) # Tells app.py to return to main menu
            QtWidgets.QApplication.quit()
        else:
            self.loadData(button)
    
    # Function that loads data from current database
    def loadData(self, selectedTable):
        if selectedTable == "N/A":
            return
        elif selectedTable == "dbleaderboard":
            connection = sqlite3.connect("WorldWanderer-main/databases/leaderboard.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM 'leaderboard-wholeMatch' ORDER BY totalScore DESC")
            rows = cursor.fetchall()
            # Set dimensions of the QTable
            self.currentDatabaseTable.setRowCount(len(rows))
            self.currentDatabaseTable.setColumnCount(len(rows[0]))
            self.currentDatabaseTable.setHorizontalHeaderLabels(["matchID", "userID", "totalScore", "roundsPlayed", "timeLimit"])
            headerRow = self.currentDatabaseTable.horizontalHeader()
            headerRow.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
            headerRow.setStretchLastSection(False)
            headerRow.setSectionsMovable(False)
            headerCol = self.currentDatabaseTable.verticalHeader()
            headerCol.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
            headerCol.setStretchLastSection(False)
            headerCol.setSectionsMovable(False)
            # Populate table based off database
            for rowID, rowData in enumerate(rows):
                for colID, colData in enumerate(rowData):
                    self.currentDatabaseTable.setItem(rowID, colID, QTableWidgetItem(str(colData)))
            self.currentDatabaseTable.resizeColumnsToContents()
            headerRow.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
            headerRow.setStretchLastSection(False)
            headerRow.setSectionsMovable(False)
            connection.close()
        elif selectedTable == "dbuserdata":
            connection = sqlite3.connect("WorldWanderer-main/databases/leaderboard.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM 'databaseUsers'")
            rows = cursor.fetchall()
            # Set dimensions of the QTable
            self.currentDatabaseTable.setRowCount(len(rows))
            self.currentDatabaseTable.setColumnCount(len(rows[0]))
            self.currentDatabaseTable.setHorizontalHeaderLabels(["userID", "userName", "userSecretKey"])
            headerRow = self.currentDatabaseTable.horizontalHeader()
            headerRow.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
            headerRow.setStretchLastSection(False)
            headerRow.setSectionsMovable(False)
            headerCol = self.currentDatabaseTable.verticalHeader()
            headerCol.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
            headerCol.setStretchLastSection(False)
            headerCol.setSectionsMovable(False)
            # Populate table based off database
            for rowID, rowData in enumerate(rows):
                for colID, colData in enumerate(rowData):
                    if colID == 2: # if its the secret key
                        self.currentDatabaseTable.setItem(rowID, colID, QTableWidgetItem("[HIDDEN]"))
                    else:
                        self.currentDatabaseTable.setItem(rowID, colID, QTableWidgetItem(str(colData)))
            self.currentDatabaseTable.resizeColumnsToContents()
            headerRow.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
            headerRow.setStretchLastSection(False)
            headerRow.setSectionsMovable(False)
            connection.close()
        else:
            print("invalid db requested via button") # if this appears check for a typo
            return

    # Translate UI text
    def retranslateUi(self, WorldWanderer):
        translate = QtCore.QCoreApplication.translate
        WorldWanderer.setWindowTitle(translate("WorldWanderer", "WorldWanderer"))
        self.titleLabel.setText(translate("WorldWanderer", "Leaderboard/Match Log"))
        self.returnToMenuButton.setText(translate("WorldWanderer", "Return to Menu"))
        self.databaseUserData.setText(translate("WorldWanderer", "List of registered players"))
        self.databaseLeaderboard.setText(translate("WorldWanderer", "Leaderboard"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WorldWanderer = QtWidgets.QMainWindow()
    ui = WorldWandererUI()
    ui.setupUi(WorldWanderer)
    WorldWanderer.show()
    sys.exit(app.exec_())
