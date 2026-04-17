#build a simple text analyzer 

import re
from collections import Counter


def analyze_text(text):
    words = re.findall(r"\b\w+\b", text.lower())
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]

    positive_words = {"good", "great", "amazing", "happy", "love", "excellent", "best"}
    negative_words = {"bad", "worst", "terrible", "sad", "hate", "awful", "poor"}

    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)

    if positive_count > negative_count:
        sentiment = "Positive"
    elif negative_count > positive_count:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    word_frequency = Counter(words).most_common(5)

    print("Text Analyzer Result")
    print("--------------------")
    print("Characters:", len(text))
    print("Words:", len(words))
    print("Sentences:", len(sentences))
    print("Positive words:", positive_count)
    print("Negative words:", negative_count)
    print("Sentiment:", sentiment)
    print("Top 5 frequent words:", word_frequency)


sample_text = "I love Python, but i hate bugs."
analyze_text(sample_text)
