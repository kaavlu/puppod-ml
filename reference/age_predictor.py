import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
data_path = 'data/filtered/dog_filtered.csv'
df = pd.read_csv(data_path)

# Encoding categorical features using LabelEncoder
# converts non-numerical data into numerical values
label_encoders = {}
categorical_columns = ['Primary_Breed', 'Gender', 'Neutered']

for column in categorical_columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Select features to train upon
features = ['Primary_Breed', 'CurrentLevel', 'Gender', 'Neutered']
target = 'Age'

X = df[features]
y = df[target]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions and evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Mean Squared Error:", mse)
print("R^2 Score:", r2)

# Create subplots
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Primary_Breed vs Age
axs[0, 0].scatter(df['Primary_Breed'], df['Age'], alpha=0.6)
axs[0, 0].set_title('Primary Breed vs Age')
axs[0, 0].set_xlabel('Primary Breed')
axs[0, 0].set_ylabel('Age')

# Plot 2: CurrentLevel vs Age
axs[0, 1].scatter(df['CurrentLevel'], df['Age'], alpha=0.6, color='orange')
axs[0, 1].set_title('Current Level vs Age')
axs[0, 1].set_xlabel('Current Level')
axs[0, 1].set_ylabel('Age')

# Plot 3: Gender vs Age
axs[1, 0].scatter(df['Gender'], df['Age'], alpha=0.6, color='green')
axs[1, 0].set_title('Gender vs Age')
axs[1, 0].set_xlabel('Gender')
axs[1, 0].set_ylabel('Age')

# Plot 4: Neutered vs Age
axs[1, 1].scatter(df['Neutered'], df['Age'], alpha=0.6, color='red')
axs[1, 1].set_title('Neutered vs Age')
axs[1, 1].set_xlabel('Neutered')
axs[1, 1].set_ylabel('Age')

# Display the plots
plt.tight_layout()
plt.show()
