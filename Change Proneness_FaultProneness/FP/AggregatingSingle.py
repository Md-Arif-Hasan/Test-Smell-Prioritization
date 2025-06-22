=

import pandas as pd

def process_raw_data(file_path):
    """
    Process the space-separated file into a structured DataFrame.
    """
    # Read the file content
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Split the content into pairs of file path and faulty status
    items = content.strip().split()
    
    # Create lists for paths and status
    paths = []
    status = []
    
    # Process items in pairs
    for i in range(0, len(items), 2):
        if i + 1 < len(items):
            paths.append(items[i])
            status.append(int(items[i + 1]))
    
    # Create DataFrame
    return pd.DataFrame({'file_path': paths, 'is_faulty': status})

def map_production_test_files(df):
    """
    Maps production files with their associated test files.
    """
    # Separate test and production files
    test_files = df[df['file_path'].str.contains('/test', case=False)]
    prod_files = df[~df['file_path'].str.contains('/test', case=False)]
    
    # Create lists for mapped data
    production_files = []
    production_faulty = []
    test_files_mapped = []
    test_faulty = []
    
    # For each production file, find matching test file
    for _, prod_row in prod_files.iterrows():
        prod_file = prod_row['file_path']
        base_name = prod_file.split('/')[-1].replace('.py', '')
        
        # Look for matching test file
        matching_tests = test_files[test_files['file_path'].str.contains(base_name, case=False)]
        
        if not matching_tests.empty:
            # Add all matching test files
            for _, test_row in matching_tests.iterrows():
                production_files.append(prod_file)
                production_faulty.append(prod_row['is_faulty'])
                test_files_mapped.append(test_row['file_path'])
                test_faulty.append(test_row['is_faulty'])
        else:
            # Add production file with no matching test
            production_files.append(prod_file)
            production_faulty.append(prod_row['is_faulty'])
            test_files_mapped.append(None)
            test_faulty.append(None)
    
    # Create result DataFrame
    result_df = pd.DataFrame({
        'ProductionFile': production_files,
        'IsFaultyProduction': production_faulty,
        'AssociatedTestFile': test_files_mapped,
        'IsFaultyTest': test_faulty
    })
    
    return result_df

# File paths
input_file = r'.../SM_CP_FP/Fault_proneness_combined.csv'
output_file = r'.../SM_CP_FP/Fault_proneness_Prod_test.csv'

try:
    # Process the raw data
    print(f"Reading input file: {input_file}")
    df = process_raw_data(input_file)
    
    # Create the mapping
    print("Processing file mappings...")
    mapped_df = map_production_test_files(df)
    
    # Save the result
    print(f"Saving output to: {output_file}")
    mapped_df.to_csv(output_file, index=False)
    
    # Display summary statistics
    print("\nSummary:")
    print(f"Total production files mapped: {len(mapped_df)}")
    print(f"Production files with associated tests: {mapped_df['AssociatedTestFile'].notna().sum()}")
    print(f"Production files without tests: {mapped_df['AssociatedTestFile'].isna().sum()}")
    
    # Display first few mappings
    print("\nFirst few mappings:")
    print(mapped_df.head())
    
except Exception as e:
    print(f"An error occurred: {str(e)}")
    raise