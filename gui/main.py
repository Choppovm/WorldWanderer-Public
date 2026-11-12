import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QTimer
import sys
import math
import subprocess
from backend.scoring import logRoundResult, calculateFinalScore, logFinalScore, clearSingleMatchLogsData

# Function for getting time limit defined by user in pre-match settings
def loadTimeLimit():
    try:
        with open("WorldWanderer-main/storage/matchSettings/timeLimit.txt", "r") as file:
            value = int(file.read().strip())
            return max(15, min(value, 150)) # ensures time limit is properly set between 15 and 150
    except Exception:
        return 60 # failsafe: any errors lead to the default 60 second time limit

# Function for getting number of rounds defined by user in pre-match settings
def loadNumberOfRounds():
    try:
        with open("WorldWanderer-main/storage/matchSettings/numberOfRounds.txt", "r") as file:
            value = int(file.read().strip())
            return max(1, min(value, 5)) # ensures round count is properly set between 1 and 5
    except Exception:
        return 3 # failsafe: any errors lead to the default 3 round match

class WorldWandererUI(object):
    def setupUi(self, WorldWanderer):
        self.WorldWanderer = WorldWanderer
        self.labelHandlers()

        # Timer process + poller
        self.timerProcess = None
        self.timerPoller = QTimer()
        self.timerPoller.timeout.connect(self.checkTimerProcess)
        self.timerExpired = False
        self.timeRemaining = 0
        self.countdownTimer = QTimer()
        self.countdownTimer.timeout.connect(self.updateCountdownLabel)

        # Round tracking
        self.totalRounds = loadNumberOfRounds()
        self.currentRound = 1

        # Main window properties (dynamic depending on screen size)
        WorldWanderer.setObjectName("WorldWanderer")
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        WorldWanderer.setFixedSize(int(screen.width() * 0.8), int(screen.height() * 0.8))
        WorldWanderer.setAutoFillBackground(False)

        # Central widget: "glues" all parts together
        self.centralwidget = QtWidgets.QWidget(WorldWanderer)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")

        # Create main horizontal layout for whole window
        mainLayout = QtWidgets.QHBoxLayout(self.centralwidget)

        # Left side layout: Mapillary and OSM stacked vertically
        leftLayout = QtWidgets.QVBoxLayout()

        # Emergency Reload Mapillary Button
        self.buttonReloadMapillary = QtWidgets.QPushButton()
        self.buttonReloadMapillary.setObjectName("buttonReloadMapillary")
        self.buttonReloadMapillary.clicked.connect(self.reloadMapillaryButtonBackend)
        leftLayout.addWidget(self.buttonReloadMapillary)

        # Mapillary frame
        self.mapillaryFrame = QWebEngineView()
        self.mapillaryFrame.setAutoFillBackground(False)
        self.mapillaryFrame.setObjectName("mapillaryFrame")
        self.mapillaryFrame.setUrl(QtCore.QUrl("http://127.0.0.1:8000/mapillary"))
        self.mapillaryFrame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.mapillaryFrame.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        leftLayout.addWidget(self.mapillaryFrame)

        # Mapillary load check: Do not start round timer until the image has loaded (checks every 300 ms)
        self.mapillaryLoaded = False
        self.mapillaryReadyPoller = QTimer()
        self.mapillaryReadyPoller.timeout.connect(self.checkMapillaryReady)
        self.mapillaryReadyPoller.start(300)

        # Horizontal divider
        self.horizontalLine = QtWidgets.QFrame()
        self.horizontalLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontalLine.setFrameShadow(QtWidgets.QFrame.Plain)
        self.horizontalLine.setLineWidth(3)
        leftLayout.addWidget(self.horizontalLine)

        # OSM frame
        self.osmFrame = QWebEngineView()
        self.osmFrame.setObjectName("osmFrame")
        self.osmFrame.setUrl(QtCore.QUrl("http://127.0.0.1:8000/osm"))
        self.osmFrame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.osmFrame.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        leftLayout.addWidget(self.osmFrame)

        # Vertical divider: separates leftLayout from rightLayout
        self.verticalLine = QtWidgets.QFrame()
        self.verticalLine.setFrameShape(QtWidgets.QFrame.VLine)
        self.verticalLine.setFrameShadow(QtWidgets.QFrame.Plain)
        self.verticalLine.setLineWidth(3)

        # Right side layout: holds all non-map parts (e.g. buttons, labels)
        rightLayout = QtWidgets.QVBoxLayout()

        # Return to menu button
        self.buttonMenu = QtWidgets.QPushButton()
        self.buttonMenu.setObjectName("buttonMenu")
        self.buttonMenu.clicked.connect(self.menuButtonBackend)
        rightLayout.addWidget(self.buttonMenu)

        # Guess button
        self.buttonGuess = QtWidgets.QPushButton()
        self.buttonGuess.setObjectName("buttonGuess")
        self.buttonGuess.clicked.connect(self.guessButtonBackend)
        rightLayout.addWidget(self.buttonGuess)

        # Countdown label
        self.labelvariableCountdown = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.labelvariableCountdown.setFont(font)
        self.labelvariableCountdown.setFrameShape(QtWidgets.QFrame.Box)
        self.labelvariableCountdown.setAlignment(QtCore.Qt.AlignCenter)
        self.labelvariableCountdown.setText("Time Left: --")
        rightLayout.addWidget(self.labelvariableCountdown)

        # Error label
        self.labelvariableError = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.labelvariableError.setFont(font)
        self.labelvariableError.setAutoFillBackground(False)
        self.labelvariableError.setFrameShape(QtWidgets.QFrame.Box)
        self.labelvariableError.setWordWrap(True)
        rightLayout.addWidget(self.labelvariableError)

        # Segment divider
        self.segmentDivider = QtWidgets.QFrame()
        self.segmentDivider.setFrameShape(QtWidgets.QFrame.HLine)
        self.segmentDivider.setFrameShadow(QtWidgets.QFrame.Plain)
        self.segmentDivider.setLineWidth(2)
        rightLayout.addWidget(self.segmentDivider)

        # "Your Guessed Coordinates" label
        self.labelconstantYourGuessedCoords = QtWidgets.QLabel()
        self.labelconstantYourGuessedCoords.setFont(font)
        self.labelconstantYourGuessedCoords.setAutoFillBackground(False)
        self.labelconstantYourGuessedCoords.setFrameShape(QtWidgets.QFrame.Box)
        self.labelconstantYourGuessedCoords.setWordWrap(True)
        rightLayout.addWidget(self.labelconstantYourGuessedCoords)

        # User coords label
        self.labelvariableUserCoords = QtWidgets.QLabel()
        self.labelvariableUserCoords.setFont(font)
        self.labelvariableUserCoords.setAutoFillBackground(False)
        self.labelvariableUserCoords.setFrameShape(QtWidgets.QFrame.Box)
        self.labelvariableUserCoords.setWordWrap(False)
        rightLayout.addWidget(self.labelvariableUserCoords)

        # "Actual Coordinates" label
        self.labelconstantActualCoords = QtWidgets.QLabel()
        self.labelconstantActualCoords.setFont(font)
        self.labelconstantActualCoords.setAutoFillBackground(False)
        self.labelconstantActualCoords.setFrameShape(QtWidgets.QFrame.Box)
        self.labelconstantActualCoords.setWordWrap(True)
        rightLayout.addWidget(self.labelconstantActualCoords)

        # Mapillary coords label
        self.labelvariableMapillaryCoords = QtWidgets.QLabel()
        self.labelvariableMapillaryCoords.setFont(font)
        self.labelvariableMapillaryCoords.setAutoFillBackground(False)
        self.labelvariableMapillaryCoords.setFrameShape(QtWidgets.QFrame.Box)
        self.labelvariableMapillaryCoords.setWordWrap(False)
        rightLayout.addWidget(self.labelvariableMapillaryCoords)

        # "Distance" label
        self.labelconstantDistance = QtWidgets.QLabel()
        self.labelconstantDistance.setFont(font)
        self.labelconstantDistance.setAutoFillBackground(False)
        self.labelconstantDistance.setFrameShape(QtWidgets.QFrame.Box)
        self.labelconstantDistance.setWordWrap(True)
        rightLayout.addWidget(self.labelconstantDistance)

        # Distance between mapillary and user guess label
        self.labelvariableDistance = QtWidgets.QLabel()
        self.labelvariableDistance.setFont(font)
        self.labelvariableDistance.setAutoFillBackground(False)
        self.labelvariableDistance.setFrameShape(QtWidgets.QFrame.Box)
        self.labelvariableDistance.setWordWrap(False)
        rightLayout.addWidget(self.labelvariableDistance)

        # Segment divider (2)
        self.segmentDivider2 = QtWidgets.QFrame()
        self.segmentDivider2.setFrameShape(QtWidgets.QFrame.HLine)
        self.segmentDivider2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.segmentDivider2.setLineWidth(2)
        rightLayout.addWidget(self.segmentDivider2)

        # Rounds left label
        self.labelvariableRoundsLeft = QtWidgets.QLabel()
        self.labelvariableRoundsLeft.setFont(font)
        self.labelvariableRoundsLeft.setFrameShape(QtWidgets.QFrame.Box)
        self.labelvariableRoundsLeft.setAlignment(QtCore.Qt.AlignCenter)
        self.labelvariableRoundsLeft.setText(f"Rounds Left: {self.totalRounds - self.currentRound + 1}")
        rightLayout.addWidget(self.labelvariableRoundsLeft)

        # Next round button
        self.buttonNext = QtWidgets.QPushButton()
        self.buttonNext.setObjectName("buttonNext")
        self.buttonNext.setEnabled(False)
        self.buttonNext.clicked.connect(self.advanceRound)
        self.buttonNext.clicked.connect(self.mapillaryFrame.reload)
        self.buttonNext.clicked.connect(self.osmFrame.reload)
        rightLayout.addWidget(self.buttonNext)

        # Glue everything to mainLayout
        mainLayout.addLayout(leftLayout, 2)   # Left side takes more space
        mainLayout.addWidget(self.verticalLine)
        mainLayout.addLayout(rightLayout, 2)  # Right side narrower
        
        # Set central widget
        WorldWanderer.setCentralWidget(self.centralwidget)

        # Set text for UI elements
        self.retranslateUi(WorldWanderer)
        QtCore.QMetaObject.connectSlotsByName(WorldWanderer)        

    # Holds coordinate values when updating labels, holds error values when checking for them and updating labels respectively, etc.
    def labelHandlers(self):
        # Error handlers (currently only checking if no coords were logged)
        self.mapillaryCoordsError = "none"
        self.userGuessCoordsError = "none"

        # Holds mapillary coordinates
        self.mapillaryCoordsLat = ""
        self.mapillaryCoordsLng = ""

        # Holds user's guessed coordinates
        self.userGuessCoordsLat = ""
        self.userGuessCoordsLng = ""

    # Polls text file that gets written to by website when the Mapillary image loads. Start timer when it does.
    def checkMapillaryReady(self):
        try:
            with open("WorldWanderer-main/storage/mapillaryReady.txt", "r") as f:
                status = f.read().strip()
        except:
            status = "" # If there's an error in any way, this simulates an empty mapillaryReady.txt file.

        if status == "READY" and not self.mapillaryLoaded:
            self.mapillaryLoaded = True
            self.startRoundTimer()

            # Reset flag for next round
            with open("WorldWanderer-main/storage/mapillaryReady.txt", "w") as f:
                f.write("")

            self.mapillaryReadyPoller.stop()

    # Update rounds label accordingly with user's pre-match settings
    def updateRoundsLeftLabel(self):
        roundsLeft = self.totalRounds - self.currentRound + 1
        self.labelvariableRoundsLeft.setText(f"Rounds Left: {roundsLeft}")

    # Backend for managing rounds-keeping (ends game or proceeds with every new round)
    def advanceRound(self):
        self.currentRound += 1
        self.updateRoundsLeftLabel()

        if self.currentRound > self.totalRounds:
            # Game over
            self.endGame()
        else:
            # Continue to next round
            self.nextButtonBackend()

    # Backend for ending the game when rounds are over. Used in advanceRound().
    def endGame(self):
        name, ok = QtWidgets.QInputDialog.getText( # Ask for player name
            None,
            "Game Over",
            "All rounds completed!\n\nEnter your name for the leaderboard:"
        )

        if not ok or name.strip() == "": # If the user fails to enter a name or they close the GUI 
            name = "Anonymous"

        # Calculate and log score
        finalScore = calculateFinalScore()
        logFinalScore(
            playerName=name,
            finalScore=finalScore,
            roundsPlayed=self.totalRounds,
            timeLimit=loadTimeLimit()
        )
        clearSingleMatchLogsData()

        # Notify user and exit
        alert = QMessageBox()
        alert.setWindowTitle("Game Over")
        alert.setIcon(QMessageBox.Information)
        alert.setText(f"Thanks, {name}! Your score has been saved.\nReturning to the main menu.")
        alert.setStandardButtons(QMessageBox.Ok)
        alert.exec_()

        print("[gui/main.py] RETURNTOMENU", flush=True)
        QtWidgets.QApplication.quit()

    # Backend for actually starting the timer
    def startRoundTimer(self):
        timeLimit = loadTimeLimit()

        # Set countdown
        self.timeRemaining = timeLimit
        self.labelvariableCountdown.setText(f"Time Left: {self.timeRemaining}")
        self.countdownTimer.start(1000) # update every second

        # Start subprocess timer
        self.timerProcess = subprocess.Popen(
            ["python", "WorldWanderer-main/backend/roundTimer.py", str(timeLimit)]
        )
        self.timerPoller.start(500)
        self.timerExpired = False

    # Responsible for polling separate timer backend file until it stops running (i.e. when timer is done)
    def checkTimerProcess(self):
        if self.timerProcess is None:
            return
        if self.timerProcess.poll() is not None: # Timer finished when file stops running
            self.timerPoller.stop()
            self.timerProcess = None
            self.timerExpired = True
            self.guessButtonBackend() # Auto-submit guess
            self.buttonNext.setEnabled(True)

    # Updates time left
    def updateCountdownLabel(self):
        if self.timeRemaining > 0:
            self.timeRemaining -= 1
            self.labelvariableCountdown.setText(f"Time Left: {self.timeRemaining}")
        else:
            self.countdownTimer.stop()

    # Ensures timer doesn't start until mapillary image loads (no point playing if you only get 30 seconds and the picture takes 26 seconds to load)
    def onMapillaryLoaded(self, ok):
        if ok and not self.mapillaryLoaded:
            self.mapillaryLoaded = True
            self.startRoundTimer()

    # Required to set text for UI elements
    def retranslateUi(self, WorldWanderer):
        translate = QtCore.QCoreApplication.translate
        WorldWanderer.setWindowTitle(translate("WorldWanderer", "WorldWanderer: Main Window"))
        self.buttonMenu.setText(translate("WorldWanderer", "Return to Menu"))
        self.buttonReloadMapillary.setText(translate("WorldWanderer", "In the event that the street-view image doesn't load, click here to reload it (DO NOT USE UNLESS THE IMAGE FAILS TO LOAD)"))
        self.buttonGuess.setText(translate("WorldWanderer", "Submit Guess"))
        if (self.userGuessCoordsError and self.mapillaryCoordsError) == "missingCoords":
            self.labelvariableError.setText(translate("WorldWanderer", "Error: Mapillary and OSM Pin coordinates mising."))
        elif self.userGuessCoordsError == "missingCoords":
            self.labelvariableError.setText(translate("WorldWanderer", "Error: OSM Pin coordinates missing."))
        elif self.mapillaryCoordsError == "missingCoords":
            self.labelvariableError.setText(translate("WorldWanderer", "Error: Mapillary coordinates missing.")) 
        else:
            self.labelvariableError.setText(translate("WorldWanderer", "(Any errors that might occur will show here. No errors have been found!"))
        self.labelconstantYourGuessedCoords.setText(translate("WorldWanderer", "Your Guessed Coordinates"))
        if self.userGuessCoordsError == "missingCoords":
            self.labelvariableUserCoords.setText(translate("WorldWanderer", "[COORDINATES COULD NOT BE FOUND]"))
        else:
            if self.userGuessCoordsLat and self.userGuessCoordsLng:
                self.labelvariableUserCoords.setText(translate("WorldWanderer", f"({self.userGuessCoordsLat}, {self.userGuessCoordsLng})\n(Latitude: {self.userGuessCoordsLat})\n(Longitude: {self.userGuessCoordsLng})"))
            else:
                self.labelvariableUserCoords.setText(translate("WorldWanderer", "..."))
        self.labelconstantActualCoords.setText(translate("WorldWanderer", "Actual Coordinates"))
        if self.mapillaryCoordsError == "missingCoords":
            self.labelvariableMapillaryCoords.setText(translate("WorldWanderer", "[COORDINATES COULD NOT BE FOUND]"))
        else:
            if self.mapillaryCoordsLat and self.mapillaryCoordsLng:
                self.labelvariableMapillaryCoords.setText(translate("WorldWanderer", f"({self.mapillaryCoordsLat}, {self.mapillaryCoordsLng})\n(Latitude: {self.mapillaryCoordsLat})\n(Longitude: {self.mapillaryCoordsLng})"))
            else:
                self.labelvariableMapillaryCoords.setText(translate("WorldWanderer", "..."))
        self.labelconstantDistance.setText(translate("WorldWanderer", "Distance between your guess and the correct answer"))
        self.labelvariableDistance.setText(translate("WorldWanderer", self.getDistance()))
        self.updateRoundsLeftLabel()
        self.buttonNext.setText(translate("WorldWanderer", "Next Round"))
    
    # Find distance between user's guessed coords and mapillary coords
    def getDistance(self):
        # Distance is returned in meters/kilometers using haversine formula (https://en.wikipedia.org/wiki/Haversine_formula)
        
        try:
            # Convert string coordinates to float, then to radians
            userLat = math.radians(float(self.userGuessCoordsLat))
            userLon = math.radians(float(self.userGuessCoordsLng))
            mapillaryLat = math.radians(float(self.mapillaryCoordsLat))
            mapillaryLon = math.radians(float(self.mapillaryCoordsLng))
        except (ValueError, TypeError):
            return "..." # Invalid coordinate format

        # Haversine formula
        distanceLat = mapillaryLat - userLat 
        distanceLon = mapillaryLon - userLon
        haversineComponent = math.sin(distanceLat / 2)**2 + math.cos(userLat) * math.cos(mapillaryLat) * math.sin(distanceLon / 2)**2
        angularDistance = 2 * math.asin(math.sqrt(haversineComponent)) 
        earthRadiusKm = 6371  # Radius of Earth in kilometers

        # Calculate distance
        distanceKilometers = abs(angularDistance * earthRadiusKm)
        distanceMeters = distanceKilometers * 1000

        # Return formatted string
        if distanceKilometers >= 1:
            return f"{distanceKilometers:.2f} Kilometers (km)"
        else:
            return f"{distanceMeters:.2f} Meters (m)"

    # Guess button backend
    def guessButtonBackend(self):
        # Get coordinates/errors
        def readText(path):
            try:
                with open(path, "r") as file:
                    return file.read().strip()
            except Exception:
                return ""
        mapillaryCoordinates = readText("WorldWanderer-main/storage/currentMapillaryCoords.txt")
        userGuessCoordinates = readText("WorldWanderer-main/storage/currentUserGuessCoords.txt")

        # Mapillary
        if "no-coordinates" in mapillaryCoordinates: # if no coords found
            self.mapillaryCoordsError = "missingCoords"
        else:
            self.mapillaryCoordsError = "none"
            # Parsing coordinates here
            parts = mapillaryCoordinates.split(",")
            if len(parts) == 2:
                self.mapillaryCoordsLat, self.mapillaryCoordsLng = parts
            else:
                self.mapillaryCoordsError = "missingCoords"

        # OSM/User's guessed coordinates
        if "no-coordinates" in userGuessCoordinates: # if no coords found
            self.userGuessCoordsError = "missingCoords"
        elif userGuessCoordinates == "": # if user hasn't placed a pin/marker down yet
            if not self.timerExpired: # if timer expired, allow auto-submit with no pin.
                alert = QMessageBox()
                alert.setWindowTitle("Warning!")
                alert.setIcon(QMessageBox.Warning)
                alert.setText("You must place down a pin/marker before submitting your guess!")
                alert.setStandardButtons(QMessageBox.Ok)
                alert.exec_()
                return
        else:
            self.userGuessCoordsError = "none"
            # Parsing coordinates here
            parts = userGuessCoordinates.split(",")
            if len(parts) == 2:
                self.userGuessCoordsLat, self.userGuessCoordsLng = parts
            else:
                self.userGuessCoordsError = "missingCoords"

        # Trigger the JS function inside the OSM page
        self.osmFrame.page().runJavaScript("plotMapillaryCoords();")

        # Log round results in database
        try:
            distanceStr = self.getDistance()
            distanceM = float(distanceStr.split()[0]) if "Meters" in distanceStr else float(distanceStr.split()[0]) * 1000
            logRoundResult(
                roundNumber = self.currentRound,
                distanceMeters = distanceM,
                timeTaken = loadTimeLimit() - self.timeRemaining,
                guessLat = float(self.userGuessCoordsLat) if self.userGuessCoordsLat else None,
                guessLon = float(self.userGuessCoordsLng) if self.userGuessCoordsLng else None,
                actualLat = float(self.mapillaryCoordsLat) if self.mapillaryCoordsLat else None,
                actualLon = float(self.mapillaryCoordsLng) if self.mapillaryCoordsLng else None
            )
        except Exception as e:
            print("Error logging round:", e)

        # Toggle buttons
        self.buttonGuess.setEnabled(False)
        if self.timerProcess:
            self.timerProcess.terminate()
            self.timerProcess = None
        self.countdownTimer.stop()
        self.buttonNext.setEnabled(True)
        # Update labels
        self.retranslateUi(self.WorldWanderer) 

    # Next button backend
    def nextButtonBackend(self):
        # Toggle Buttons
        self.buttonNext.setEnabled(False)
        self.buttonGuess.setEnabled(True)

        # Reset coordinate text files
        with open("WorldWanderer-main/storage/currentUserGuessCoords.txt", "w") as file:
            file.write("")
        with open("WorldWanderer-main/storage/currentMapillaryCoords.txt", "w") as file:
            file.write("")

        # Reset ready flag
        with open("WorldWanderer-main/storage/mapillaryReady.txt", "w") as f:
            f.write("")

        # Prevent timer from starting immediately on future rounds
        self.mapillaryLoaded = False

        # Update (reset) labels/error handler values
        self.mapillaryCoordsError = "none"
        self.userGuessCoordsError = "none"
        self.mapillaryCoordsLat = ""
        self.mapillaryCoordsLng = ""
        self.userGuessCoordsLat = ""
        self.userGuessCoordsLng = ""
        self.retranslateUi(self.WorldWanderer)

    # Main menu button backend
    def menuButtonBackend(self):
        def returnToMenuAlert(type):
            alert = QMessageBox()
            alert.setWindowTitle("Warning!")
            alert.setIcon(QMessageBox.Warning)
            if type == "valid":
                alert.setText("Are you sure you want to return to the main menu? You will lose all of your progress for this session.")
                alert.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                result = alert.exec_()
                if result == QMessageBox.Ok:
                    print("[gui/main.py] RETURNTOMENU", flush=True) # Tells app.py to return to main menu
                    # Reset coordinate text files
                    with open("WorldWanderer-main/storage/currentUserGuessCoords.txt", "w") as file:
                        file.write("")
                    with open("WorldWanderer-main/storage/currentMapillaryCoords.txt", "w") as file:
                        file.write("")
                    QtWidgets.QApplication.quit()
                elif result == QMessageBox.Cancel:
                    pass
                else:
                    pass
            elif type == "invalid":
                alert.setText("You cannot return to the menu while a round is in progress. End the current round, then try again!")
                alert.setStandardButtons(QMessageBox.Ok)
                alert.exec_()
            elif type == "unknown":
                alert.setText("An error has occurred. Details: gui/main.py:182, unknown isEnabled value logged when check took place.")
                alert.setStandardButtons(QMessageBox.Ok)
                alert.exec_()
            else:
                alert.setText("An error has occurred. Details: gui/main.py:186, unknown function input ('type') logged when function was ran.")
                alert.setStandardButtons(QMessageBox.Ok)
                alert.exec_()
            return
        if self.buttonGuess.isEnabled() == False:
            returnToMenuAlert("valid")
        elif self.buttonGuess.isEnabled() == True:
            returnToMenuAlert("invalid")
        else:
            returnToMenuAlert("unknown")
    
    # Emergency reload mapillary button backend
    def reloadMapillaryButtonBackend(self):
        self.buttonReloadMapillary.setEnabled(False) # Disable the button temporarily to prevent spam-clicking

        # Reset the ready flag so the timer won't start prematurely
        try:
            with open("WorldWanderer-main/storage/mapillaryReady.txt", "w") as f:
                f.write("")
        except Exception:
            pass

        # Mark Mapillary as not loaded so the timer won't start
        self.mapillaryLoaded = False

        # Restart the polling loop that waits for Mapillary to finish loading
        self.mapillaryReadyPoller.start(300)

        # Reload the Mapillary frame
        self.mapillaryFrame.reload()

        # Re-enable the button after a short delay (prevents double reloads)
        QtCore.QTimer.singleShot(1500, lambda: self.buttonReloadMapillary.setEnabled(True))

        


# Main function to run the application.
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    WorldWanderer = QtWidgets.QMainWindow()
    ui = WorldWandererUI()
    ui.setupUi(WorldWanderer)
    WorldWanderer.show()
    sys.exit(app.exec_())
