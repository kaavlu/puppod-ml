import pandas as pd
import os
from datetime import datetime

# ------------------- enter csv path here --------------------------------
file_path = 'data/dog.csv'
df = pd.read_csv(file_path)

# ------------------- filter your file here ------------------------------
filtered_df = df[df['LifeTimeStats_TimePlayed'] != 0]

# Remove specified columns
columns_to_remove = ['PictureLocation', 'LifeTimeStats_TotalNegPrompts', 'LifeTimeStats_TotalHitsNegSound']
filtered_df = filtered_df.drop(columns=columns_to_remove)

# Convert BirthDate to age
def calculate_age(birthdate):
    birthdate = datetime.strptime(birthdate, '%m/%d/%Y %I:%M:%S %p')
    today = datetime.today()
    age = (today - birthdate).days / 365.25
    return round(age, 1)

filtered_df['Age'] = filtered_df['BirthDate'].apply(calculate_age)
filtered_df = filtered_df.drop(columns=['BirthDate'])

# ------------------- filtered csv save ----------------------------------
directory, file_name = os.path.split(file_path)
file_name_wo_ext, ext = os.path.splitext(file_name)
filtered_directory = os.path.join(directory, 'filtered')
filtered_file_name = f"{file_name_wo_ext}_filtered{ext}"
filtered_file_path = os.path.join(filtered_directory, filtered_file_name)
os.makedirs(filtered_directory, exist_ok=True)
filtered_df.to_csv(filtered_file_path, index=False)

print(f"Filtered data saved to {filtered_file_path}")

