import numpy as np

# Create two arrays
a = np.array([10, 20, 30, 40])
b = np.array([1, 2, 3, 4])

print("Array a:", a)
print("Array b:", b)

# Basic operations
print("\nAddition:", a + b)
print("Subtraction:", a - b)
print("Multiplication:", a * b)
print("Division:", a / b)

# Advanced operations
print("\nSquare of a:", np.square(a))
print("Square root of a:", np.sqrt(a))
print("Exponential of a:", np.exp(a))
print("Logarithm of a:", np.log(a))

# Aggregate operations
print("\nSum of a:", np.sum(a))
print("Mean of a:", np.mean(a))
print("Maximum value in a:", np.max(a))
print("Minimum value in a:", np.min(a))