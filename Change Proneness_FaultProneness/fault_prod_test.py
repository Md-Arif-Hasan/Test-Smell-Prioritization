# import pandas as pd
# import os
# import re

# def get_module_path(filepath):
#     """Get the module path excluding the filename"""
#     return os.path.dirname(filepath)

# def get_file_base_name(filepath):
#     """Get the base filename without extension and test indicators"""
#     filename = os.path.basename(filepath)
#     base_name = re.sub(r'test_|_test|\.py$', '', filename, flags=re.IGNORECASE)
#     return base_name.lower()

# def calculate_path_similarity(prod_path, test_path):
#     """Calculate similarity score between production and test paths"""
#     prod_parts = prod_path.split('/')
#     test_parts = test_path.split('/')
    
#     # Extract the relevant parts of the path (ignoring test/new_tests prefix)
#     if 'test/new_tests' in test_path:
#         test_parts = test_parts[2:]  # Skip 'test/new_tests'
    
#     # Score based on directory structure
#     score = 0
#     if 'examples/client' in prod_path:
#         score += 3  # Higher priority for client examples
#     elif 'examples/deprecated' in prod_path:
#         score += 1  # Lower priority for deprecated examples
#     elif 'doc/examples' in prod_path:
#         score += 2  # Medium priority for doc examples
    
#     # Additional score for matching directory names
#     common_dirs = set(prod_parts) & set(test_parts)
#     score += len(common_dirs)
    
#     return score

# def find_matching_files(data):
#     """Find matching production and test file pairs with precise mapping"""
#     # Create dictionaries to store files and their attributes
#     prod_files = {}
#     test_files = {}
    
#     # Process each file
#     for _, row in data.iterrows():
#         filepath = row['File'].split()[-1]
#         is_test = 'test/new_tests' in filepath or filepath.startswith('test/')
        
#         if is_test:
#             test_files[filepath] = {
#                 'base_name': get_file_base_name(filepath),
#                 'module_path': get_module_path(filepath),
#                 'is_faulty': row['Is_Faulty']
#             }
#         else:
#             prod_files[filepath] = {
#                 'base_name': get_file_base_name(filepath),
#                 'module_path': get_module_path(filepath),
#                 'is_faulty': row['Is_Faulty']
#             }
    
#     # Find matches with improved precision
#     matched_pairs = []
#     used_test_files = set()
    
#     for prod_path, prod_info in prod_files.items():
#         best_match = None
#         best_score = -1
        
#         for test_path, test_info in test_files.items():
#             if test_path in used_test_files:
#                 continue
                
#             if prod_info['base_name'] == test_info['base_name']:
#                 score = calculate_path_similarity(prod_path, test_path)
                
#                 if score > best_score:
#                     best_score = score
#                     best_match = test_path
        
#         if best_match and best_score >= 1:  # Ensure minimum similarity
#             used_test_files.add(best_match)
#             matched_pairs.append({
#                 'Production_file': prod_path,
#                 'isFaulty_prod': prod_files[prod_path]['is_faulty'],
#                 'Test_file': best_match,
#                 'isFaulty_test': test_files[best_match]['is_faulty']
#             })
    
#     return matched_pairs

# # File paths
# input_file = r'/home/iit/Downloads/Thesis/Data/SM_CP_FP/Fault_proneness/aerospike-client-python_fault_proneness.csv'
# output_file = r'/home/iit/Downloads/Thesis/Data/SM_CP_FP/Fault_proneness/aerospike-client-python_mapped.csv'

# # Read input CSV
# print(f"Reading input file: {input_file}")
# data = pd.read_csv(input_file)

# print("\nProcessing file pairs...")
# paired_data = find_matching_files(data)

# # Convert to DataFrame
# result_df = pd.DataFrame(paired_data)

# # Sort by Production_file for better readability
# result_df = result_df.sort_values('Production_file')

# # Save transformed CSV
# print(f"\nSaving output to: {output_file}")
# result_df.to_csv(output_file, index=False)

# # Print statistics
# print("\nMapping Statistics:")
# print(f"Total pairs found: {len(result_df)}")
# print("\nSample of mapped pairs (first 5):")
# pd.set_option('display.max_colwidth', None)
# print(result_df.head().to_string())

# # Print potential duplicates
# print("\nChecking for duplicate test file mappings...")
# test_file_counts = result_df['Test_file'].value_counts()
# duplicates = test_file_counts[test_file_counts > 1]
# if not duplicates.empty:
#     print("\nWarning: Found test files mapped to multiple production files:")
#     for test_file, count in duplicates.items():
#         print(f"\n{test_file} is mapped {count} times to:")
#         print(result_df[result_df['Test_file'] == test_file]['Production_file'].tolist())
# else:
#     print("\nNo duplicate mappings found.")





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
