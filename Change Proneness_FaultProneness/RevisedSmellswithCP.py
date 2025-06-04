import pandas as pd
import os
from pathlib import Path

def process_csv_files(input_folder, output_folder):
    """
    Process CSV files to keep only rows where TestFile and File Path match exactly.
    Saves filtered results to new CSV files.
    
    Args:
        input_folder (str): Path to the folder containing input CSV files
        output_folder (str): Path to save the filtered CSV files
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Get all CSV files in the input folder
    csv_files = list(Path(input_folder).glob('*.csv'))
    
    for csv_file in csv_files:
        print(f"\nProcessing {csv_file.name}...")
        
        try:
            # Read the CSV file
            df = pd.read_csv(csv_file)
            
            # Check if required columns exist
            if 'TestFile' not in df.columns or 'File Path' not in df.columns:
                print(f"Warning: Required columns not found in {csv_file.name}")
                continue
            
            # Store original column order
            original_columns = df.columns.tolist()
            
            # Convert paths to standard format for comparison
            df['TestFile'] = df['TestFile'].apply(lambda x: str(Path(x)).replace('\\', '/'))
            df['File Path'] = df['File Path'].apply(lambda x: str(Path(x)).replace('\\', '/'))
            
            # Keep only rows where paths match exactly
            df_filtered = df[df['TestFile'] == df['File Path']]
            
            # Create output filename
            output_file = Path(output_folder) / f"_{csv_file.name}"
            
            # Save the filtered CSV
            df_filtered.to_csv(output_file, index=False)
            
            # Print summary statistics
            total_rows = len(df)
            matching_rows = len(df_filtered)
            removed_rows = total_rows - matching_rows
            
            print(f"File: {csv_file.name}")
            print(f"Original rows: {total_rows}")
            print(f"Rows with exact path matches: {matching_rows}")
            print(f"Rows removed (non-matching paths): {removed_rows}")
            
            # Print examples of removed rows (up to 3 examples)
            if removed_rows > 0:
                print("\nExamples of removed rows (non-matching paths):")
                removed_df = df[df['TestFile'] != df['File Path']].head(3)
                for _, row in removed_df.iterrows():
                    print("\nTestFile:")
                    print(row['TestFile'])
                    print("File Path:")
                    print(row['File Path'])
                    print("-" * 50)
            
        except Exception as e:
            print(f"Error processing {csv_file.name}: {str(e)}")
            continue

if __name__ == "__main__":
    input_folder = ".../SmellsPlusCPP"
    output_folder = ".../SmellsPlusCP_FRevised"
    
    process_csv_files(input_folder, output_folder)