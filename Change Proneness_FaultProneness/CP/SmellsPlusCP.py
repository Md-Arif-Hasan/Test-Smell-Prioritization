import os
import pandas as pd

def extract_filename(path):
    """Safely extract filename."""
    if pd.isna(path):
        return None
    return os.path.basename(str(path))

def merge_project_csvs(cp_dir, smell_dir, output_dir):
    # Create output directory if not exists
    os.makedirs(output_dir, exist_ok=True)

    # Logging for tracking
    merge_log = []

    # Iterate through CP transformed CSV files
    for cp_filename in os.listdir(cp_dir):
        if cp_filename.endswith('_transformed.csv'):
            # Extract project name
            project_name = cp_filename.replace('_transformed.csv', '')
            
            # Construct full paths
            cp_file = os.path.join(cp_dir, cp_filename)
            smell_dir_path = os.path.join(smell_dir, f"{project_name}_csv/Summary")
            
            # Check if smell directory exists
            if not os.path.exists(smell_dir_path):
                print(f"Skipping {project_name}: Smell directory not found")
                continue

            # Iterate through smell summary files in the project directory
            for smell_filename in os.listdir(smell_dir_path):
                if smell_filename == 'smell_summary.csv':
                    smell_file = os.path.join(smell_dir_path, smell_filename)
                    output_file = os.path.join(output_dir, f"{project_name}.csv")

                    # Read CSV files
                    cp_df = pd.read_csv(cp_file)
                    smell_df = pd.read_csv(smell_file)

                    # Extract filenames for test files
                    cp_df['test_filename'] = cp_df['TestFile'].apply(extract_filename)
                    smell_df['test_filename'] = smell_df['File Path'].apply(extract_filename)

                    # Merge on test filenames
                    merged_df = cp_df.merge(smell_df, on='test_filename', how='inner')
                    merged_df = merged_df.dropna(subset=['test_filename'])

                    # Save merged dataframe
                    merged_df.to_csv(output_file, index=False)
                    
                    # Log merge details
                    merge_log.append({
                        'Project': project_name,
                        'Total Merged Rows': len(merged_df)
                    })
                    print(f"{project_name}: Merged {len(merged_df)} rows")

    # Optional: Create a log file
    log_df = pd.DataFrame(merge_log)
    log_df.to_csv(os.path.join(output_dir, 'merge_log.csv'), index=False)

# Directories
cp_dir = ".../CP/CP_Summary"
smell_dir = "...TestSmells/SmellsCleanAggregatedData"
output_dir = ".../SmellsPlusCPP"

# Merge files in bulk
merge_project_csvs(cp_dir, smell_dir, output_dir)