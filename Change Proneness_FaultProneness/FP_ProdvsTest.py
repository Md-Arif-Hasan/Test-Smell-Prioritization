


# import pandas as pd
# import os
# import glob

# def is_test_file(file_path: str) -> bool:
#     """Determine if a file is a test file based on common naming conventions."""
#     test_patterns = [
#         r"(^|/)tests?(/|$)",  # Matches folders named 'test' or 'tests'
#         r"(^|/)test_.*\.py$",  # Matches 'test_*.py'
#         r"(^|/).*_test\.py$",  # Matches '*_test.py'
#         r"(^|/)unittests?(/|$)",  # Matches 'unittest' or 'unittests' folders
#         r"(^|/)specs?(/|$)",  # Matches 'spec' or 'specs' folders
#     ]
    
#     return any(pd.Series(file_path).str.contains(pattern, regex=True, na=False).iloc[0] for pattern in test_patterns)

# def split_csv_by_file_type(input_file, output_folder):
#     """Split a single CSV file into production and test files, and store them in a structured folder."""
#     df = pd.read_csv(input_file)

#     if "File" not in df.columns:
#         print(f"Skipping {input_file} (No 'File' column found).")
#         return

#     # Apply test file detection logic
#     df["Is_Test"] = df["File"].apply(is_test_file)
    
#     # Separate into production and test files
#     prod_files = df[~df["Is_Test"]].drop(columns=["Is_Test"])
#     test_files = df[df["Is_Test"]].drop(columns=["Is_Test"])

#     # Extract base name without the .csv extension
#     base_name = os.path.basename(input_file).replace("_fault_proneness.csv", "").replace(".csv", "")

#     # Create a subdirectory for this file
#     subfolder_path = os.path.join(output_folder, base_name)
#     os.makedirs(subfolder_path, exist_ok=True)

#     # Define output file paths
#     prod_output_file = os.path.join(subfolder_path, f"{base_name}_production.csv")
#     test_output_file = os.path.join(subfolder_path, f"{base_name}_test.csv")

#     # Save the files
#     prod_files.to_csv(prod_output_file, index=False)
#     test_files.to_csv(test_output_file, index=False)

#     # Print summary
#     print(f"Processed: {input_file}")
#     print(f"  - Production files: {len(prod_files)} -> {prod_output_file}")
#     print(f"  - Test files: {len(test_files)} -> {test_output_file}")

# def process_all_csv_files(input_folder, output_folder):
#     """Process all CSV files in the input folder."""
#     csv_files = glob.glob(os.path.join(input_folder, "*.csv"))

#     if not csv_files:
#         print(f"No CSV files found in {input_folder}")
#         return

#     print(f"Found {len(csv_files)} CSV files in {input_folder}. Processing...")

#     for csv_file in csv_files:
#         split_csv_by_file_type(csv_file, output_folder)

# # File paths
# input_folder = "/home/siam/Desktop/volume1/MS_Papers_Arif/Data/Fault_proneness/All_Faults"
# output_folder = "/home/siam/Desktop/volume1/MS_Papers_Arif/Data/Fault_proneness/All_FaultsProdVsTest"

# # Process all CSV files in the folder
# process_all_csv_files(input_folder, output_folder)



import pandas as pd
import os
import glob

def is_test_file(file_path: str) -> bool:
    """Determine if a file is a test file based on common naming conventions."""
    test_patterns = [
        r"(^|/)tests?(/|$)",  # Matches folders named 'test' or 'tests'
        r"(^|/)test_.*\.py$",  # Matches 'test_*.py'
        r"(^|/).*_test\.py$",  # Matches '*_test.py'
        r"(^|/)unittests?(/|$)",  # Matches 'unittest' or 'unittests' folders
        r"(^|/)specs?(/|$)",  # Matches 'spec' or 'specs' folders
    ]
    
    return any(pd.Series(file_path).str.contains(pattern, regex=True, na=False).iloc[0] for pattern in test_patterns)

def split_csv_by_file_type(input_file, output_folder):
    """Split a single CSV file into production and test files, and store them in a structured folder."""
    df = pd.read_csv(input_file)

    if "File" not in df.columns:
        print(f"Skipping {input_file} (No 'File' column found).")
        return

    # Apply test file detection logic
    df["Is_Test"] = df["File"].apply(is_test_file)
    
    # Separate into production and test files
    prod_files = df[~df["Is_Test"]].drop(columns=["Is_Test", "Repository"])  # Drop "Repository"
    test_files = df[df["Is_Test"]].drop(columns=["Is_Test", "Repository"])  # Drop "Repository"

    # Extract base name without the .csv extension
    base_name = os.path.basename(input_file).replace("_fault_proneness.csv", "").replace(".csv", "")

    # Create a subdirectory for this file
    subfolder_path = os.path.join(output_folder, base_name)
    os.makedirs(subfolder_path, exist_ok=True)

    # Define output file paths
    prod_output_file = os.path.join(subfolder_path, f"{base_name}_production.csv")
    test_output_file = os.path.join(subfolder_path, f"{base_name}_test.csv")

    # Save the files
    prod_files.to_csv(prod_output_file, index=False)
    test_files.to_csv(test_output_file, index=False)

    # Print summary
    print(f"Processed: {input_file}")
    print(f"  - Production files: {len(prod_files)} -> {prod_output_file}")
    print(f"  - Test files: {len(test_files)} -> {test_output_file}")

def process_all_csv_files(input_folder, output_folder):
    """Process all CSV files in the input folder."""
    csv_files = glob.glob(os.path.join(input_folder, "*.csv"))

    if not csv_files:
        print(f"No CSV files found in {input_folder}")
        return

    print(f"Found {len(csv_files)} CSV files in {input_folder}. Processing...")

    for csv_file in csv_files:
        split_csv_by_file_type(csv_file, output_folder)

# File paths
input_folder = "/home/siam/Desktop/volume1/MS_Papers_Arif/Data/Fault_proneness/All_Faults"
output_folder = "/home/siam/Desktop/volume1/MS_Papers_Arif/Data/Fault_proneness/All_FaultsProdVsTest"

# Process all CSV files in the folder
process_all_csv_files(input_folder, output_folder)
