// Fetches each countries' bounding box from json file
async function loadCountryBounds() {
    const res = await fetch("static/json/bboxValues.json");
    if (!res.ok) throw new Error("Failed to load country bounds JSON.");
    return await res.json();
}

// Selects a random country code from json file data.
function getRandomCountryCode(boundsData) {
    const codes = Object.keys(boundsData);
    return codes[Math.floor(Math.random() * codes.length)];
}

// From that country code, gets bounding box region for that respective country
function getRegionFromCountryCode(code, boundsData) {
    const country = boundsData[code];
    if (!country || !country.sw || !country.ne) {
      throw new Error(`HTTP 404: Invalid or missing bounding box for country code: ${code}`);
    }
    const { sw, ne } = country;
    return [sw.lat, sw.lon, ne.lat, ne.lon]; // [minLat, minLon, maxLat, maxLon]
}

// Gets a random coordinate from bounding box (otherwise it'd likely select the same photo over and over for that country)
function randomCoordInBBox([minLat, minLon, maxLat, maxLon]) {
    const lat = minLat + Math.random() * (maxLat - minLat);
    const lon = minLon + Math.random() * (maxLon - minLon);
    return { lat, lon };
}

// Gets random image
async function getRandomImage(region) {
    const attempts = 10; // Rate limit: 10 images before blocking access
    for (let i = 0; i < attempts; i++) {
        const center = randomCoordInBBox(region);
        const delta = 0.015; // ~1.6 km radius, under 0.001 sq deg 
        const bbox = [
        center.lon - delta,
        center.lat - delta,
        center.lon + delta,
        center.lat + delta
        ].join(",");

        const url = `https://graph.mapillary.com/images?fields=id,thumb_1024_url,computed_geometry&limit=1&bbox=${bbox}`;

        try {
        const res = await fetch(url, {
            headers: { Authorization: `OAuth ${MAPILLARYTOKEN}` }
        });

        if (!res.ok) {
            if (res.status === 401 || res.status === 403) {
            throw new Error("Unauthorized (HTTP 401/403; Check Mapillary access token).");
            }
            continue;
        }

        const data = await res.json();
        if (data && Array.isArray(data.data) && data.data.length > 0) {
            const imgObj = data.data[0];
            let imgUrl = imgObj.thumb_1024_url ||
                        `https://images.mapillary.com/${imgObj.id}/thumb-1024.jpg`;

            let latlon = null;
            if (imgObj.computed_geometry?.coordinates) {
            const [imgLon, imgLat] = imgObj.computed_geometry.coordinates;
            latlon = { lat: imgLat, lon: imgLon };
            }

            if (imgUrl) return { url: imgUrl, latlon };
        }
        } catch (err) {
        if (String(err).toLowerCase().includes("unauthorized")) throw err;
        }
    }
    throw new Error("HTTP 429: Rate limit (10) reached; try again in a moment."); // Rate limit
}

// Rate limit stuff
async function countdown(seconds, statusEl, rateLimitAttemptCounter) {
    return new Promise(resolve => {
        let remaining = seconds;
        statusEl.style.color = "orange";
        statusEl.style.display = "block";
        statusEl.textContent = `Rate limit hit (instance: ${rateLimitAttemptCounter}). Retrying in ${remaining}...`;

        const interval = setInterval(() => {
            remaining--;
            if (remaining > 0) {
                statusEl.textContent = `Rate limit hit (instance: ${rateLimitAttemptCounter}). Retrying in ${remaining}...`;
            } else {
                statusEl.style.color = "yellow";
                statusEl.textContent = "Retrying...";
                clearInterval(interval);
                resolve();
            }
        }, 1000);
    });
}

async function sendCoordinates(coordsVariable) { // Sends coordinates to text file so that GUI can read it for later
    const payload = coordsVariable ? coordsVariable : { error: "no-coordinates" } // If there are coordinates ("?"), post them. If not (":"), post an error.
    await fetch("http://127.0.0.1:8000/savemapillarycoordinates", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });
}

(async () => {
    const statusEl = document.getElementById("status");
    const imgEl = document.getElementById("img");
    const countryBounds = await loadCountryBounds();
    let retries = 0;
    const maxRetries = 5;

    while (retries < maxRetries) {
        try {
            const countryBounds = await loadCountryBounds();
            const randomCode = getRandomCountryCode(countryBounds);
            const REGION = getRegionFromCountryCode(randomCode, countryBounds);
            console.log(`Selected country: ${countryBounds[randomCode].fullName}`);

            const { url, latlon } = await getRandomImage(REGION);

            imgEl.src = url;
            imgEl.style.display = "block";
            imgEl.alt = `Mapillary Image (if you see this message outside developer tools, image could not be rendered. Hint: The country is ${countryBounds[randomCode].fullName})`;
            statusEl.style.display = "none";

            console.log("Mapillary image generated");
            console.log("Url: " + url);
            if (latlon) {
                console.log(`Approximate location: ${latlon.lat.toFixed(5)}, ${latlon.lon.toFixed(5)}`);
                sendCoordinates(latlon);
            } else {
                console.log("Approximate location unknown");
            }
            break;
        } catch (e) {
            console.error(e);

            if (String(e).includes("HTTP 429")) {
                console.log("-!- RATE LIMIT REACHED -!-")
                retries++;
                if (retries >= maxRetries) {
                    statusEl.textContent = "Rate limit reached too many times (50 attempts). Please try again later."
                    statusEl.style.color = "red";
                    imgEl.style.display = "none";
                    break;
                }
                await countdown(5, statusEl, retries);
                continue;
            } else {
                statusEl.textContent = e.message || "Failed to load image.";
                statusEl.style.color = "red";
                imgEl.style.display = "none";
                console.error(e);
                break;
            }
        }
    }
})();
