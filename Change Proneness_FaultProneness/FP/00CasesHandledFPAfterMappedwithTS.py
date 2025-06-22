import pandas as pd
import os

# Define input and output paths
input_file = '.../TS_FP/tsfp.csv'
output_file = '.../00CaseHandlesFP.csv'

# Read the input CSV
df = pd.read_csv(input_file)

# Print initial statistics
print(f"Original number of rows: {len(df)}")

# Create a mask for cases where either Production or Test is faulty
faulty_mask = (df['Prod_Is_Faulty'] == 1) | (df['Test_Is_Faulty'] == 1)

# Filter the dataframe to keep only cases where at least one is faulty
filtered_df = df[faulty_mask]

# Print detailed statistics about the filtering
print("\nDetailed Statistics:")
print("-" * 50)
print("Cases in original dataset:")
print(f"(0-0) Neither faulty: {len(df[~faulty_mask])}")
print(f"(1-0) Only Production faulty: {len(df[(df['Prod_Is_Faulty'] == 1) & (df['Test_Is_Faulty'] == 0)])}")
print(f"(0-1) Only Test faulty: {len(df[(df['Prod_Is_Faulty'] == 0) & (df['Test_Is_Faulty'] == 1)])}")
print(f"(1-1) Both faulty: {len(df[(df['Prod_Is_Faulty'] == 1) & (df['Test_Is_Faulty'] == 1)])}")

# Create output directory if it doesn't exist
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Save the filtered dataframe
filtered_df.to_csv(output_file, index=False)

# Print final statistics
print(f"\nFinal number of rows (excluding 0-0 cases): {len(filtered_df)}")
print(f"Number of rows removed: {len(df) - len(filtered_df)}")
print(f"\nOutput file saved to: {output_file}")

# Additional verification
print("\nVerification of filtered dataset:")
print("-" * 50)
zero_zero_cases = len(filtered_df[(filtered_df['Prod_Is_Faulty'] == 0) & (filtered_df['Test_Is_Faulty'] == 0)])
print(f"Number of (0-0) cases in filtered dataset: {zero_zero_cases} (should be 0)")