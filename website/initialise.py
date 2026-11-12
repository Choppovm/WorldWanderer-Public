from flask import *
import os

# Define web app
app = Flask(__name__)

@app.route("/") # Main page
def index():
    return "Select desired web page:<br><a href='osm'>[OSM]</a><br><a href='mapillary'>[MAPILLARY]</a><br><a href='ping'>[PING]</a>"

@app.route("/ping") # Ping page to check if web app is running
def ping():
    return redirect("/"), 200

@app.route("/osm") # OSM page
def osm():
    return render_template("osm.html")

@app.route("/mapillary") # Mapillary page
def mapillary():
    # Get the absolute path to project root
    projectRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tokenPath = os.path.join(projectRoot, "storage", "mapillaryaccesstoken.txt")

    # Build full path to token file
    with open(tokenPath, "r") as f:
        mapillaryToken = f.read().strip()
    return render_template("mapillary.html" , token=mapillaryToken) # Pass token to HTML file

@app.route("/savemapillarycoordinates", methods=["POST"]) # Send coordinates of mapillary image to currentMapillaryCoords.txt
def savemapillarycoordinates():
    data = request.get_json()
    if "error" in data: # Failed to get coordinates for whatever reason, does not send to the file
        print("JS reported failure:", data["error"])
        with open("WorldWanderer-main/storage/currentMapillaryCoords.txt", "w") as file:
            file.write(data["error"])
        return {"status": "skipped"}
    lat = data.get("lat")
    lon = data.get("lon")
    with open("WorldWanderer-main/storage/currentMapillaryCoords.txt", "w") as file:
        file.write(f"{lat},{lon}\n")
    
    # Write to a file - alerts GUI to start the timer so that it doesn't start while the image is still loading
    with open("WorldWanderer-main/storage/mapillaryReady.txt", "w") as f:
        f.write("READY")
    return {"status": "ok"}

@app.route("/saveosmcoordinates", methods=["POST"]) # Send coordinates of the user's placed osm pin to currentUserGuessCoords.txt
def saveosmcoordinates():
    data = request.get_json()
    if "error" in data: # Failed to get coordinates for whatever reason, does not send to the file
        print("JS reported failure:", data["error"])
        with open("WorldWanderer-main/storage/currentUserGuessCoords.txt", "w") as file:
            file.write(data["error"])
        return {"status": "skipped"}
    lat = data.get("lat")
    lon = data.get("lon")
    with open("WorldWanderer-main/storage/currentUserGuessCoords.txt", "w") as file:
        file.write(f"{lat},{lon}\n")
    return {"status": "ok"}

@app.route("/plotmapillarycoords", methods=["POST", "GET"]) # Sends mapillary coordinates to osm so that a pin can be placed
def plotmapillarycoords():
    try:
        with open("WorldWanderer-main/storage/currentMapillaryCoords.txt", "r") as file:
            line = file.read().strip()
        if "," in line:
            lat, lon = line.split(",")
            return {"lat": float(lat), "lon": float(lon)}
        else:
            return {"error": "invalid-data"}
    except FileNotFoundError:
        return {"error": "no-file"}
    # GET requests to 127.0.0.1:8000/plotmapillarycoords will respond with something like { "lat": coord, "lon": coord }

# Start local server
if __name__ == "__main__":
    app.run(debug=False, port=8000) # 8th sept 2025 - changed to false since app.py will be polling the /ping endpoint, dont want terminal being flooded.
    # Port prevents conflicts with other web apps should I need multiple in the future (flask default is 5000)
    # Debug gives error messages + auto-reloads on code changes, only remove when done with web app
