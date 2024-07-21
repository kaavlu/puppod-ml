import pandas as pd

# File paths
achievements_filter_path = 'data/filtered/Achievements_filtered.csv'
dog_filter_path = 'data/filtered/dog_filtered.csv'
game_sessions_filter_path = 'data/filtered/GameSessions_filtered.csv'

# Read CSV files into DataFrames
a_df = pd.read_csv(achievements_filter_path)
d_df = pd.read_csv(dog_filter_path)
g_df = pd.read_csv(game_sessions_filter_path)

# Group data by DogId and aggregate into lists
a_grouped = a_df.groupby('DogId').agg(lambda x: list(x)).reset_index()
g_grouped = g_df.groupby('DogId').agg(lambda x: list(x)).reset_index()

# Merge the grouped data with the dog DataFrame on DogId
merged_df = d_df.merge(a_grouped, on='DogId', how='left').merge(g_grouped, on='DogId', how='left')

# Save the merged DataFrame to a new CSV file
output_path = 'data/filtered/merged_data.csv'
merged_df.to_csv(output_path, index=False)

print(f"Merged data saved to {output_path}")
