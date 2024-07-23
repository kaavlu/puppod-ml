import csv
import json
from collections import defaultdict

# Recursive function to convert defaultdict to dict
def convert_defaultdict_to_dict(d):
    if isinstance(d, defaultdict):
        d = {k: convert_defaultdict_to_dict(v) for k, v in d.items()}
    return d

# Function to convert CSV to JSON and split data into two files
def csv_to_json(game_file_path, dog_file_path, json_file_path1, json_file_path2):
    # Dictionary to store the final data
    data = defaultdict(lambda: defaultdict(list))
    
    with open(game_file_path, mode='r') as game_file:
        csv_reader = csv.DictReader(game_file)
        for row in csv_reader:
            dog_id = row['DogId']
            session_id = row['SessionId']
            
            # Remove dog_id and session_id from the row data
            row_data = {k: v for k, v in row.items() if k not in ['DogId', 'SessionId']}
            
            # Append the row data under the respective dog_id and session_id
            data[dog_id][session_id].append(row_data)
    
    with open(dog_file_path, mode='r') as dog_file:
        csv_reader = csv.DictReader(dog_file)
        for row in csv_reader:
            dog_id = row['DogId']
            
            # Remove DogID 
            row_data = {k: v for k, v in row.items() if k not in ['DogId']}
            
            # Append lifetime dog stats under a specific key for each DogId
            data[dog_id]['lifetime_stats'] = row_data

    # Convert defaultdict to a regular dict for JSON serialization
    data = convert_defaultdict_to_dict(data)
    
    # Split the data into two parts
    items = list(data.items())
    mid_index = len(items) // 2
    
    data_part1 = dict(items[:mid_index])
    data_part2 = dict(items[mid_index:])
    
    with open(json_file_path1, mode='w') as json_file1:
        json.dump(data_part1, json_file1, indent=4)
    
    with open(json_file_path2, mode='w') as json_file2:
        json.dump(data_part2, json_file2, indent=4)

# Define your CSV file path and JSON file paths
game_file_path = 'data/filtered/GameSessions_filtered.csv'
json_file_path1 = 'total_data1.json'
json_file_path2 = 'total_data2.json'
dog_file_path = 'data/filtered/dog_filtered.csv'

# Call the function to convert CSV to JSON and split the data
csv_to_json(game_file_path, dog_file_path, json_file_path1, json_file_path2)
