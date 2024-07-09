import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# still playing around with this but just an example of how to view data


df = pd.read_csv('data/filtered/dog_filtered.csv')

df['ModifiedCreatedTime'] = pd.to_datetime(df['ModifiedCreatedTime'])

print(df.head())

# Create a bar plot for average age per dog breed
plt.figure(figsize=(12, 6))
avg_age_per_breed = df.groupby('Primary_Breed')['Age'].mean().reset_index()
sns.barplot(data=avg_age_per_breed, x='Primary_Breed', y='Age', palette='viridis')
plt.xticks(rotation=90)
plt.title('Average Age per Dog Breed')
plt.xlabel('Dog Breed')
plt.ylabel('Average Age')
plt.show()

# Create a box plot to show the distribution of dog ages by gender
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x='Gender', y='Age', palette='Set2')
plt.title('Age Distribution by Gender')
plt.xlabel('Gender')
plt.ylabel('Age')
plt.show()

# Create a scatter plot to show the relationship between Time Played and Age
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='LifeTimeStats_TimePlayed', y='Age', hue='Gender', palette='coolwarm')
plt.title('Time Played vs. Age')
plt.xlabel('Time Played (seconds)')
plt.ylabel('Age')
plt.show()

# Create a histogram of the dogs' ages
plt.figure(figsize=(8, 6))
sns.histplot(data=df, x='Age', bins=20, kde=True, color='blue')
plt.title('Age Distribution of Dogs')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()
