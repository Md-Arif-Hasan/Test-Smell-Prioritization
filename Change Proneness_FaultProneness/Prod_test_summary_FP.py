import pandas as pd

def map_production_test_files(df):
    """
    Maps production files with their associated test files and fault status.
    
    Parameters:
    df (pandas.DataFrame): DataFrame containing file paths and fault status
    
    Returns:
    pandas.DataFrame: Mapped production and test files with fault status
    """
    # Create empty lists to store the mappings
    production_files = []
    production_faulty = []
    test_files = []
    test_faulty = []
    
    # Create dictionaries to store fault status
    production_fault_status = {}
    test_fault_status = {}
    
    # Get the correct column names
    file_path_column = df.columns[0]  # Assuming file path is the first column
    is_faulty_column = [col for col in df.columns if 'faulty' in col.lower()][0]  # Find column with 'faulty' in name
    
    # Process each row in the DataFrame
    for _, row in df.iterrows():
        file_path = row[file_path_column]
        is_faulty = row[is_faulty_column]
        
        # Check if file is a test file
        if 'test' in str(file_path).lower():
            test_fault_status[file_path] = is_faulty
        else:
            production_fault_status[file_path] = is_faulty
    
    # Map production files to test files
    for prod_file in production_fault_status.keys():
        base_name = str(prod_file).split('/')[-1].replace('.py', '')
        
        # Look for associated test files
        found_test = False
        for test_file in test_fault_status.keys():
            if base_name.lower() in str(test_file).lower():
                production_files.append(prod_file)
                production_faulty.append(production_fault_status[prod_file])
                test_files.append(test_file)
                test_faulty.append(test_fault_status[test_file])
                found_test = True
                break
        
        # If no test file found, still include the production file
        if not found_test:
            production_files.append(prod_file)
            production_faulty.append(production_fault_status[prod_file])
            test_files.append(None)
            test_faulty.append(None)
    
    # Create the mapped DataFrame
    mapped_df = pd.DataFrame({
        'ProductionFile': production_files,
        'IsFaultyProduction': production_faulty,
        'AssociatedTestFile': test_files,
        'IsFaultyTest': test_faulty
    })
    
    return mapped_df

# File paths
input_file = r'.../Fault_proneness_combined.csv'
output_file = r'.../Fault_proneness_Prod_test.csv'

try:
    # Read the CSV file
    print(f"Reading input file: {input_file}")
    df = pd.read_csv(input_file)
    
    # Print column names for debugging
    print("\nAvailable columns in the CSV file:")
    print(df.columns.tolist())
    
    # Display first few rows for debugging
    print("\nFirst few rows of the data:")
    print(df.head())
    
    # Create the mapping
    print("\nProcessing file mappings...")
    mapped_df = map_production_test_files(df)
    
    # Save the result
    print(f"\nSaving output to: {output_file}")
    mapped_df.to_csv(output_file, index=False)
    
    # Display summary statistics
    print("\nSummary:")
    print(f"Total production files mapped: {len(mapped_df)}")
    print(f"Production files with associated tests: {mapped_df['AssociatedTestFile'].notna().sum()}")
    print(f"Production files without tests: {mapped_df['AssociatedTestFile'].isna().sum()}")
    
except Exception as e:
    print(f"An error occurred: {str(e)}")