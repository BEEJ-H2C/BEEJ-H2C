import requests
import numpy as np
import matplotlib.pyplot as plt
from sentinelhub import SHConfig, MimeType, SentinelHubRequest, CRS, BBox, bbox_to_dimensions, DataCollection

# 🔹 Your API Keys
GOOGLE_API_KEY = ""
SENTINEL_CLIENT_ID = ""
SENTINEL_CLIENT_SECRET = ""

# 🔹 Sentinel Configuration
config = SHConfig()
config.sh_client_id = SENTINEL_CLIENT_ID
config.sh_client_secret = SENTINEL_CLIENT_SECRET

def get_coordinates(address, api_key):
    """Convert address to latitude & longitude using Google Maps API."""
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(url).json()
    if response["status"] == "OK":
        location = response["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    else:
        raise Exception(f"Geocoding error: {response['status']}")

def fetch_sentinel_image(lat, lon, evalscript, bands_description):
    """
    Fetch Sentinel-2 image using the specified evalscript.
    bbox_size determines how 'zoomed in' or 'zoomed out' the final image is.
    """
    bbox_size = 0.005  # ~500m bounding box around the location
    bbox = BBox([
        lon - bbox_size / 2,
        lat - bbox_size / 2,
        lon + bbox_size / 2,
        lat + bbox_size / 2
    ], crs=CRS.WGS84)
    size = bbox_to_dimensions(bbox, resolution=10)  # 10m resolution

    request = SentinelHubRequest(
        evalscript=evalscript,
        input_data=[
            SentinelHubRequest.input_data(
                DataCollection.SENTINEL2_L2A,
                maxcc=0.2,  # maximum cloud coverage
                time_interval=("2024-01-01", "2024-12-31")
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=bbox,
        size=size,
        config=config
    )
    return request.get_data()[0], bands_description

def extract_np_ph_values(image):
    """Extract proxies for Nitrogen (N), Phosphorus (P), Potassium (K), and Soil pH from Sentinel-2 bands."""
    
    def calculate_nitrogen_index(image):
        # Proxy: B05 / B08 (Red Edge / NIR)
        return np.divide(
            image[:, :, 0], image[:, :, 3],
            out=np.zeros_like(image[:, :, 0]),
            where=image[:, :, 3] != 0
        )

    def calculate_phosphorus_index(image):
        # Proxy: B06 / B11
        return np.divide(
            image[:, :, 1], image[:, :, 4],
            out=np.zeros_like(image[:, :, 1]),
            where=image[:, :, 4] != 0
        )

    def calculate_potassium_index(image):
        # Proxy: B07 / B12
        return np.divide(
            image[:, :, 2], image[:, :, 5],
            out=np.zeros_like(image[:, :, 2]),
            where=image[:, :, 5] != 0
        )

    def calculate_soil_ph(image):
        # Proxy formula for pH: 4.5 + 3.5 * (B12 / B08) - 2.2 * (B11 / B06)
        ph_part1 = np.divide(
            image[:, :, 5], image[:, :, 3],
            out=np.zeros_like(image[:, :, 5]),
            where=image[:, :, 3] != 0
        )
        ph_part2 = np.divide(
            image[:, :, 4], image[:, :, 1],
            out=np.zeros_like(image[:, :, 4]),
            where=image[:, :, 1] != 0
        )
        ph = 4.5 + 3.5 * ph_part1 - 2.2 * ph_part2
        return np.clip(ph, 4.5, 9.0)  # Soil pH typically ranges from 4.5 to 9.0

    nitrogen_index = calculate_nitrogen_index(image)
    phosphorus_index = calculate_phosphorus_index(image)
    potassium_index = calculate_potassium_index(image)
    soil_ph_index = calculate_soil_ph(image)

    # Compute means safely: replace NaNs with default values.
    nitrogen_value = int(np.nan_to_num(np.nanmean(nitrogen_index), nan=0) * 100)
    phosphorus_value = int(np.nan_to_num(np.nanmean(phosphorus_index), nan=0) * 100)
    potassium_value = int(np.nan_to_num(np.nanmean(potassium_index), nan=0) * 100)
    soil_ph_value = round(np.nan_to_num(np.nanmean(soil_ph_index), nan=6.5), 2)

    return nitrogen_value, phosphorus_value, potassium_value, soil_ph_value

# def plot_images(hyperspectral_image, true_color_image):
#     """Plot the hyperspectral-like and true-color images with interpolation to reduce pixelation."""
#     fig, axes = plt.subplots(1, 4, figsize=(20, 5), dpi=150)

#     axes[0].imshow(hyperspectral_image[:, :, 0], cmap="Reds", interpolation="bilinear")
#     axes[0].set_title("Red Edge (B05)")

#     axes[1].imshow(hyperspectral_image[:, :, 3], cmap="Greens", interpolation="bilinear")
#     axes[1].set_title("Near-Infrared (B08)")

#     axes[2].imshow(hyperspectral_image[:, :, 5], cmap="Purples", interpolation="bilinear")
#     axes[2].set_title("Shortwave Infrared (B12)")

#     axes[3].imshow(true_color_image, interpolation="bilinear")
#     axes[3].set_title("True-Color Image")

#     plt.tight_layout()
#     plt.show()

# Extract values and store them as **global variables** for direct import
address = "Raigad, Maharashtra, India"  # Replace with actual location
lat, lon = get_coordinates(address, GOOGLE_API_KEY)

# Hyperspectral Evalscript
hyperspectral_evalscript = """
//VERSION=3
function setup() {
    return {
        input: ["B05", "B06", "B07", "B08", "B11", "B12"],
        output: { bands: 6, sampleType: "FLOAT32" }
    };
}
function evaluatePixel(sample) {
    return [sample.B05, sample.B06, sample.B07, sample.B08, sample.B11, sample.B12];
}
"""

# Fetch Sentinel-2 Images
hyperspectral_image, _ = fetch_sentinel_image(lat, lon, hyperspectral_evalscript, ["B05", "B06", "B07", "B08", "B11", "B12"])

# **Global variables for direct import**
nitrogen, phosphorus, potassium, soil_ph = extract_np_ph_values(hyperspectral_image)

# Debug: Print values to confirm they are extracted correctly
print(f"Nitrogen: {nitrogen}, Phosphorus: {phosphorus}, Potassium: {potassium}, Soil pH: {soil_ph}")

# Show the images
# plot_images(hyperspectral_image, true_color_image)
