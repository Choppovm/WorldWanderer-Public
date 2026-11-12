// Creating OSM map, defining rules/limitations
// Zoom level 2 is more practical for global view
// Zoom restrictions prevent 
const map = L.map("map", {
    minZoom: 2,
    maxZoom: 18
}).setView([0, 0], 2);

// Define OSM bounds (prevent being able to scroll left/right infinitely)
const boundsLimit = L.latLngBounds(
    L.latLng(-85, -180),
    L.latLng(85, 180)
);
map.setMaxBounds(boundsLimit);
map.on("drag", function () {
    map.panInsideBounds(boundsLimit, { animate: false });
});

// Prevent map from generating infinitely
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    noWrap: true
}).addTo(map);

// Display where images are gathered from (UK, USA)
var tempbounds = [
    [[50.400000, -4.000000], [50.300000, -4.200000]],
    [[50.717000, -1.269000], [50.686000, -1.327000]],
    [[50.735000, -1.138000], [50.717000, -1.196000]],
    [[51.559000, 0.065000], [51.448000, -0.313000]],
    [[51.566000, -2.378000], [51.403000, -2.706000]],
    [[51.549000, -3.085000], [51.445000, -3.260000]],
    [[52.242484, 0.233459], [52.161659, 0.067291]],
    [[51.932794, 0.972290], [51.857770, 0.828094]],
    [[52.102687, 1.338272], [52.019494, 1.087646]],
    [[52.657957, -1.649323], [52.325898, -2.232971]],
    [[52.640119, -0.098190], [52.506539, -0.336456]],
    [[53.563991, -2.068863], [53.396402, -2.389526]],
    [[53.870360, -1.429596], [53.725937, -1.683655]],
    [[54.006573, -1.007309], [53.918481, -1.163864]],
    [[55.982999, -3.069992], [55.888356, -3.310318]],
    [[55.939204, -3.898087], [55.712343, -4.568939]],
    [[56.432132, -3.378639], [56.370748, -3.503952]],
    [[56.518521, -2.680664], [56.450254, -3.076172]],
    [[53.439803, -6.045227], [53.235150, -6.527252]],
    [[53.321229, -8.944588], [53.251218, -9.136848]],
    [[51.939759, -8.377258], [51.856050, -8.653290]],
    [[54.290486, -8.432007], [54.247767, -8.517494]],
    [[54.634080, -5.765076], [54.492703, -6.111145]],
    [[32.421966, -86.131096], [32.305351, -86.348763]],
    [[33.737863, -111.448059], [33.144078, -112.681274]],
    [[34.830148, -92.145081], [34.643315, -92.523422]],
    [[34.229311, -116.921997], [33.453446, -118.427124]],
    [[40.044327, -104.658508], [39.488916, -105.323181]],
    [[41.840891, -72.446594], [41.500212, -72.828369]],
    [[39.204303, -75.489464], [39.085778, -75.568428]],
    [[30.547550, -84.116821], [30.368743, -84.412079]],
    [[34.007064, -84.004211], [33.482761, -84.689484]],
    [[43.761122, -116.069183], [43.451769, -116.731110]],
    [[39.874706, -89.523468], [39.725630, -89.790573]],
    [[40.019163, -85.882874], [39.565288, -86.487122]],
    [[41.786614, -93.452454], [41.506372, -93.945465]],
    [[39.295015, -94.228363], [38.751798, -95.045471]],
    [[38.363201, -85.458527], [38.080444, -85.926819]],
    [[30.576427, -90.933151], [30.297499, -91.244888]],
    [[39.478075, -76.409225], [39.193325, -76.863098]],
    [[42.403167, -71.015625], [42.314853, -71.154327]],
    [[42.823546, -82.784729], [42.030617, -83.822937]],
    [[45.213960, -92.842712], [44.611585, -93.663940]],
    [[32.476743, -90.065918], [32.152833, -90.359802]],
    [[38.615529, -92.121048], [38.519936, -92.308502]],
    [[46.744558, -111.816788], [46.552181, -112.093506]],
    [[40.930013, -96.503906], [40.652322, -96.873322]],
    [[36.326005, -114.906006], [35.933230, -115.370178]],
    [[43.055325, -71.371307], [42.890988, -71.527863]],
    [[40.289927, -74.608154], [40.122062, -74.930878]],
    [[35.280928, -106.460266], [35.006841, -106.799469]],
    [[40.933120, -73.299408], [40.588710, -74.263458]],
    [[36.047853, -78.361359], [35.566573, -78.961487]],
    [[46.917900, -100.639572], [46.732262, -100.959549]],
    [[40.169337, -82.768250], [39.798830, -83.217316]],
    [[36.308424, -95.648346], [35.858800, -96.119385]],
    [[45.721481, -122.298431], [45.338470, -123.057861]],
    [[40.690915, -79.681091], [40.245712, -80.332031]],
    [[34.073568, -80.912247], [33.930643, -81.112747]],
    [[44.192937, -103.005066], [44.008462, -103.368988]],
    [[36.244189, -86.585312], [35.907770, -86.911469]],
    [[30.140223, -94.883423], [29.412896, -96.026001]],
    [[41.337687, -111.695251], [40.480157, -112.186890]],
    [[37.722711, -77.135010], [37.216819, -77.862854]],
    [[48.030392, -122.005920], [46.886157, -122.827148]],
    [[38.382017, -81.553230], [38.311449, -81.763000]],
    [[43.442944, -87.819214], [42.766958, -88.398743]],
    [[41.217876, -104.704514], [41.089617, -104.889908]]
]; // NE-LAT, NE-LON, SW-LAT, SW-LON

