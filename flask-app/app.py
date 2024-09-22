from flask import Flask, request, jsonify
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder

app = Flask(__name__)

def random_forest_regression(age, gender, breed):
    with open('/app/data/total_data.json') as f:
        json_data = json.load(f)

    data_list = []
    for key, value in json_data.items():
        if 'dog_information' in value:
            dog_info = value['dog_information']
            dog_info['SuccessRate'] = dog_info.get('LifeTimeStats_SuccessRate', None)
            data_list.append(dog_info)

    if not data_list:
        return None

    data = pd.DataFrame(data_list)
    data = data[['Age', 'Gender', 'Primary_Breed', 'SuccessRate']]
    data = data.dropna(subset=['SuccessRate'])

    encoder = OneHotEncoder(sparse_output=False)
    encoded_data = encoder.fit_transform(data[['Gender', 'Primary_Breed']])
    encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(['Gender', 'Primary_Breed']))
    data_encoded = pd.concat([data[['Age']], encoded_df], axis=1)

    y = data['SuccessRate']
    X_train, X_test, y_train, y_test = train_test_split(data_encoded, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    example_dog = {'Age': age, 'Gender': gender, 'Primary_Breed': breed}
    example_dog_df = pd.DataFrame([example_dog])
    encoded_example = encoder.transform(example_dog_df[['Gender', 'Primary_Breed']])
    example_dog_encoded = pd.concat([example_dog_df[['Age']].reset_index(drop=True),
                                     pd.DataFrame(encoded_example, columns=encoder.get_feature_names_out(['Gender', 'Primary_Breed']))],
                                    axis=1)

    predicted_success_rate = model.predict(example_dog_encoded)
    return predicted_success_rate[0]

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    age = data['age']
    gender = data['gender']
    breed = data['breed']
    result = random_forest_regression(age, gender, breed)
    return jsonify({'predicted_success_rate': result})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
