import pandas as pd

# Create sample data
data = {
    "Name": ["Ankitha", "Rahul", "Sneha", "Arjun"],
    "Age": [20, 22, 21, 23],
    "City": ["Bangalore", "Mumbai", "Delhi", "Chennai"],
    "Score": [85, 90, 78, 88]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV file
df.to_csv("students.csv", index=False)
print(df)
print("CSV file 'students.csv' created successfully!")

#add a new column to the dataframe
df["Passed"] = df["Score"] >= 80
print(df)
print("Added 'Passed' column based on 'Score'.")

#drop the "City" column
df = df.drop(columns=["City"])
print(df)
print("Dropped 'City' column.")

#write the modified DataFrame back to the same CSV file
df.to_csv("students.csv", index=False)
print("Modified DataFrame written back to 'students.csv'.")
