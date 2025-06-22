import pandas as pd
import os
import glob

def create_mapped_csv(project_folder, output_folder):
    """Create a CSV mapping production files to test files for a given project folder."""
    project_name = os.path.basename(project_folder)
    prod_file = os.path.join(project_folder, f"{project_name}_production.csv")
    test_file = os.path.join(project_folder, f"{project_name}_test.csv")

    # Check if both files exist
    if not os.path.exists(prod_file) or not os.path.exists(test_file):
        print(f"Skipping {project_name} (Missing CSV files).")
        return

    # Load CSVs
    df_prod = pd.read_csv(prod_file)
    df_test = pd.read_csv(test_file)

    if "File" not in df_prod.columns or "File" not in df_test.columns:
        print(f"Skipping {project_name} (Missing 'File' column).")
        return

    # Create mapping (Cartesian product)
    df_prod["key"] = 1
    df_test["key"] = 1
    mapped_df = df_prod.merge(df_test, on="key", suffixes=("_Prod", "_Test")).drop(columns=["key"])

    # Output path
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"{project_name}_mapped.csv")

    # Save to CSV
    mapped_df.to_csv(output_file, index=False)

    print(f"Created mapped CSV for {project_name}: {output_file}")

def process_all_projects(input_folder, output_folder):
    """Iterate through all projects in the input folder and generate mapped CSVs."""
    project_folders = [f for f in glob.glob(os.path.join(input_folder, "*")) if os.path.isdir(f)]

    if not project_folders:
        print(f"No project folders found in {input_folder}")
        return

    print(f"Found {len(project_folders)} projects. Processing...")

    for project_folder in project_folders:
        create_mapped_csv(project_folder, output_folder)

# File paths
input_folder = ".../Fault_proneness/All_FaultsProdVsTest"
output_folder = ".../Fault_proneness/All_Faults_Mapped"

# Process all projects
process_all_projects(input_folder, output_folder)





# EI CODE UPDATE KORE MAPPING KORA LAGBE