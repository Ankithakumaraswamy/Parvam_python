import pandas as pd
data = {
    "name": ["Alice", "Bob", "Carol", "Dave", "Eve"],
    "age": [30, 25, 27, 22, 29],
    "city": ["New York", "Los Angeles", "Chicago", "New York", "Chicago"],
    "sales": [100, 150, 200, 130, 170],
}
df = pd.DataFrame(data)
print("--- DataFrame created from dict ---")
print(df, "\n")

#pandas series example
ages = df["age"]
print("--- Ages Series ---")
print(ages, "\n")

#pandas dataframe example
sales_by_city = df.groupby("city")["sales"].sum()
print("--- Sales by city ---")
print(sales_by_city, "\n")

