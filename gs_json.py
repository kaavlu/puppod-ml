import csv
import json
from collections import defaultdict

# Function to convert CSV to JSON and split data into two files
def csv_to_json(csv_file_path, json_file_path1, json_file_path2):
    # Dictionary to store the final data
    data = defaultdict(lambda: defaultdict(list))
    
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            dog_id = row['DogId']
            session_id = row['SessionId']
            
            # Remove dog_id and session_id from the row data
            row_data = {k: v for k, v in row.items() if k not in ['DogId', 'SessionId']}
            
            # Append the row data under the respective dog_id and session_id
            data[dog_id][session_id].append(row_data)
    
    # Convert defaultdict to a regular dict for JSON serialization
    data = {dog_id: dict(sessions) for dog_id, sessions in data.items()}
    
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
csv_file_path = 'data/filtered/GameSessions_filtered.csv'
json_file_path1 = 'total_data1.json'
json_file_path2 = 'total_data2.json'

# Call the function to convert CSV to JSON and split the data
csv_to_json(csv_file_path, json_file_path1, json_file_path2)
