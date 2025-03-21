import pandas as pd
from Testing_sentinel import nitrogen, phosphorus, potassium, soil_ph

# Load the filtered crop dataset
csv_path = "filtered_data.csv"
df = pd.read_csv(csv_path, encoding="ISO-8859-1")

# Extracted NPK and pH values from Sentinel (Replace with actual values from your script)
extracted_N = nitrogen   # Example extracted Nitrogen value
extracted_P = phosphorus   # Example extracted Phosphorus value
extracted_K = potassium  # Example extracted Potassium value
extracted_pH = soil_ph  # Example extracted Soil pH value

# Ensure correct column names (modify if necessary)
soil_column = "Soil Type"
N_column = "N Content (kg/ha)"
P_column = "P Content (kg/ha)"
K_column = "K Content (kg/ha)"
pH_column = "pH"

def parse_range(value):
    """Parses range values like '50-200' (NPK) or '5.5-7.5' (pH) and returns min & max as floats."""
    if isinstance(value, str) and "-" in value:
        min_val, max_val = map(float, value.split("-"))  # Convert to float for proper range comparison
        return min_val, max_val
    return float(value), float(value)  # If it's a single number, treat min=max

def filter_by_npk(df):
    """Filters crops that fall within the extracted NPK and pH range."""
    filtered_rows = []

    for _, row in df.iterrows():
        min_N, max_N = parse_range(row[N_column])
        min_P, max_P = parse_range(row[P_column])
        min_K, max_K = parse_range(row[K_column])
        min_pH, max_pH = parse_range(row[pH_column])

        # Check if extracted values fall within the crop's NPK & pH range
        if (min_N <= extracted_N <= max_N and
            min_P <= extracted_P <= max_P and
            min_K <= extracted_K <= max_K and
            min_pH <= extracted_pH <= max_pH):
            filtered_rows.append(row)

    return pd.DataFrame(filtered_rows)

# Apply filtering
filtered_npk_df = filter_by_npk(df)

# Save the final filtered dataset
output_csv = "filtered_NPK.csv"
filtered_npk_df.to_csv(output_csv, index=False, encoding="ISO-8859-1")

# Print final status
if not filtered_npk_df.empty:
    print(f"✅ Final filtered data saved as {output_csv}")
    print(filtered_npk_df)
else:
    print("⚠️ No crops matched the given NPK & pH range.")
