from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

class WorldWandererUI(object):
    # Sets up GUI layout
    def setupUi(self, WorldWanderer):
        WorldWanderer.setObjectName("WorldWanderer")
        # Main window properties (dynamic depending on screen size)
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        WorldWanderer.setFixedSize(int(screen.width() * 0.8), int(screen.height() * 0.8))

        # Central widget: "glues" all parts together
        self.centralWidget = QtWidgets.QWidget(WorldWanderer)
        self.centralWidget.setObjectName("centralWidget")
        WorldWanderer.setCentralWidget(self.centralWidget)

        # Create main vertical layout for whole window
        self.mainVerticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.mainVerticalLayout.setContentsMargins(16, 16, 16, 16)
        self.mainVerticalLayout.setSpacing(16)

        # Create outer frame for GUI's contents with border
        self.mainFrame = QtWidgets.QFrame()
        self.mainFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.mainFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.mainFrame.setLineWidth(2)
        self.mainVerticalLayout.addWidget(self.mainFrame)

        # Content layout inside the main frame
        self.contentVerticalLayout = QtWidgets.QVBoxLayout(self.mainFrame)
        self.contentVerticalLayout.setContentsMargins(16, 16, 16, 16)
        self.contentVerticalLayout.setSpacing(16)

        # Create GUI title
        self.labelconstantTitle = QtWidgets.QLabel()
        titleFont = QtGui.QFont()
        titleFont.setPointSize(28)
        self.labelconstantTitle.setFont(titleFont)
        self.labelconstantTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelconstantTitle.setWordWrap(True)
        self.labelconstantTitle.setFrameShape(QtWidgets.QFrame.Box)
        self.labelconstantTitle.setLineWidth(2)
        self.contentVerticalLayout.addWidget(self.labelconstantTitle)

        # Create GUI subtitle
        self.labelconstantSubtitle = QtWidgets.QLabel()
        subtitleFont = QtGui.QFont()
        subtitleFont.setPointSize(11)
        self.labelconstantSubtitle.setFont(subtitleFont)
        self.labelconstantSubtitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelconstantSubtitle.setWordWrap(True)
        self.labelconstantSubtitle.setFrameShape(QtWidgets.QFrame.Box)
        self.labelconstantSubtitle.setLineWidth(1)
        self.contentVerticalLayout.addWidget(self.labelconstantSubtitle)

        # Define grid layout (2 columns)
        self.categoriesGridLayout = QtWidgets.QGridLayout()
        self.categoriesGridLayout.setHorizontalSpacing(12)
        self.categoriesGridLayout.setVerticalSpacing(8)
        self.contentVerticalLayout.addLayout(self.categoriesGridLayout)

        # Reusable function to build a category cell with title + description
        def makeCategory(titleText, descText):
            container = QtWidgets.QWidget()
            categoryVerticalLayout = QtWidgets.QVBoxLayout(container)
            categoryVerticalLayout.setContentsMargins(0, 0, 0, 0)
            categoryVerticalLayout.setSpacing(6)

            title = QtWidgets.QLabel(titleText)
            titleFontLocal = QtGui.QFont()
            titleFontLocal.setPointSize(18)
            title.setFont(titleFontLocal)
            title.setAlignment(QtCore.Qt.AlignCenter)
            title.setFrameShape(QtWidgets.QFrame.Box)
            title.setLineWidth(1)

            desc = QtWidgets.QLabel(descText)
            descFont = QtGui.QFont()
            descFont.setPointSize(10)
            desc.setFont(descFont)
            desc.setAlignment(QtCore.Qt.AlignCenter)
            desc.setWordWrap(True)
            desc.setFrameShape(QtWidgets.QFrame.Box)
            desc.setLineWidth(1)

            title.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
            desc.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

            categoryVerticalLayout.addWidget(title)
            categoryVerticalLayout.addWidget(desc)
            return container, title, desc

        (roundsCell, self.labelconstantRounds, self.labelconstantRoundsDesc) = makeCategory(
            "Rounds",
            "Select how many rounds you can have."
        )
        (timeCell, self.labelconstantTime, self.labelconstantTimeDesc) = makeCategory(
            "Time Limit",
            "Select how long you have to guess before your time runs out."
        )

        categoryCells = [roundsCell, timeCell]
        for i in range(len(categoryCells)):
            self.categoriesGridLayout.addWidget(categoryCells[i], 0, i)

        # Make column widths equal
        for i in range(2):
            self.categoriesGridLayout.setColumnStretch(i, 1)

        # Grid for limits
        self.limitsGridLayout = QtWidgets.QGridLayout()
        self.limitsGridLayout.setHorizontalSpacing(12)
        self.limitsGridLayout.setVerticalSpacing(6)
        self.contentVerticalLayout.addLayout(self.limitsGridLayout)

        # Make column widths equal
        for i in range(2):
            self.limitsGridLayout.setColumnStretch(i, 1)

        # Limits utility
        def limit(limitType, text):
            if limitType == "Def":
                label = QtWidgets.QLabel(f"Default: {text}")
            elif limitType == "Max":
                label = QtWidgets.QLabel(f"Maximum: {text}")
            elif limitType == "Min":
                label = QtWidgets.QLabel(f"Minimum: {text}")
            else:
                label = QtWidgets.QLabel("Error defining limitation")
            labelFont = QtGui.QFont()
            labelFont.setPointSize(10)
            label.setFont(labelFont)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setWordWrap(True)
            label.setFrameShape(QtWidgets.QFrame.Box)
            label.setLineWidth(1)
            label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
            return label

        self.labelconstantRoundsDefault, self.labelconstantRoundsMax, self.labelconstantRoundsMin = limit("Def", "Disabled"), limit("Max", "N/A"), limit("Min", "N/A")
        self.labelconstantTimeDefault, self.labelconstantTimeMax, self.labelconstantTimeMin = limit("Def", "Disabled"), limit("Max", "N/A"), limit("Min", "N/A")

        # Add all to limitsGridLayout
        limitsArray = [
            [self.labelconstantRoundsDefault, self.labelconstantRoundsMax, self.labelconstantRoundsMin],
            [self.labelconstantTimeDefault, self.labelconstantTimeMax, self.labelconstantTimeMin]
        ]
        for col, widgets in enumerate(limitsArray):
            for row, widget in enumerate(widgets):
                self.limitsGridLayout.addWidget(widget, row, col)

        # Define controls layout
        self.controlsGridLayout = QtWidgets.QGridLayout()
        self.controlsGridLayout.setHorizontalSpacing(12)
        self.controlsGridLayout.setVerticalSpacing(8)
        self.contentVerticalLayout.addLayout(self.controlsGridLayout)

        # Make only the used columns expand equally
        self.controlsGridLayout.setColumnStretch(0, 1)
        self.controlsGridLayout.setColumnStretch(1, 1)

        # Reusable function to build a framed interaction control
        def makeFrame(frameType):
            frame = QtWidgets.QFrame()
            frame.setFrameShape(QtWidgets.QFrame.Box)
            frame.setLineWidth(1)
            frameLayout = QtWidgets.QHBoxLayout(frame)
            frameLayout.setContentsMargins(8, 8, 8, 8)
            font = QtGui.QFont()
            font.setBold(True)
            font.setPointSize(11)
            if frameType == "slider":
                interaction = QtWidgets.QSlider(QtCore.Qt.Horizontal)
                interaction.setMinimum(1)
                interaction.setMaximum(5)
                interaction.setValue(3)
                frameLayout.addStretch(1)
                frameLayout.addWidget(interaction, alignment=QtCore.Qt.AlignCenter)
                frameLayout.addStretch(1)
                return frame, interaction
            elif frameType == "dial":
                interaction = QtWidgets.QDial()
                interaction.setMinimum(15)
                interaction.setMaximum(150)
                interaction.setSingleStep(5)
                interaction.setValue(60)
                interaction.setNotchesVisible(True)
                valueLabel = QtWidgets.QLabel()
                valueFont = QtGui.QFont()
                valueFont.setBold(True)
                valueFont.setPointSize(11)
                valueLabel.setFont(valueFont)
                valueLabel.setAlignment(QtCore.Qt.AlignCenter)
                frameLayout.addStretch(1)
                frameLayout.addWidget(interaction, alignment=QtCore.Qt.AlignCenter)
                frameLayout.addWidget(valueLabel, alignment=QtCore.Qt.AlignCenter)
                frameLayout.addStretch(1)
                return frame, interaction, valueLabel
            else:
                return frame, None

        # Frame for how many rounds (slider + ticks)
        self.roundsFrame, self.roundSlider = makeFrame("slider")

        # Frame for time limits (dial + value label)
        self.timeFrame, self.timeDial, self.labelvariableDialValue = makeFrame("dial")

        # Add frames to main grid layout
        self.controlsGridLayout.addWidget(self.roundsFrame, 0, 0)
        self.controlsGridLayout.addWidget(self.timeFrame, 0, 1)

        # Footer message
        self.labelconstantFooter = QtWidgets.QLabel()
        footerFont = QtGui.QFont()
        footerFont.setPointSize(10)
        self.labelconstantFooter.setFont(footerFont)
        self.labelconstantFooter.setAlignment(QtCore.Qt.AlignCenter)
        self.labelconstantFooter.setWordWrap(True)
        self.labelconstantFooter.setFrameShape(QtWidgets.QFrame.Box)
        self.labelconstantFooter.setLineWidth(1)
        self.contentVerticalLayout.addWidget(self.labelconstantFooter)

        # Finish button
        self.finishButtonRowLayout = QtWidgets.QHBoxLayout()
        self.finishButton = QtWidgets.QPushButton()
        finishButtonFont = QtGui.QFont()
        finishButtonFont.setPointSize(12)
        finishButtonFont.setBold(True)
        self.finishButton.setFont(finishButtonFont)
        self.finishButton.clicked.connect(self.finishButtonBackend)
        self.finishButtonRowLayout.addStretch(1)
        self.finishButtonRowLayout.addWidget(self.finishButton)
        self.finishButtonRowLayout.addStretch(1)
        self.contentVerticalLayout.addLayout(self.finishButtonRowLayout)

        # Update label for time of each round
        def updateTimeLabel(value):
            if hasattr(self, "unitSecondsShort"):
                self.labelvariableDialValue.setText(f"{value} {self.unitSecondsShort}")
            else:
                self.labelvariableDialValue.setText(f"{value} s")
        self.timeDial.valueChanged.connect(updateTimeLabel)

        # Set GUI's text
        self.retranslateUi(WorldWanderer)
        QtCore.QMetaObject.connectSlotsByName(WorldWanderer)

    # Required to set GUI's text
    def retranslateUi(self, WorldWanderer):
        translate = QtCore.QCoreApplication.translate
        WorldWanderer.setWindowTitle(translate("WorldWanderer", "MainWindow"))
        self.labelconstantTitle.setText(translate("WorldWanderer", "Pre-Match Settings"))
        self.labelconstantSubtitle.setText(translate("WorldWanderer", "When finished (or to skip), press the button below"))
        self.labelconstantRounds.setText(translate("WorldWanderer", "Rounds"))
        self.labelconstantTime.setText(translate("WorldWanderer", "Time Limit"))
        self.labelconstantRoundsDesc.setText(translate("WorldWanderer", "Select how many rounds you can have."))
        self.labelconstantTimeDesc.setText(translate("WorldWanderer", "Select how long you have to guess before your time runs out."))
        self.labelconstantRoundsDefault.setText(translate("WorldWanderer", "Default: 3"))
        self.labelconstantRoundsMax.setText(translate("WorldWanderer", "Maximum: 5"))
        self.labelconstantRoundsMin.setText(translate("WorldWanderer", "Minimum: 1"))
        self.labelconstantTimeDefault.setText(translate("WorldWanderer", "Default: 60 seconds"))
        self.labelconstantTimeMax.setText(translate("WorldWanderer", "Maximum: 150 seconds"))
        self.labelconstantTimeMin.setText(translate("WorldWanderer", "Minimum: 15 seconds"))
        self.labelvariableDialValue.setText(translate("WorldWanderer", "60 s"))
        self.labelconstantFooter.setText(translate("WorldWanderer", "Note: going beyond a setting's limits (if they're defined) will automatically reset to their defaults."))
        self.finishButton.setText(translate("WorldWanderer", "Finish"))
    
    # Finish button backend
    def finishButtonBackend(self):
        valueRounds = self.roundSlider.value()
        valueTimeLimit = self.timeDial.value()

        with open("WorldWanderer-main/storage/matchSettings/numberOfRounds.txt", "w") as file:
            file.write(str(valueRounds))
        with open("WorldWanderer-main/storage/matchSettings/timeLimit.txt", "w") as file:
            file.write(str(valueTimeLimit))
        
        alert = QMessageBox()
        alert.setWindowTitle("Warning")
        alert.setText("Images from the UK and USA are shown only. No images outside the green boxes will be shown, so make your guesses within them.")
        alert.setIcon(QMessageBox.Information)
        alert.setStandardButtons(QMessageBox.Ok)
        result = alert.exec_()
        if result == QMessageBox.Ok:
            pass

        print("[gui/preMatchSettingsSingleplayer.py] START", flush=True) # Tells app.py to start up main.py
        QtWidgets.QApplication.quit()

# Run GUI
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WorldWanderer = QtWidgets.QMainWindow()
    ui = WorldWandererUI()
    ui.setupUi(WorldWanderer)
    WorldWanderer.show()
    sys.exit(app.exec_())
