import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming the JSON file paths (update with actual paths)
json_file_path1 = 'total_data1.json'
json_file_path2 = 'total_data2.json'

# Read the JSON files
with open(json_file_path1, mode='r') as json_file1:
    data_part1 = json.load(json_file1)

with open(json_file_path2, mode='r') as json_file2:
    data_part2 = json.load(json_file2)

# Merge the two parts of the data
data = {**data_part1, **data_part2}

# Extract the "lifetime_stats" for each dog and relevant fields
lifetime_data = []

for dog_id, details in data.items():
    if 'lifetime_stats' in details:
        lifetime_stats = details['lifetime_stats']
        primary_breed = lifetime_stats.get('Primary_Breed', 'Unknown')
        success_rate = float(lifetime_stats.get('LifeTimeStats_SuccessRate', 0))
        
        # Append the data to the list
        lifetime_data.append({
            'Primary_Breed': primary_breed,
            'LifeTimeStats_SuccessRate': success_rate
        })

# Create a DataFrame
df = pd.DataFrame(lifetime_data)

# Calculate the average success rate per breed
average_success_rate_per_breed = df.groupby('Primary_Breed')['LifeTimeStats_SuccessRate'].mean().reset_index()


# Sort in ascending order
average_success_rate_per_breed = average_success_rate_per_breed.sort_values(by='LifeTimeStats_SuccessRate', ascending=True)

# Plot the data using seaborn
plt.figure(figsize=(12, 8))
sns.barplot(x='Primary_Breed', y='LifeTimeStats_SuccessRate', data=average_success_rate_per_breed)
plt.title('Average Success Rate per Dog Breed')
plt.xlabel('Dog Breed')
plt.ylabel('Average Success Rate')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Show the plot
plt.show()