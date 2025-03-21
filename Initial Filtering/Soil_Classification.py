import tensorflow as tf
import numpy as np
import cv2
import pandas as pd

# Load the trained model
model_path = "soil_model.h5"
model = tf.keras.models.load_model(model_path)

# Define class labels (must match training labels)
class_labels = ["Black Soil", "Cinder Soil", "Laterite Soil", "Peat Soil", "Yellow Soil"]

# Load dataset with correct encoding
csv_path = "Crop_req_data.xlsx"
df = pd.read_csv(csv_path, encoding="ISO-8859-1")  # Change encoding if necessary

# Ensure correct column name
soil_column = "Soil Type"  # Change if necessary
df[soil_column] = df[soil_column].astype(str).str.strip().str.lower()  # Clean column values

def preprocess_image(image_path):
    """Reads an image, resizes it to 224x224, normalizes pixel values, and returns the processed image."""
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Error: Could not read image. Check the file path!")
    image = cv2.resize(image, (224, 224))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image

def predict_soil(image_path):
    """Predicts the soil type from the input image."""
    image = preprocess_image(image_path)
    prediction = model.predict(image)
    predicted_class = np.argmax(prediction)
    soil_type = class_labels[predicted_class]
    confidence = np.max(prediction) * 100
    print(f"Predicted Soil Type: {soil_type} ({confidence:.2f}% confidence)")
    return soil_type

def filter_dataset_by_soil(soil_type):
    """Filters the dataset and saves it as a new CSV file."""
    soil_type = soil_type.lower().replace(" soil", "").strip()  # Remove "Soil" suffix
    filtered_df = df[df[soil_column].str.contains(soil_type, case=False, na=False)]

    if not filtered_df.empty:
        output_csv = "filtered_data.csv"
        filtered_df.to_csv(output_csv, index=False, encoding="ISO-8859-1")  # Keep same format
        print(f"Filtered data saved to {output_csv}")
    else:
        print("No matching data found. Check CSV formatting.")

    return filtered_df

if __name__ == "__main__":
    image_path = "laterite soil 2.webp"  # Change to your image file
    predicted_soil = predict_soil(image_path)
    
    # Filter dataset and save to CSV
    filtered_df = filter_dataset_by_soil(predicted_soil)
    
    # Print the filtered data
    if not filtered_df.empty:
        print("Filtered Data:")
        print(filtered_df)
