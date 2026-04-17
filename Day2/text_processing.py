text = "  Hello, World! Welcome to AI Workshop.  "

# Cleaning
print(text.strip())           
print(text.lower())           
print(text.upper())           
print(text.replace("AI", "Machine Learning"))

# Splitting and joining
words = "apple,banana,cherry".split(",")
print(words)                  
print(" | ".join(words))  

# Checking content
print("hello".isalpha())      
print("123".isdigit())        
print("hello123".isalnum())   
print("Python".startswith("Py"))  
print("Python".endswith("on"))    
