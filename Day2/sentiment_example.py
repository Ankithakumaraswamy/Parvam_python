#sentiment analysis example
import re
text = "I love this product! It's amazing and works great. However, the customer service was terrible."
positive_words = ["love", "amazing", "great"]
negative_words = ["terrible", "bad", "awful"]
positive_count = sum(1 for word in re.findall(r"\b\w+\b", text.lower()) if word in positive_words)
negative_count = sum(1 for word in re.findall(r"\b\w+\b", text.lower()) if word in negative_words)
print("Positive words count:", positive_count)
print("Negative words count:", negative_count)

