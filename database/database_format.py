import csv
import json

# Load the JSON data
with open(r'/Users/manavk/Documents/puppod/puppod-ml/data/total_data.json', 'r') as file:
    json_data = json.load(file)

# Function to parse and write Dogs table
def write_dogs_table(data):
    with open('dogs.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['DogID', 'Name', 'Primary_Breed', 'Secondary_Breed', 'CurrentLevel', 'Gender', 'Neutered', 'Age', 'ModifiedCreatedTime'])
        for dog_id, dog_data in data.items():
            dog_info = dog_data.get('dog_information', {})
            writer.writerow([
                dog_id,
                dog_info.get('Name', ''),
                dog_info.get('Primary_Breed', ''),
                dog_info.get('Secondary_Breed', ''),
                dog_info.get('CurrentLevel', ''),
                dog_info.get('Gender', ''),
                dog_info.get('Neutered', ''),
                dog_info.get('Age', ''),
                dog_info.get('ModifiedCreatedTime', '')
            ])

# Function to parse and write LifeTimeStats table
def write_lifetime_stats_table(data):
    with open('lifetime_stats.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['DogID', 'TimePlayed', 'TreatsWon', 'SuccessRate', 'TotalPrompts', 'TotalMissed', 'ModifiedCreatedTime'])
        for dog_id, dog_data in data.items():
            dog_info = dog_data.get('dog_information', {})
            writer.writerow([
                dog_id,
                dog_info.get('LifeTimeStats_TimePlayed', ''),
                dog_info.get('LifeTimeStats_TreatsWon', ''),
                dog_info.get('LifeTimeStats_SuccessRate', ''),
                dog_info.get('LifeTimeStats_TotalPrompts', ''),
                dog_info.get('LifeTimeStats_TotalMissed', ''),
                dog_info.get('ModifiedCreatedTime', '')
            ])

# Function to parse and write Sessions table
def write_sessions_table(data):
    with open('sessions.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'SessionId', 'DogID', 'GameState', 'ModifiedCreatedTime', 'NumDispenses', 'NumPrompts', 'NumNegPrompts', 
            'StartTime', 'EndTime', 'SuccessRate', 'NumMissed', 'NumHitsNegSound', 'CurrentSound', 'CurrentLevel', 
            'CurrentSoundInterval', 'IsRandom', 'MaxInterval', 'MinInterval', 'LastInteractionTime', 
            'StartGameLatency', 'EndGameLatency', 'WasGameStopCommandSent', 'GameStoppedAutomatically', 
            'DidPostProcess', 'GameTime', 'AverageResponseTime', 'PromptEffectiveness', 'SuccessRatePerSession'
        ])
        for dog_id, dog_data in data.items():
            sessions = dog_data.get('total_sessions', [])
            for session in sessions:
                writer.writerow([
                    session.get('SessionId', ''),
                    dog_id,
                    session.get('GameState', ''),
                    session.get('ModifiedCreatedTime', ''),
                    session.get('NumDispenses', ''),
                    session.get('NumPrompts', ''),
                    session.get('NumNegPrompts', ''),
                    session.get('StartTime', ''),
                    session.get('EndTime', ''),
                    session.get('SuccessRate', ''),
                    session.get('NumMissed', ''),
                    session.get('NumHitsNegSound', ''),
                    session.get('CurrentSound', ''),
                    session.get('CurrentLevel', ''),
                    session.get('CurrentSoundInterval', ''),
                    session.get('IsRandom', ''),
                    session.get('MaxInterval', ''),
                    session.get('MinInterval', ''),
                    session.get('LastInteractionTime', ''),
                    session.get('StartGameLatency', ''),
                    session.get('EndGameLatency', ''),
                    session.get('WasGameStopCommandSent', ''),
                    session.get('GameStoppedAutomatically', ''),
                    session.get('DidPostProcess', ''),
                    session.get('GameTime', ''),
                    session.get('AverageResponseTime', ''),
                    session.get('PromptEffectiveness', ''),
                    session.get('SuccessRatePerSession', '')
                ])

# Write the CSV files
write_dogs_table(json_data)
write_lifetime_stats_table(json_data)
write_sessions_table(json_data)

print("CSV files created successfully!")
