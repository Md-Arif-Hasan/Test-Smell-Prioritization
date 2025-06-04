


import pandas as pd
import numpy as np

# Read CSV
df = pd.read_csv('.../aggregate_summary.csv')

# Replace blank cells with 0
df = df.replace(r'^\s*$', 0, regex=True)

# Convert columns to numeric, coercing any remaining non-numeric values to 0
numeric_columns = df.select_dtypes(include=[object]).columns
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce').fillna(0)

# Save updated CSV
df.to_csv('.../aggregate_summary_zero_filled.csv', index=False)

print("CSV processed. Zero-filled values saved.")