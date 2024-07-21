import csv
import json
from collections import defaultdict

# Function to convert CSV to JSON
def csv_to_json(csv_file_path, json_file_path):
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
    
    with open(json_file_path, mode='w') as json_file:
        json.dump(data, json_file, indent=4)

# Define your CSV file path and JSON file path
csv_file_path = 'data/filtered/GameSessions_filtered.csv'
json_file_path = 'test.json'

# Call the function to convert CSV to JSON
csv_to_json(csv_file_path, json_file_path)
