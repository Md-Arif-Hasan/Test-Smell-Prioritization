import pandas as pd
import os

def check_folder_structure(prod_path, test_path):
    """
    Check if the folder structure is similar enough to indicate a mapping.
    Returns True if the paths have a similar structure.
    """
    prod_parts = prod_path.split('/')
    test_parts = test_path.split('/')
    
    # If one path is significantly longer than the other, they're probably not related
    if abs(len(prod_parts) - len(test_parts)) > 2:
        return False
    
    # Get the base filenames
    prod_file = prod_parts[-1]
    test_file = test_parts[-1]
    
    # Remove 'test_' prefix for comparison
    test_file_clean = test_file.replace('test_', '')
    
    # Base filenames should match (excluding test prefix)
    if prod_file.replace('.py', '') != test_file_clean.replace('.py', ''):
        return False
    
    # At least the last component of the paths should be similar
    # (excluding test/tests directory)
    prod_dir = prod_parts[-2]
    test_dir = test_parts[-2]
    
    if test_dir not in ['test', 'tests', 'unit', 'integration'] and prod_dir != test_dir:
        return False
    
    return True

def map_prod_to_test(prod_df, test_df):
    """Map production files to their corresponding test files using folder structure similarity"""
    matched_pairs = []
    
    for _, prod_row in prod_df.iterrows():
        prod_file = prod_row['File']
        best_match = None
        
        for _, test_row in test_df.iterrows():
            test_file = test_row['File']
            
            if check_folder_structure(prod_file, test_file):
                best_match = test_file
                break  # Stop searching if a match is found
        
        if best_match:
            matched_pairs.append({
                'ProductionFile': prod_file,
                'TestFile': best_match,
                'Prod_Is_Faulty': prod_row['Is_Faulty'],
                'Prod_TotalCommits': prod_row['TotalCommits'],
                'Prod_Insertions': prod_row['Insertions'],
                'Prod_Deletions': prod_row['Deletions'],
                'Prod_FaultCount': prod_row['FaultCount'],
                'Test_Is_Faulty': test_row['Is_Faulty'],
                'Test_TotalCommits': test_row['TotalCommits'],
                'Test_Insertions': test_row['Insertions'],
                'Test_Deletions': test_row['Deletions'],
                'Test_FaultCount': test_row['FaultCount']
            })
    
    return pd.DataFrame(matched_pairs)

def main():
    # Input and output paths
    input_path = "/home/iit/Downloads/Thesis/Data/FaultProneness/All_FaultsProdVsTest/f5-common-python"
    output_path = "/home/iit/Downloads/Thesis/Data/FaultProneness/All_FaultsProdVsTest/"
    
    # Find CSV files
    csv_files = [f for f in os.listdir(input_path) if f.endswith('.csv')]
    
    # Read the CSV files
    prod_df = test_df = None
    for file in csv_files:
        df = pd.read_csv(os.path.join(input_path, file))
        
        if 'test' in file.lower():
            test_df = df
        else:
            prod_df = df
    
    if prod_df is None or test_df is None:
        print("Error: Could not find both production and test CSV files.")
        return
    
    # Create the mapping
    result_df = map_prod_to_test(prod_df, test_df)
    
    # Save to CSV
    output_file = os.path.join(output_path, 'matched_files.csv')
    result_df.to_csv(output_file, index=False)
    print(f"Mapping completed. Output saved to: {output_file}")
    
    # Print matching statistics
    total_prod_files = len(prod_df)
    matched_files = len(result_df)
    print(f"\nMatching Statistics:")
    print(f"Total production files: {total_prod_files}")
    print(f"Files with matching tests: {matched_files}")
    print(f"Coverage percentage: {(matched_files / total_prod_files * 100):.2f}%")

if __name__ == "__main__":
    main()
