#sentiment analysis example
from textblob import TextBlob
text = "I hate this product! It's amazing and works worst. However, the customer service was terrible."
blob = TextBlob(text)
sentiment = blob.sentiment
print("Sentiment polarity:", sentiment.polarity)
print("Sentiment subjectivity:", sentiment.subjectivity)
print("Overall sentiment:", "Positive" if sentiment.polarity > 0 else "Negative" if sentiment.polarity < 0 else "Neutral")


