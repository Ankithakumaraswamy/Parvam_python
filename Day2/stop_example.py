text = "This is  a simple NLP example"

custom_stop_words = ["is", "a", "This"]

words=text.split()

filtered = [w for w in words if w not in custom_stop_words] 

print(filtered)