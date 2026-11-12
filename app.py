########### Imports ###########

import subprocess
import time
import requests
import colorama as fontFormat



"""###################### Debug Settings ######################"""

consoleDebug = True # Toggle terminal debug output
fontFormat.init(autoreset=True) # Initializes only once
def debug(message): # Function for handling debug statements being printed to terminal (if enabled)
    if consoleDebug:
        print(f"{fontFormat.Style.BRIGHT}{fontFormat.Back.MAGENTA}[DEBUG]{fontFormat.Style.RESET_ALL} | {message}")



"""###################### Loading Screen ######################"""

########### Start GUI ###########
def runLoadingScreen(): # Function for starting loading screen GUI
    debug("Starting loading screen")
    global loadingScreen
    loadingScreen = subprocess.Popen(
        ["python", "WorldWanderer-main/gui/loading.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    debug("Loading screen running")

    while True:
        # If loading screen is closed
        if loadingScreen.poll() is not None:
            break

        # Check for whether loading screen has finished rendering yet or not
        line = loadingScreen.stdout.readline()
        if "[gui/loading.py] RENDERED" in line:
            debug("Loading GUI is visible")
            break
    
    # When "break" is called (when while True loop is stopped)
    return

########### Close GUI ###########
def closeLoadingScreen(): # Function for ending loading screen GUI
    debug("Terminating loading screen")
    try:
        loadingScreen.terminate()
    except Exception:
        pass
    try:
        loadingScreen.wait(timeout=2)
    except Exception:
        pass
    debug("Loading screen terminated")

########### Clear data stored in WorldWanderer-main/storage ###########
def clearVariableStorageData(): # Function for clearing any past coordinates that might've existed when somebody else played the game in the past
    # Coordinates
    try:
        with open("WorldWanderer-main/storage/currentUserGuessCoords.txt", "w") as file:
            file.write("")
        debug("User Guessed Coordinates text file reset successfully")
    except Exception:
        debug("User Guessed Coordinates text file failed to be reset")
    try:
        with open("WorldWanderer-main/storage/currentMapillaryCoords.txt", "w") as file:
            file.write("")
        debug("Mapillary Coordinates text file reset successfully")
    except Exception:
        debug("Mapillary Coordinates text file failed to be reset")
    # Settings data
    try:
        with open("WorldWanderer-main/storage/matchSettings/numberOfRounds.txt", "w") as file:
            file.write("")
        debug("Number of rounds file reset successfully")
    except Exception:
        debug(f"Number of rounds file failed to be reset ({Exception})")
    try:
        with open("WorldWanderer-main/storage/matchSettings/timeLimit.txt", "w") as file:
            file.write("")
        debug("Time limit file reset successfully")
    except Exception:
        debug("Time limit file failed to be reset")

########### Wait for flask web server to start up ###########
def waitForFlask(): # Function for checking whether web app is running
    url = "http://127.0.0.1:8000/ping" # Will return "200" when requesting status_code if it's running
    attempts = 1 # Number of times status_code has been requested
    while True:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                debug("Web app running")
                return "WEBAPPRUNNING"
        except requests.exceptions.RequestException:
            pass
        debug(f"Ping attempted (Attempt : {attempts})")
        attempts += 1
        time.sleep(0.5)



"""###################### Main Menu ######################"""

########### Run main menu GUI ###########
def runMainMenu(): # Function for starting the main menu GUI
    debug("Starting main menu")
    mainMenu = subprocess.Popen(
        ["python", "WorldWanderer-main/gui/menu.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    debug("Main menu running")
    return mainMenuButtonsHandler(mainMenu)

########### Handle backend processes for each button ###########
def mainMenuButtonsHandler(proc): # Function for handling buttons of the main menu GUI. proc is short for process.
    while True:
        # If main menu is closed manually (via X in top right of all windows), terminate program entirely.
        if proc.poll() is not None:
            debug("Main menu GUI closed manually")
            try:
                proc.terminate()
            except Exception:
                pass
            try:
                proc.wait(timeout=2)
            except Exception:
                pass
            debug("Main menu GUI terminated")
            return "EXIT"

        line = proc.stdout.readline()
        # No line yet; process still alive
        if not line:
            continue

        # Play Button (Returns "PLAY")
        if "[gui/menu.py] PLAYBUTTONCLICKED" in line:
            debug("Main menu play button pressed")
            debug("Main menu GUI terminated (via gui/menu.py)")
            try:
                proc.terminate()
            except Exception:
                pass
            try:
                proc.wait(timeout=2)
            except Exception:
                pass
            debug("Main menu GUI terminated")
            return "PLAY"
        # Credits button (Returns "CREDITS")
        elif "[gui/menu.py] CREDITSBUTTONCLICKED" in line:
            debug("Credits button pressed")
            try:
                proc.terminate()
            except Exception:
                pass
            try:
                proc.wait(timeout=2)
            except Exception:
                pass
            debug("Main menu GUI terminated")
            return "CREDITS"
        # Leaderboard button (Returns "LEADERBOARD")
        elif "[gui/menu.py] LEADERBOARDBUTTONCLICKED" in line:
            debug("Leaderboard button pressed")
            try:
                proc.terminate()
            except Exception:
                pass
            try:
                proc.wait(timeout=2)
            except Exception:
                pass
            debug("Main menu GUI terminated")
            return "LEADERBOARD"

        # Add other buttons here similarly (leaderboard, developer portal)
        # Credits is just a template; IT DOES NOT DO ANYTHING!
        # To future self - do not add an "else break" statement or "else pass" statement, etcetera. Loop must not be stopped. Just end function here.



"""###################### Play Button / Main Game ######################"""

########### Let user set pre-match settings ###########
def runPreMatchSettings(): # Function for running pre match settings GUI
    debug("Starting pre-match settings screen")
    preMatchSettingsGUI = subprocess.Popen(
        ["python", "WorldWanderer-main/gui/preMatchSettingsSingleplayer.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    debug("PreMatchSettings (SINGLEPLAYER) running")

    while True:
        line = preMatchSettingsGUI.stdout.readline()

        if line:
            if "[gui/preMatchSettingsSingleplayer.py] START" in line:
                debug("preMatchSettings GUI requested to start match")
                try:
                    preMatchSettingsGUI.terminate()
                except Exception:
                    pass
                try:
                    preMatchSettingsGUI.wait(timeout=2)
                except Exception:
                    pass
                debug("preMatchSettings GUI terminated")
                return "STARTMATCH"

        if preMatchSettingsGUI.poll() is not None:
            break

    debug("GUI closed")
    try:
        preMatchSettingsGUI.terminate()
    except Exception:
        pass
    try:
        preMatchSettingsGUI.wait(timeout=2)
    except Exception:
        pass
    return "EXIT"

########### Run the main game ###########
def runMainGame(webAppProc): # Function for starting main game GUI
    debug("Starting main GUI")
    mainGui = subprocess.Popen(
        ["python", "WorldWanderer-main/gui/main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    debug("Main GUI running")

    while True:
        # If main game GUI is closed
        if mainGui.poll() is not None:
            break

        line = mainGui.stdout.readline()

        # If line is empty, continue
        if not line:
            continue

        # If line states RETURNTOMENU (i.e. when the "return to main menu" button is pressed). Returns "RETURNTOMENU"
        if "[gui/main.py] RETURNTOMENU" in line:
            debug("Main GUI requested return to main menu")
            try:
                mainGui.terminate()
            except Exception:
                pass
            try:
                mainGui.wait(timeout=2)
            except Exception:
                pass
            debug("Main GUI terminated")
            # IMPORTANT: Do NOT terminate webAppProc here; keep it for reuse
            return "RETURNTOMENU"

    # When "break" is called (when while True loop is stopped). Returns "EXIT"
    debug("Main GUI closed")
    try:
        mainGui.terminate()
    except Exception:
        pass
    try:
        mainGui.wait(timeout=2)
    except Exception:
        pass
    return "EXIT"



"""###################### Credits Screen ######################"""

########### Run credits screen ###########
def runCreditsScreen(): # Function for running credits GUI
    debug("Starting credits GUI")
    creditsGUI = subprocess.Popen(
        ["python", "WorldWanderer-main/gui/credits.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    debug("Credits GUI running")

    while True:
        # If credits GUI is closed
        if creditsGUI.poll() is not None:
            break

        line = creditsGUI.stdout.readline()

        # If line is empty, continue
        if not line:
            continue

        # If line states RETURNTOMENU (i.e. when the "return to main menu" button is pressed). Returns "RETURNTOMENU"
        if "[gui/credits.py] RETURNTOMENU" in line:
            debug("Credits GUI requested return to main menu")
            try:
                creditsGUI.terminate()
            except Exception:
                pass
            try:
                creditsGUI.wait(timeout=2)
            except Exception:
                pass
            debug("Credits GUI terminated")
            # IMPORTANT: Do NOT terminate webAppProc here; keep it for reuse
            return "RETURNTOMENU"

    # When "break" is called (when while True loop is stopped). Returns "EXIT"
    debug("GUI closed")
    try:
        creditsGUI.terminate()
    except Exception:
        pass
    try:
        creditsGUI.wait(timeout=2)
    except Exception:
        pass
    return "EXIT"



"""###################### Leaderboards ######################"""

########### Handle backend for each leaderboard (depending on what was selected) ###########
def leaderboardBackendHandler():
    debug(f"Starting leaderboard GUI")
    leaderboardGUI = subprocess.Popen(
        ["python", "WorldWanderer-main/gui/leaderboardSingleplayer.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    debug(f"Leaderboard GUI running")

    while True:
        # If selected GUI is closed
        if leaderboardGUI.poll() is not None:
            break

        line = leaderboardGUI.stdout.readline()

        # If line is empty, continue
        if not line:
            continue

        # If line states RETURNTOMENU (i.e. when the "return to main menu" button is pressed). Returns "RETURNTOMENU"
        if "RETURNTOMENU" in line:
            debug(f"Leaderboard GUI requested return to main menu")
            try:
                leaderboardGUI.terminate()
            except Exception:
                pass
            try:
                leaderboardGUI.wait(timeout=2)
            except Exception:
                pass
            debug(f"Leaderboard GUI terminated")
            # IMPORTANT: Do NOT terminate webAppProc here; keep it for reuse
            return "RETURNTOMENU"

    # When "break" is called (when while True loop is stopped). Returns "EXIT"
    debug("GUI closed")
    try:
        leaderboardGUI.terminate()
    except Exception:
        pass
    try:
        leaderboardGUI.wait(timeout=2)
    except Exception:
        pass
    return "EXIT"



"""###################### Run App ######################"""

########### Run app; metaphorically glues everything together ###########
def runApp(): # Function for running the app (when the file is ran)
    # Run loading screen to allow for backend processes to take place
    runLoadingScreen()

    # Clear coordinates if a person has used the app in the past:
    clearVariableStorageData()
    
    # Starts web app ONLY ONCE and keeps it across game sessions (closes when program terminates). Output should not be PIPE'd.
    debug("Starting web app")
    webApp = subprocess.Popen(
        ["python", "WorldWanderer-main/website/initialise.py"],
        # Note to self: Inherit stdio to avoid pipe buffer filling (or use DEVNULL if silence is wanted (stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,))
        stdout=None,
        stderr=None,
        text=False
    )
    waitForFlask() # Check if app is running

    # At this point, flask is running, coords are cleared, game is ready to launch.
    # Close loading screen so that it can be replaced with main menu
    closeLoadingScreen()
    try:
        while True:
            result = runMainMenu() # Result is what button is pressed

            # Play button
            if result == "PLAY":
                setSettings = runPreMatchSettings() # run pre match settings gui
                if setSettings == "STARTMATCH": # wait until pre match settings gui is ready/closed
                    pass
                elif setSettings == "EXIT":
                    break
                else:
                    debug("Unknown preMatchSettings return value, defaulting to pass")
                    pass
                result = runMainGame(webApp) # reuse the same web app
                if result == "RETURNTOMENU":
                    continue
                elif result == "EXIT":
                    break
            # Credits button
            elif result == "CREDITS":
                result = runCreditsScreen()
                if result == "RETURNTOMENU":
                    continue
                elif result == "EXIT":
                    break
            # Leaderboard button
            elif result == "LEADERBOARD":
                result = leaderboardBackendHandler()
                if result == "RETURNTOMENU":
                    continue
                elif result == "EXIT":
                    break
            else:
                break
    finally:
        # Clean shutdown of Flask
        try:
            webApp.terminate()
        except Exception:
            pass
        try:
            webApp.wait(timeout=3)
        except Exception:
            pass
        debug("Web app terminated")
        debug("Program terminated")

########### Runs this python file ###########
if __name__ == "__main__":
    runApp()
