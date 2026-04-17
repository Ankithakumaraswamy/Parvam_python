from nltk.stem import WordNetLemmatizer
import nltk

nltk.download('wordnet')
nltk.download('omw-1.4')

words = ["playing", "running", "studies", "better"]

lemmatizer = WordNetLemmatizer()

for word in words:
    print(word, "→", lemmatizer.lemmatize(word))