for (let i = 0; i < tempbounds.length; i++) {
    // Extract NE and SW points
    let ne = tempbounds[i][0];
    let sw = tempbounds[i][1];

    // Reorder to [SW, NE] for Leaflet
    let leafletBounds = [
        [sw[0], sw[1]], // SW lat, SW lon
        [ne[0], ne[1]]  // NE lat, NE lon
    ];

    // Draw rectangle
    L.rectangle(leafletBounds, { color: "#006700", weight: 3 }).addTo(map);
}

// Function for sending coordinates of a placed pin to file
async function sendCoordinates(coordsVariable) { // Sends coordinates to text file so that GUI can read it for later
    const payload = coordsVariable ? coordsVariable : { error: "no-coordinates" } // If there are coordinates ("?"), post them. If not (":"), post an error.
    await fetch("http://127.0.0.1:8000/saveosmcoordinates", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });
}

// Define icons for markers (https://leafletjs.com/reference.html#icon)
var bluePinIcon = L.icon({
    iconUrl: "/static/assets/images/bluePinAssets/markerIcon.png",
    shadowUrl: "/static/assets/images/bluePinAssets/markerShadow.png",
    // These are Leaflet’s defaults for the standard marker
    iconSize:     [25, 41],
    iconAnchor:   [12, 41],
    popupAnchor:  [1, -34],
    shadowSize:   [41, 41],
    shadowAnchor: [12, 41]
});
var redPinIcon = L.icon({
    iconUrl: "/static/assets/images/redPinAssets/markerIcon.png",
    shadowUrl: "/static/assets/images/redPinAssets/markerShadow.png",
    // These are Leaflet’s defaults for the standard marker
    iconSize:     [25, 41],
    iconAnchor:   [12, 41],
    popupAnchor:  [1, -34],
    shadowSize:   [41, 41],
    shadowAnchor: [12, 41]
})

// Function for when you click on the map (place a marker)
let currentUserMarker = null;
map.on("click", function(e) {
    // Log coordinates to txt file
    const { lat, lng } = e.latlng;
    latlon = { lat: lat, lon: lng };
    sendCoordinates(latlon)

    // Remove previous marker if it exists
    if (currentUserMarker) {
        map.removeLayer(currentUserMarker);
    }
                
    // Add new marker
    currentUserMarker = L.marker([lat, lng], {
        icon: bluePinIcon
    }).addTo(map);

    // Draw line between the two when guessed
    drawLineBetweenMarkers()
                
    // Print coordinates to console
    console.log(`Marker placed at: Latitude ${lat}, Longitude ${lng}`);
});

// Function for when guess is submitted
let currentMapillaryMarker = null;
async function plotMapillaryCoords() {
    try {
        const response = await fetch("http://127.0.0.1:8000/plotmapillarycoords");
        const data = await response.json();

        if (data.lat && data.lon) {
            // Place a red pin at the Mapillary coords
            currentMapillaryMarker = L.marker([data.lat, data.lon], {
                icon: redPinIcon
            }).addTo(map);

            // Optionally pan/zoom to it
            map.setView([data.lat, data.lon], 5);

                // Draw line between the two when guessed
                drawLineBetweenMarkers()

            console.log(`Mapillary coords plotted at: ${data.lat}, ${data.lon}`);
        } else {
            console.error("No valid coords from server:", data);
        }
    } catch (err) {
        console.error("Error fetching Mapillary coords:", err);
    }
}

// Function that draws line between mapillary image point and user point
let connectionLine = null;
function drawLineBetweenMarkers() {
    if (currentUserMarker && currentMapillaryMarker) {
        const userLatLng = currentUserMarker.getLatLng();
        const mapillaryLatLng = currentMapillaryMarker.getLatLng();

        // Remove previous line if it exists
        if (connectionLine) {
            map.removeLayer(connectionLine);
        }

        // Draw new line
        connectionLine = L.polyline([userLatLng, mapillaryLatLng], {
            color: 'purple',
            weight: 3,
            opacity: 0.7,
            smoothFactor: 1
        }).addTo(map);

        console.log("Line drawn between user marker and Mapillary marker.");

        // Prevent user from moving their original marker once guess is made
        map.off("click")
    }
}
