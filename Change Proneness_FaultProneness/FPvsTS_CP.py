import pandas as pd
import os

def combine_test_metrics(csv1_path, csv2_path, output_path):
    """
    Combine two CSVs based on TestFile mapping and create a new combined CSV,
    ensuring one-to-one mapping between test files
    """
    # Read both CSVs
    df1 = pd.read_csv(csv1_path)
    df2 = pd.read_csv(csv2_path)
    
    # Check for duplicate TestFiles in both dataframes
    duplicates_df1 = df1[df1['TestFile'].duplicated(keep=False)]
    duplicates_df2 = df2[df2['TestFile'].duplicated(keep=False)]
    
    # Remove duplicates by keeping the first occurrence
    df1_unique = df1.drop_duplicates(subset=['TestFile'], keep='first')
    df2_unique = df2.drop_duplicates(subset=['TestFile'], keep='first')
    
    # Create the merged dataframe based on TestFile
    merged_df = pd.merge(
        df1_unique,
        df2_unique,
        on='TestFile',
        how='inner',  # Changed to inner join to keep only matching records
        suffixes=('_1', '_2')
    )
    
    # Define the desired column order
    columns_order = [
        'ProductionFile', 'TestFile',
        'Prod_Changes', 'Prod_TotalCommits', 'Prod_Insertions', 'Prod_Deletions',
        'Test_Changes', 'Test_TotalCommits', 'Test_Insertions', 'Test_Deletions',
        'test_filename', 'File Path',
        'Assertion Roulette', 'Conditional Test Logic', 'Constructor Initialization',
        'Duplicate Assertion', 'Empty Test', 'Exception Handling', 'General Fixture',
        'Lack of Cohesion of Test Cases', 'Magic Number Test', 'Obscure In-Line Setup',
        'Redundant Assertion', 'Redundant Print', 'Sleepy Test', 'Suboptimal Assert',
        'Test Maverick', 'Total Smells',
        'ProdIs_Faulty', 'ProdTotalCommits', 'ProdInsertions', 'ProdDeletions',
        'ProdFaultCount', 'TestIs_Faulty', 'TestTotalCommits', 'TestInsertions',
        'TestDeletions', 'TestFaultCount', 'Project'
    ]
    
    # Ensure all columns exist, create if missing with NaN values
    for col in columns_order:
        if col not in merged_df.columns:
            merged_df[col] = pd.NA
    
    # Select and order columns
    result_df = merged_df[columns_order]
    
    # Save the combined DataFrame
    result_df.to_csv(output_path, index=False)
    
    # Print detailed statistics
    print(f"\nDetailed Combination Statistics:")
    print(f"Records in first CSV (TS_CP.csv): {len(df1)}")
    print(f"Unique test files in first CSV: {len(df1_unique)}")
    print(f"Duplicate test files in first CSV: {len(duplicates_df1)}")
    print(f"\nRecords in second CSV (combined_results.csv): {len(df2)}")
    print(f"Unique test files in second CSV: {len(df2_unique)}")
    print(f"Duplicate test files in second CSV: {len(duplicates_df2)}")
    print(f"\nFinal matched records (1-to-1 mapping): {len(result_df)}")
    print(f"\nOutput saved to: {output_path}")
    
    # Print some example duplicates if they exist
    if len(duplicates_df1) > 0:
        print("\nExample duplicate test files in first CSV:")
        print(duplicates_df1['TestFile'].head())
    if len(duplicates_df2) > 0:
        print("\nExample duplicate test files in second CSV:")
        print(duplicates_df2['TestFile'].head())

def main():
    # Your specific input and output paths
    csv1_path = ".../TS_CP.csv"
    csv2_path = ".../combined_results.csv"
    output_path = ".../final.csv"
    
    try:
        combine_test_metrics(csv1_path, csv2_path, output_path)
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        print("Please check if the input files exist and have the correct format")

if __name__ == "__main__":
    main()