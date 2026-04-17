#write a function that tokenizes a sentence into words and removes punctuation.
import re


def tokenize_and_remove_punctuation(sentence):
    tokens = re.findall(r"\b\w+\b", sentence)
    return tokens


sample_sentence = "Hello, Ankitha! Welcome to AI workshop 2026."
result = tokenize_and_remove_punctuation(sample_sentence)
print(result)
