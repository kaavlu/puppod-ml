import csv
import json
from collections import defaultdict

# Recursive function to convert defaultdict to dict
def convert_defaultdict_to_dict(d):
    if isinstance(d, defaultdict):
        d = {k: convert_defaultdict_to_dict(v) for k, v in d.items()}
    return d

# Function to convert CSV to JSON and split data into two files
def csv_to_json(game_file_path, dog_file_path, json_file_path1, json_file_path2, total_json_file_path):
    # Dictionary to store the final data
    data = defaultdict(lambda: defaultdict(list))
    
    # Process the dog stats CSV file first to ensure dog_information is added before sessions
    with open(dog_file_path, mode='r') as dog_file:
        csv_reader = csv.DictReader(dog_file)
        for row in csv_reader:
            dog_id = row['DogId']
            
            # Extract the relevant dog stats
            dog_information = {k: v for k, v in row.items() if k in [
                'Name', 'Primary_Breed', 'Secondary_Breed', 'CurrentLevel', 'Gender', 'Neutered',
                'LifeTimeStats_TimePlayed', 'LifeTimeStats_TreatsWon', 'LifeTimeStats_SuccessRate',
                'LifeTimeStats_TotalPrompts', 'LifeTimeStats_TotalMissed', 'ModifiedCreatedTime', 'Age'
            ]}
            
            # Add the dog stats under "dog_information"
            data[dog_id]['dog_information'] = dog_information

    # Process the game sessions CSV file and add sessions under "total_sessions"
    with open(game_file_path, mode='r') as game_file:
        csv_reader = csv.DictReader(game_file)
        for row in csv_reader:
            dog_id = row['DogId']
            session_id = row['SessionId']
            
            # Remove dog_id and session_id from the row data
            row_data = {k: v for k, v in row.items() if k not in ['DogId', 'SessionId']}
            row_data['SessionId'] = session_id
            
            # Append the row data to the "total_sessions" list
            data[dog_id]['total_sessions'].append(row_data)
    
    # Convert defaultdict to a regular dict for JSON serialization
    data = convert_defaultdict_to_dict(data)
    
    # Save the complete data into the total JSON file
    with open(total_json_file_path, mode='w') as total_json_file:
        json.dump(data, total_json_file, indent=4)
    
    # Split the data into two parts
    items = list(data.items())
    mid_index = len(items) // 2
    
    data_part1 = dict(items[:mid_index])
    data_part2 = dict(items[mid_index:])
    
    with open(json_file_path1, mode='w') as json_file1:
        json.dump(data_part1, json_file1, indent=4)
    
    with open(json_file_path2, mode='w') as json_file2:
        json.dump(data_part2, json_file2, indent=4)

# Define your CSV file paths and JSON file paths
game_file_path = 'data/filtered/GameSessions_filtered.csv'
dog_file_path = 'data/filtered/dog_filtered.csv'
json_file_path1 = 'total_data1.json'
json_file_path2 = 'total_data2.json'
total_json_file_path = 'total_data.json'

# Call the function to convert CSV to JSON, save the complete data, and split the data
csv_to_json(game_file_path, dog_file_path, json_file_path1, json_file_path2, total_json_file_path)
