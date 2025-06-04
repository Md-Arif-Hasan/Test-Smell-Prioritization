import pandas as pd

# Read the CSV files
test_smells_path = '.../TS.csv'
fault_proneness_path = '.../FP.csv'
output_path = '.../TS_FP/'

# Read CSVs
test_smells_df = pd.read_csv(test_smells_path)
fault_proneness_df = pd.read_csv(fault_proneness_path)

# Merge dataframes on TestFile column
merged_df = pd.merge(
    test_smells_df,
    fault_proneness_df,
    left_on='TestFile',
    right_on='TestFile',
    how='inner'
)

# Reorganize columns to have test smells first, then fault data
smell_columns = [
    'TestFile',
    'ProductionFile',
    'Assertion Roulette',
    'Conditional Test Logic',
    'Constructor Initialization',
    'Duplicate Assertion',
    'Empty Test',
    'Exception Handling',
    'General Fixture',
    'Lack of Cohesion of Test Cases',
    'Magic Number Test',
    'Obscure In-Line Setup',
    'Redundant Assertion',
    'Redundant Print',
    'Sleepy Test',
    'Suboptimal Assert',
    'Test Maverick',
    'Total Smells'
]

fault_columns = [
    'TestIs_Faulty',
    'TestTotalCommits',
    'TestInsertions',
    'TestDeletions',
    'TestFaultCount'
]

# Select and reorder columns
final_columns = smell_columns + fault_columns

# Select only the desired columns that exist in the merged dataframe
existing_columns = [col for col in final_columns if col in merged_df.columns]
final_df = merged_df[existing_columns]

# Save the final merged dataframe
output_file = output_path + 'combined_metrics.csv'
final_df.to_csv(output_file, index=False)

# Print summary statistics
print(f"Original number of rows in test smells file: {len(test_smells_df)}")
print(f"Original number of rows in fault proneness file: {len(fault_proneness_df)}")
print(f"Number of rows in merged file: {len(final_df)}")
print(f"\nColumns in final file:")
for col in final_df.columns:
    print(f"- {col}")