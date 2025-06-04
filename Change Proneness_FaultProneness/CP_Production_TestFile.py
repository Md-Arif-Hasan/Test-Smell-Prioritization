import pandas as pd
import os
import re

def is_test_file(filename):
    """Determine if a file is a test file"""
    test_patterns = [
        r'test_',           # test_ at start
        r'_test\.',         # _test. in middle
        r'/test/',          # /test/ in path
        r'/tests/',         # /tests/ in path
        r'_tests\.',        # _tests. in middle
        r'tests_'           # tests_ at start
    ]
    return any(re.search(pattern, filename, re.IGNORECASE) for pattern in test_patterns)

def get_base_name(filename):
    """Extract base name for matching test and production files"""
    # Remove directory path
    base = os.path.basename(filename)
    
    # Remove test-related prefixes and suffixes
    base = re.sub(r'^test_', '', base, flags=re.IGNORECASE)
    base = re.sub(r'^tests_', '', base, flags=re.IGNORECASE)
    base = re.sub(r'_test\.', '.', base, flags=re.IGNORECASE)
    base = re.sub(r'_tests\.', '.', base, flags=re.IGNORECASE)
    
    return base

def find_matching_files(files):
    """Find matching test and production file pairs"""
    file_pairs = {}
    
    for file1 in files:
        base1 = get_base_name(file1)
        for file2 in files:
            base2 = get_base_name(file2)
            
            # Check if one is a test file and other is production
            if base1 == base2:
                if is_test_file(file1) and not is_test_file(file2):
                    file_pairs[file2] = file1
                elif is_test_file(file2) and not is_test_file(file1):
                    file_pairs[file1] = file2
    
    return file_pairs

def transform_csv(input_path, output_path):
    """Transform CSV data to group test and production files together with their metrics."""
    # Read input CSV
    data = pd.read_csv(input_path)
    
    # Get all unique filenames
    all_files = data['Filename'].unique()
    
    # Find matching file pairs
    file_pairs = find_matching_files(all_files)
    
    # Create empty lists to store paired data
    paired_data = []
    processed_files = set()
    
    # Process production files and their matching test files
    for prod_file in data['Filename'].unique():
        if prod_file in processed_files or is_test_file(prod_file):
            continue
            
        # Get production file metrics
        prod_row = data[data['Filename'] == prod_file].iloc[0]
        prod_metrics = prod_row[['Changes', 'TotalCommits', 'Insertions', 'Deletions']].values
        
        # Find matching test file
        test_file = file_pairs.get(prod_file, 'N/A')
        
        # Get test file metrics if it exists
        test_metrics = [0, 0, 0, 0]  # Default values if test file doesn't exist
        if test_file != 'N/A':
            test_row = data[data['Filename'] == test_file]
            if not test_row.empty:
                test_metrics = test_row.iloc[0][['Changes', 'TotalCommits', 'Insertions', 'Deletions']].values
                processed_files.add(test_file)
        
        # Add the paired data
        paired_data.append({
            'ProductionFile': prod_file,
            'TestFile': test_file,
            'Prod_Changes': prod_metrics[0],
            'Prod_TotalCommits': prod_metrics[1],
            'Prod_Insertions': prod_metrics[2],
            'Prod_Deletions': prod_metrics[3],
            'Test_Changes': test_metrics[0],
            'Test_TotalCommits': test_metrics[1],
            'Test_Insertions': test_metrics[2],
            'Test_Deletions': test_metrics[3]
        })
        
        processed_files.add(prod_file)
    
    # Convert to DataFrame
    result_df = pd.DataFrame(paired_data)
    
    # Save transformed CSV
    result_df.to_csv(output_path, index=False)
    print(f"Transformed CSV saved to: {output_path}")

# Process all CSVs in the input directory
input_dir = "/home/siam/Desktop/volume1/MS_Papers_Arif/Data/ChangeProneness_analysis_results"
output_dir = "/home/siam/Desktop/volume1/MS_Papers_Arif/Data/CP_Summary"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Process each CSV file
for filename in os.listdir(input_dir):
    if filename.endswith('_analysis.csv'):
        input_path = os.path.join(input_dir, filename)
        # Create output filename
        output_filename = filename.replace('_analysis.csv', '_transformed.csv')
        output_path = os.path.join(output_dir, output_filename)
        
        try:
            transform_csv(input_path, output_path)
        except Exception as e:
            print(f"Error processing {filename}: {e}")