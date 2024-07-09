import pandas as pd
import numpy as np
import os

# Load the data
file_path = 'data/GameSessions.csv'  # Update with the actual file path
df = pd.read_csv(file_path)

# Remove the Email column
df = df.drop(columns=['Email'])

# Remove games where they didn't even start and drop the column
df = df[df['DidGameStart'] != False]
df = df.drop(columns=['DidGameStart'])

# Remove games where they are not finished and drop the column
df = df[df['IsGameEnded'] != False]
df = df.drop(columns=['IsGameEnded'])

# Remove games where they didn't stop and drop the column
df = df[df['DidGameStop'] != False]
df = df.drop(columns=['DidGameStop'])

# Remove redundant columns
redundant_columns = ['DispenserId', 'ToyId', 'UserId']
df = df.drop(columns=redundant_columns)

# Convert relevant columns to numeric type if needed
numeric_columns = ['GameTime', 'NumPrompts', 'NumNegPrompts', 'SuccessRate']
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Calculate additional metrics and add them as new columns in the existing DataFrame
# Ensure to handle division by zero or NaN values
df['AverageResponseTime'] = df.apply(lambda row: row['GameTime'] / (row['NumPrompts'] + row['NumNegPrompts']) if (row['NumPrompts'] + row['NumNegPrompts']) != 0 else np.nan, axis=1)
df['PromptEffectiveness'] = df.apply(lambda row: row['SuccessRate'] / (row['NumPrompts'] + row['NumNegPrompts']) if (row['NumPrompts'] + row['NumNegPrompts']) != 0 else np.nan, axis=1)
df['SuccessRatePerSession'] = df['SuccessRate']

# ------------------- filtered csv save ----------------------------------
directory, file_name = os.path.split(file_path)
file_name_wo_ext, ext = os.path.splitext(file_name)
filtered_directory = os.path.join(directory, 'filtered')
filtered_file_name = f"{file_name_wo_ext}_filtered{ext}"
filtered_file_path = os.path.join(filtered_directory, filtered_file_name)
os.makedirs(filtered_directory, exist_ok=True)
df.to_csv(filtered_file_path, index=False)

print(f"Filtered and analyzed data saved to {filtered_file_path}")
