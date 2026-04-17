import matplotlib.pyplot as plt
import numpy as np

# Sample data
x = np.arange(1, 11)
y1 = x * 2
y2 = x ** 2
y3 = np.sqrt(x)
y4 = np.log(x)
y5 = np.sin(x)
y6 = np.cos(x)

# Create a 3x2 grid (6 graphs)
plt.figure(figsize=(12, 10))

# 1. Line Graph
plt.subplot(3, 2, 1)
plt.plot(x, y1, color='red')
plt.title("Line Graph")

# 2. Bar Graph
plt.subplot(3, 2, 2)
plt.bar(x, y2, color='blue')
plt.title("Bar Graph")

# 3. Scatter Plot
plt.subplot(3, 2, 3)
plt.scatter(x, y3, color='green')
plt.title("Scatter Plot")

# 4. Histogram
plt.subplot(3, 2, 4)
plt.hist(y4, color='purple')
plt.title("Histogram")

# 5. Pie Chart
plt.subplot(3, 2, 5)
labels = ['A', 'B', 'C', 'D']
sizes = [15, 30, 35, 20]
plt.pie(sizes, labels=labels, colors=['gold', 'cyan', 'lightcoral', 'pink'], autopct='%1.1f%%')
plt.title("Pie Chart")

# 6. Area Plot
plt.subplot(3, 2, 6)
plt.fill_between(x, y5, color='orange')
plt.title("Area Plot")

# Adjust layout
plt.tight_layout()

# Show all graphs in one window
plt.show()

