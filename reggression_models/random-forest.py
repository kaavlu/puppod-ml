import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder

# Assuming your JSON data is already loaded as a dictionary
def random_forest_regression(age, gender, breed):
    # Load the JSON data directly
    with open('/data/total_data.json') as f:
        json_data = json.load(f)  # json.load is correct for loading from a file

    # Convert JSON data to a pandas DataFrame
    data_list = []
    for key, value in json_data.items():
        # Safely access 'dog_information' key
        if 'dog_information' in value:
            dog_info = value['dog_information']
            dog_info['SuccessRate'] = dog_info.get('LifeTimeStats_SuccessRate', None)  # Handle missing 'LifeTimeStats_SuccessRate'
            data_list.append(dog_info)

    # If no valid data found, exit the function
    if not data_list:
        print("No valid data found in the JSON file.")
        return

    data = pd.DataFrame(data_list)

    # Feature selection: Only keep relevant columns (Age, Gender, Primary_Breed, SuccessRate)
    data = data[['Age', 'Gender', 'Primary_Breed', 'SuccessRate']]

    # Drop any rows with missing SuccessRate
    data = data.dropna(subset=['SuccessRate'])

    # Encode categorical variables
    encoder = OneHotEncoder(sparse_output=False)
    encoded_data = encoder.fit_transform(data[['Gender', 'Primary_Breed']])

    # Create a DataFrame with the encoded columns
    encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(['Gender', 'Primary_Breed']))

    # Combine encoded columns with original data
    data_encoded = pd.concat([data[['Age']], encoded_df], axis=1)

    # Define the target variable
    y = data['SuccessRate']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data_encoded, y, test_size=0.2, random_state=42)

    # Initialize the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Example prediction
    example_dog = {
        'Age': age,  # Age of the dog
        'Gender': gender,  # Gender of the dog
        'Primary_Breed': breed  # Breed of the dog
    }

    # Convert example dog data to DataFrame and encode it
    example_dog_df = pd.DataFrame([example_dog])
    encoded_example = encoder.transform(example_dog_df[['Gender', 'Primary_Breed']])
    example_dog_encoded = pd.concat([example_dog_df[['Age']].reset_index(drop=True),
                                     pd.DataFrame(encoded_example, columns=encoder.get_feature_names_out(['Gender', 'Primary_Breed']))],
                                    axis=1)

    # Predict the success rate
    predicted_success_rate = model.predict(example_dog_encoded)
    print(f"Predicted Success Rate: {predicted_success_rate[0]}")

# Main function to call the test_function
def main():
    random_forest_regression(4, "GIRL", "Goldendoodle")

if __name__ == "__main__":
    main()
