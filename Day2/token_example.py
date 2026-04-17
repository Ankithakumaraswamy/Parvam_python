from nltk.tokenize import TreebankWordTokenizer
import re

text = "Python is very powerful. It is used in NLP."

# Word tokenization without external NLTK downloads
word_tokenizer = TreebankWordTokenizer()
words = word_tokenizer.tokenize(text)
print("Words:", words)

# Simple sentence tokenization without punkt/punkt_tab
sentences = re.split(r'(?<=[.!?])\s+', text)
print("Sentences:", sentences)
