import os
import pandas as pd

def aggregate_csv_files(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    for project_folder in os.listdir(input_dir):
        project_path = os.path.join(input_dir, project_folder)
        
        # Skip if not a directory
        if not os.path.isdir(project_path):
            continue
        
        # List to hold dataframes for this project
        dfs = []
        
        # Read all CSV files in the project folder
        for csv_file in os.listdir(project_path):
            if csv_file.endswith('.csv'):
                file_path = os.path.join(project_path, csv_file)
                df = pd.read_csv(file_path)
                dfs.append(df)
        
        # Combine project dataframes
        if dfs:
            combined_df = pd.concat(dfs, ignore_index=True)
            
            # Save project-specific aggregated CSV
            output_path = os.path.join(output_dir, f"{project_folder}_aggregated.csv")
            combined_df.to_csv(output_path, index=False)
            
            print(f"Aggregated {len(dfs)} files for {project_folder}")

# Paths
input_dir = '/home/siam/Desktop/volume1/MS_Papers_Arif/Data/XMLtoCSV'
output_dir = '/home/siam/Desktop/volume1/MS_Papers_Arif/Data/AggregatedSmellsTogether'

# Run aggregation
aggregate_csv_files(input_dir, output_dir)