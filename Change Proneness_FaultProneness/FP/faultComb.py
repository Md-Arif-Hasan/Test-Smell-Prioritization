import os
import pandas as pd

def combine_csv_files(source_folder, destination_file):
    """
    Combine all CSV files from source folder into a single destination file without spacing.
    
    Parameters:
    source_folder (str): Path to the folder containing source CSV files
    destination_file (str): Path for the output combined CSV file
    """
    try:
        # Get list of all CSV files in the folder
        csv_files = [f for f in os.listdir(source_folder) if f.endswith('.csv')]
        
        if not csv_files:
            print(f"No CSV files found in {source_folder}")
            return
            
        # Create empty list to store dataframes
        dfs = []
        
        # Read each CSV file
        for file in csv_files:
            print(f"Processing: {file}")
            # Read the current CSV
            df = pd.read_csv(os.path.join(source_folder, file))
            
            # Add project name as a column 
            df['Source_File'] = file.replace('.csv', '')
            
            # Append to list of dataframes
            dfs.append(df)
        
        # Concatenate all dataframes
        merged_df = pd.concat(dfs, ignore_index=True)
        
        # Create destination directory if it doesn't exist
        os.makedirs(os.path.dirname(destination_file), exist_ok=True)
        
        # Save the merged dataframe
        merged_df.to_csv(destination_file, index=False)
        print(f"\nSuccess! Combined file saved as: {destination_file}")
        print(f"Total files processed: {len(csv_files)}")
        print(f"Total rows in combined file: {len(merged_df)}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Paths
source_folder = r'.../Fault_proneness'
destination_file = r'.../Fault_proneness_combined.csv'

# Run the combination
combine_csv_files(source_folder, destination_file)