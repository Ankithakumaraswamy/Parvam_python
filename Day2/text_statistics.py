import re
from collections import Counter


def analyze_text_statistics(text):
    words = re.findall(r"\b\w+\b", text.lower())
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]

    character_count = len(text)
    word_count = len(words)
    sentence_count = len(sentences)
    average_word_length = sum(len(word) for word in words) / word_count if word_count else 0
    longest_word = max(words, key=len) if words else ""
    most_common_words = Counter(words).most_common(5)

    print("Text Statistics")
    print("----------------")
    print("Characters:", character_count)
    print("Words:", word_count)
    print("Sentences:", sentence_count)
    print("Average word length:", round(average_word_length, 2))
    print("Longest word:", longest_word)
    print("Most common words:", most_common_words)


sample_text = "Python is easy to learn. Python is powerful and useful for text analysis!"
analyze_text_statistics(sample_text)
