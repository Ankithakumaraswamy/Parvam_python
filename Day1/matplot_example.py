# Matplotlib example
import matplotlib.pyplot as plt

# Sample data
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]

# Create a line plot
plt.plot(x, y, marker='o')

# Add titles and labels
plt.title("Sample Line Plot")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")

# Show the plot
plt.show()

# Create a bar chart
categories = ['A', 'B', 'C', 'D', 'E']
values = [5, 7, 3, 8, 6]
plt.bar(categories, values, color='skyblue')
plt.title("Sample Bar Chart")
plt.xlabel("Categories")
plt.ylabel("Values")
plt.show()

# Create a scatter plot
x_scatter = [1, 2, 3, 4, 5]
y_scatter = [2, 3, 5, 7, 11]
plt.scatter(x_scatter, y_scatter, color='red')
plt.title("Sample Scatter Plot")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()

# Create a histogram
data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
plt.hist(data, bins=4, color='green', edgecolor='black')
plt.title("Sample Histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()

# Create a pie chart
labels = ['Category A', 'Category B', 'Category C']
sizes = [30, 45, 25]
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title("Sample Pie Chart")
plt.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
plt.show()

# Create a box plot
data_box = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
plt.boxplot(data_box)
plt.title("Sample Box Plot")
plt.ylabel("Values")
plt.show()

#show all the plots together
plt.figure(figsize=(10, 8))
plt.subplot(2, 2, 1)
plt.plot(x, y, marker='o')
plt.title("Line Plot")

plt.subplot(2, 2, 2)
plt.bar(categories, values, color='skyblue')
plt.title("Bar Chart")

plt.subplot(2, 2, 3)
plt.scatter(x_scatter, y_scatter, color='red')
plt.title("Scatter Plot")

plt.subplot(2, 2, 4)
plt.hist(data, bins=4, color='green', edgecolor='black')
plt.title("Histogram")
plt.tight_layout()
plt.show()


