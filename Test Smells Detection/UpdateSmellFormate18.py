import pandas as pd
import os

def standardize_smell_data(input_path, output_dir):
    # Define exact mapping between input column names and standard names
    smell_mapping = {
        'Assertion Roulette': ['Assertion Roulette'],
        'Conditional Test Logic': ['logic test', 'Conditional logic test'],
        'Constructor Initialization': [],
        'Default Test': [],
        'Duplicate Assertion': ['Duplicate assertion test'],
        'Empty Test': [],
        'Exception Handling': ['Exception handling test'],
        'General Fixture': [],
        'Ignored Test': [],
        'Lack of Cohesion of Test Cases': [],
        'Magic Number Test': ['Magic number test'],
        'Obscure In-Line Setup': ['Obscure in line setup test'],
        'Redundant Assertion': ['Redundant assertion test'],
        'Redundant Print': ['Redundant print test'],
        'Sleepy Test': ['Sleepy test'],
        'Suboptimal Assert': [],
        'Test Maverick': [],
        'Unknown Test': []
    }

    # Process each project folder
    for project_folder in os.listdir(input_path):
        summary_path = os.path.join(input_path, project_folder, 'Summary')
        
        if not os.path.exists(summary_path):
            print(f"No Summary folder found for {project_folder}")
            continue
            
        csv_files = [f for f in os.listdir(summary_path) if f.endswith('.csv')]
        
        for csv_file in csv_files:
            input_csv = os.path.join(summary_path, csv_file)
            df = pd.read_csv(input_csv)
            
            # Create new dataframe
            new_df = pd.DataFrame()
            
            # Copy file path
            file_path_col = [col for col in df.columns if 'path' in col.lower() or 'file' in col.lower()][0]
            new_df['File Path'] = df[file_path_col]
            
            # Map the columns using exact mapping
            for std_smell, input_variations in smell_mapping.items():
                found = False
                for variation in input_variations:
                    if variation in df.columns:
                        new_df[std_smell] = df[variation]
                        found = True
                        break
                if not found:
                    new_df[std_smell] = 0
            
            # Calculate total smells from the mapped columns
            smell_columns = list(smell_mapping.keys())
            new_df['Total Smells'] = new_df[smell_columns].sum(axis=1)
            
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Save standardized file
            output_file = os.path.join(output_dir, f"{project_folder}_standardized.csv")
            new_df.to_csv(output_file, index=False)
            
            # Print sample for verification
            print(f"\nProcessed {project_folder}")
            print("First row values:")
            print(new_df.iloc[0])

# Paths
input_path = '.../SmellsCleanAggregatedData/'
output_dir = '.../TestSmells/18SmellsCleanData'

# Process all projects
print("Starting standardization process...")
standardize_smell_data(input_path, output_dir)
print("\nStandardization complete!")