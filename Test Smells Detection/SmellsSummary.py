

import pandas as pd
import os

def clean_file_path(path):
    """Remove the repetitive prefix from file paths"""
    prefix = "file://$PROJECT_DIR$/"
    if isinstance(path, str) and path.startswith(prefix):
        return path[len(prefix):]
    return path

def generate_smell_summary(input_csv, output_dir):
    # Read the CSV file
    df = pd.read_csv(input_csv)
    
    # Identify columns
    file_path_col = [col for col in df.columns if 'path' in col.lower() or 'file' in col.lower()][0]
    smell_name_col = [col for col in df.columns if 'smell' in col.lower()][0]
    
    # Clean file paths
    df[file_path_col] = df[file_path_col].apply(clean_file_path)
    
    # Group by unique file path and smell name, and count occurrences
    smell_summary = df.groupby([file_path_col, smell_name_col]).size().reset_index(name='smell_count')
    
    # Pivot the table 
    pivot_summary = smell_summary.pivot_table(
        index=file_path_col, 
        columns=smell_name_col, 
        values='smell_count', 
        fill_value=0
    ).reset_index()
    
    # Sort rows by total smells
    pivot_summary['total_smells'] = pivot_summary.iloc[:, 1:].sum(axis=1)
    pivot_summary = pivot_summary.sort_values('total_smells', ascending=False)
    
    # Save to CSV
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'smell_summary.csv')
    pivot_summary.to_csv(output_path, index=False)
    
    print(f"Summary for {input_csv}: {len(pivot_summary)} unique file paths")
    return pivot_summary

def process_all_projects(base_dir):
    print("Processing all projects in:", base_dir)
    print("-" * 50)
    
    for project_folder in os.listdir(base_dir):
        project_path = os.path.join(base_dir, project_folder)
        
        # Skip if not a directory
        if not os.path.isdir(project_path):
            continue
        
        # Find CSV files
        csv_files = [f for f in os.listdir(project_path) if f.endswith('_aggregated.csv')]
        
        if csv_files:
            print(f"\nProcessing project: {project_folder}")
            
            for csv_file in csv_files:
                input_csv = os.path.join(project_path, csv_file)
                output_dir = os.path.join(project_path, 'Summary')
                
                generate_smell_summary(input_csv, output_dir)
        else:
            print(f"\nNo aggregated CSV files found in: {project_folder}")

# Base directory
base_dir = '.../TestSmells/SmellsCleanAggregatedData'

# Process all projects
process_all_projects(base_dir)