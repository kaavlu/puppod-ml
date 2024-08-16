import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np

# Assuming: parameters is a list of params
#           target & params are in dog_information
#           targetDog is well formed & only has params
def runModel(parameters, target, targetDog):

    # Loading data 
    # (Flask app should have db call here)
    with open('data/total_data.json') as f:
        json_data = json.load(f)

    data_list = []

    for key, value in json_data.items():
        if 'dog_information' in value:
            dog_info = value['dog_information']
            dog_info[target] = dog_info.get(target, None) 
            data_list.append(dog_info)

    if not data_list:
        print("No valid data found in the JSON file.")
        return
    
    data = pd.DataFrame(data_list)

    if target not in data.columns:
        print(f"Target column '{target}' is not in the DataFrame.")
        return

    # Filter data to only include parameters and target columns
    data = data[parameters + [target]]
    
    # Drop rows without our target param
    data = data.dropna(subset=[target])

    encoder = OneHotEncoder(sparse_output=False)

    # Encode appropriate params
    qualitativeData = []

    for parameter in parameters:
        if parameter in ['Gender', 'Primary_Breed', 'Secondary_Breed', 'Neutered']:
            qualitativeData.append(parameter)
    
    # Encode the qualitative data
    if qualitativeData:
        encoded_data = encoder.fit_transform(data[qualitativeData])
        encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(qualitativeData))

        # Encode targetDog
        targetDog_df = pd.DataFrame([targetDog])
        encoded_targetDog = encoder.transform(targetDog_df[qualitativeData])

        not_encoded_data = []

        for parameter in parameters:
            if parameter not in qualitativeData:
                not_encoded_data.append(parameter)

        targetDog_encoded = pd.concat([targetDog_df[not_encoded_data].reset_index(drop=True),
                                     pd.DataFrame(encoded_targetDog, columns=encoder.get_feature_names_out(qualitativeData))],
                                    axis=1)
        
        # Drop original qualitative columns and concatenate the encoded data
        data = data.drop(columns=qualitativeData)
        data_encoded = pd.concat([data.reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)
    else:
        data_encoded = data

    # Define target
    y = data_encoded[target]
    X = data_encoded.drop(columns=[target])

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    # Train the model
    model.fit(X_train, y_train) 

    # The following could be useful if we want to provide some metric of accuracy for output
    # Make predictions on the test set
    # y_pred = model.predict(X_test)

    # Validity scores
    # r2 = r2_score(y_test, y_pred)
    # mae = mean_absolute_error(y_test, y_pred)
    # rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    # Predict the success rate
    return model.predict(targetDog_encoded)

def main():
    parameters = ['Age', 'Gender', 'Primary_Breed']
    target = 'LifeTimeStats_SuccessRate'

    targetDog = {
        'Age': 4,
        'Gender': 'BOY',
        'Primary_Breed': 'Goldendoodle'
    }

    # Predict the success rate
    predicted_success_rate = runModel(parameters, target, targetDog)
    print(f"Predicted Success Rate: {predicted_success_rate[0]}")


if __name__ == "__main__":
    main()



