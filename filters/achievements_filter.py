import pandas as pd
import os


# Reading in csv
file_path = 'data/Achievements.csv'
df = pd.read_csv(file_path)

# Only care about completeed achievements
filtered_df = df[df['AchievementProgress'] != 0]


# Remove unhelpful data
columns_to_remove = ['PictureLocation', 'ModifiedCreatedTime']
filtered_df = filtered_df.drop(columns=columns_to_remove)

# Saving filtered data
directory, file_name = os.path.split(file_path)
file_name_wo_ext, ext = os.path.splitext(file_name)
filtered_directory = os.path.join(directory, 'filtered')
filtered_file_name = f"{file_name_wo_ext}_filtered{ext}"
filtered_file_path = os.path.join(filtered_directory, filtered_file_name)
os.makedirs(filtered_directory, exist_ok=True)
filtered_df.to_csv(filtered_file_path, index=False)

print(f"Filtered data saved to {filtered_file_path}")


