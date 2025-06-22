import pandas as pd
import os

def find_result_csvs(root_dir):
    """Find all CSV files containing 'result' in their names in the given directory and its subdirectories"""
    result_files = []
    
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.csv') and 'result' in file.lower():
                full_path = os.path.join(root, file)
                result_files.append(full_path)
                print(f"Found result file: {full_path}")
    
    return result_files

def combine_csv_files(file_paths, output_path):
    """Combine multiple CSV files into a single CSV file"""
    # List to store all dataframes
    dfs = []
    
    # Read each CSV file
    for file_path in file_paths:
        try:
            df = pd.read_csv(file_path)
            # Add a column for the source project
            project_name = os.path.basename(os.path.dirname(file_path))
            df['Project'] = project_name
            dfs.append(df)
            print(f"Successfully read: {file_path}")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    if not dfs:
        print("No CSV files were successfully read!")
        return
    
    # Combine all dataframes
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Save the combined dataframe
    output_file = os.path.join(output_path, 'combined_results.csv')
    combined_df.to_csv(output_file, index=False)
    print(f"\nCombined CSV saved to: {output_file}")
    print(f"Total number of rows: {len(combined_df)}")
    print(f"Total number of files combined: {len(dfs)}")

def main():
    # Input and output paths
    input_dir = ".../All_FaultsProdVsTest"
    output_dir = ".../TS_CP_FP"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all result CSV files
    print("Searching for result CSV files...")
    result_files = find_result_csvs(input_dir)
    
    if not result_files:
        print("No result CSV files found!")
        return
    
    print(f"\nFound {len(result_files)} result CSV files")
    
    # Combine the CSV files
    print("\nCombining CSV files...")
    combine_csv_files(result_files, output_dir)

if __name__ == "__main__":
    main()