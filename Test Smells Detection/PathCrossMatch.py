import pandas as pd
import os

# Define the folder path containing the CSV files
folder_path = "/home/siam/Desktop/volume1/MS_Papers_Arif/Data/SmellsPlusCPP"

# Initialize a list to store the results
results = []

# Loop through all CSV files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".csv"):
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path)
        
        # Ensure the columns 'TestFile' and 'File Path' exist
        if 'TestFile' in df.columns and 'File Path' in df.columns:
            # Find similar file paths
            similar_paths = df[df['TestFile'] == df['File Path']]
            
            # Count the number of similar file paths
            count = similar_paths.shape[0]
            
            # Append the result to the list
            results.append({
                'Project Name': file_name.replace('.csv', ''),  # Remove .csv extension
                'Similar File Path Count': count
            })
        else:
            print(f"Error: 'TestFile' or 'File Path' columns not found in {file_name}.")

# Convert the results list to a DataFrame
results_df = pd.DataFrame(results)

# Save the results to a new CSV file
report_path = ".../report.csv"
results_df.to_csv(report_path, index=False)

print(f"Report saved to {report_path}")