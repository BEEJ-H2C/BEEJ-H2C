# Import required libraries
import pandas as pd
import numpy as np
from datetime import datetime

# Load the dataset for weights
weights_path = "DATASET/Dataset_for_Weights.csv"
data = pd.read_csv(weights_path)

# Check if required columns exist
required_columns = ["Arrival_Date", "Min_Price", "Max_Price", "Modal_Price"]
if not all(col in data.columns for col in required_columns):
    raise ValueError("One or more required columns are missing in the dataset.")

# Convert Arrival_Date to datetime
data["Arrival_Date"] = pd.to_datetime(data["Arrival_Date"], errors='coerce')

# Get today's date for recency calculation
today_date = datetime.today()

# Calculate Profit Margin
data["Profit_Margin"] = np.where(
    data["Max_Price"] != data["Min_Price"],
    (data["Modal_Price"] - data["Min_Price"]) / (data["Max_Price"] - data["Min_Price"]),
    0
)

# Calculate Recency Weight
data["Days_Since_Arrival"] = (today_date - data["Arrival_Date"]).dt.days
data["Recency_Weight"] = 1 / (data["Days_Since_Arrival"] + 1)  # Avoid division by zero

# Normalize weights for both parameters
profit_weight = data["Profit_Margin"].mean()
recency_weight = data["Recency_Weight"].mean()

# Normalize the weights to sum to 1
total_weight = profit_weight + recency_weight
W1 = profit_weight / total_weight
W2 = recency_weight / total_weight

# Print calculated weights
print("\nCalculated Weights:")
print(f"Profit Margin Weight (W1): {W1:.4f}")
print(f"Recency Weight (W2): {W2:.4f}\n")

# Load single crop data (e.g., wheat) to calculate the final crop score
wheat_path = "DATASET/Wheat_for_Demo.xlsx"
wheat_data = pd.read_excel(wheat_path)

# Calculate score for all rows of wheat data and average it
wheat_data["Profit_Margin"] = np.where(
    wheat_data["Max_Price"] != wheat_data["Min_Price"],
    (wheat_data["Modal_Price"] - wheat_data["Min_Price"]) / (wheat_data["Max_Price"] - wheat_data["Min_Price"]),
    0
)

wheat_data["Days_Since_Arrival"] = (today_date - pd.to_datetime(wheat_data["Arrival_Date"])).dt.days
wheat_data["Recency_Weight"] = 1 / (wheat_data["Days_Since_Arrival"] + 1)

# Calculate crop score for each row and average the scores
wheat_data["Crop_Score"] = W1 * wheat_data["Profit_Margin"] + W2 * wheat_data["Recency_Weight"]
wheat_data["Crop_Score"] = wheat_data["Crop_Score"].clip(0, 1)

# Get the final crop score by averaging all rows
final_crop_score = wheat_data["Crop_Score"].mean()

# Print final crop score
print(f"Final Crop Score for Wheat: {final_crop_score:.4f}")