
import pandas as pd
import os

# Define input and output paths
input_dir = '.../TS_FP'
output_file = '.../tsfp.csv'

# Construct full file paths
test_smells_path = os.path.join(input_dir, 'TS.csv')
fault_proneness_path = os.path.join(input_dir, 'FP.csv')

# Read CSVs
test_smells_df = pd.read_csv(test_smells_path)
fault_proneness_df = pd.read_csv(fault_proneness_path)

# Remove duplicates from both dataframes based on TestFile
test_smells_df = test_smells_df.drop_duplicates(subset=['TestFile'])
fault_proneness_df = fault_proneness_df.drop_duplicates(subset=['TestFile'])

# Print column names and counts before merge
print("Columns in Test Smells file:")
print(test_smells_df.columns.tolist())
print(f"Unique TestFiles in Test Smells: {len(test_smells_df)}")
print("\nColumns in Fault Proneness file:")
print(fault_proneness_df.columns.tolist())
print(f"Unique TestFiles in Fault Proneness: {len(fault_proneness_df)}")

# Merge dataframes on TestFile column
merged_df = pd.merge(
    fault_proneness_df[['ProductionFile', 'TestFile', 'Prod_Is_Faulty',
                        'Prod_TotalFaultyCommit', 'Prod_TotalCommits',
                        'Prod_FaultyInsertions', 'Prod_FaultyDeletions',
                        'Test_Is_Faulty', 'Test_TotalFaultyCommit',
                        'Test_TotalCommits', 'Test_FaultyInsertions',
                        'Test_FaultyDeletions']],
    test_smells_df[['TestFile', 'Assertion Roulette', 'Conditional Test Logic',
                    'Constructor Initialization', 'Duplicate Assertion',
                    'Empty Test', 'Exception Handling', 'General Fixture',
                    'Lack of Cohesion of Test Cases', 'Magic Number Test',
                    'Obscure In-Line Setup', 'Redundant Assertion ', 'Redundant Print', 
                    'Sleepy Test', 'Suboptimal Assert', 'Test Maverick', 
                    'Total Smells']],
    on='TestFile',
    how='inner'
)

# Define the exact column order needed
final_columns = [
    'ProductionFile', 'TestFile', 'Prod_Is_Faulty', 'Prod_TotalFaultyCommit',
    'Prod_TotalCommits', 'Prod_FaultyInsertions', 'Prod_FaultyDeletions',
    'Test_Is_Faulty', 'Test_TotalFaultyCommit', 'Test_TotalCommits',
    'Test_FaultyInsertions', 'Test_FaultyDeletions', 'Assertion Roulette',
    'Conditional Test Logic', 'Constructor Initialization', 'Duplicate Assertion',
    'Empty Test', 'Exception Handling', 'General Fixture',
    'Lack of Cohesion of Test Cases', 'Magic Number Test', 'Obscure In-Line Setup',
    'Redundant Assertion ', 'Redundant Print', 'Sleepy Test', 'Suboptimal Assert', 
    'Test Maverick', 'Total Smells'
]

# Verify all columns exist in merged_df
print("\nColumns in merged dataframe:")
print(merged_df.columns.tolist())

# Select the columns in the desired order
final_df = merged_df[final_columns]

# Verify no duplicates in final dataset
final_df = final_df.drop_duplicates(subset=['TestFile'])

# Create output directory if it doesn't exist
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Save the final merged dataframe
final_df.to_csv(output_file, index=False)

# Print summary statistics
print(f"\nOriginal number of rows in test smells file: {len(test_smells_df)}")
print(f"Original number of rows in fault proneness file: {len(fault_proneness_df)}")
print(f"Number of rows in merged file: {len(final_df)}")
print(f"Number of unique TestFiles in final file: {final_df['TestFile'].nunique()}")
print(f"\nOutput file saved to: {output_file}")