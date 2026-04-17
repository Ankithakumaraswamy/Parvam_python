#Smart Email Spam Detection System
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
sys.path = [path for path in sys.path if Path(path or ".").resolve() != CURRENT_DIR]

from nltk.stem import PorterStemmer, WordNetLemmatizer


EMAIL_DATASET = [
    {
        "text": "<p>Congratulations!</p> You have won a FREE vacation. Click here now!!!",
        "label": "spam",
    },
    {
        "text": "Reminder: your team meeting is scheduled for 10 AM tomorrow in room 201.",
        "label": "original",
    },
    {
        "text": "Limited time offer. Buy 1 get 1 free on all electronics. Visit our website today.",
        "label": "spam",
    },
    {
        "text": "Please find the project status update attached and review it before the client call.",
        "label": "original",
    },
    {
        "text": "URGENT! Your bank account has been suspended. Verify your details immediately.",
        "label": "spam",
    },
    {
        "text": "Can we reschedule lunch to Friday? I have a doctor appointment on Thursday.",
        "label": "original",
    },
    {
        "text": "<div>Claim your cash reward now</div> by replying with your account number.",
        "label": "spam",
    },
    {
        "text": "The invoice for March has been paid successfully. Thank you for your business.",
        "label": "original",
    },
    {
        "text": "Exclusive deal for selected customers only. Earn money fast from home!!!",
        "label": "spam",
    },
    {
        "text": "Your interview has been confirmed for Monday at 2 PM. Best of luck!",
        "label": "original",
    },
    {
        "text": "Cheap medicines available online with instant delivery and huge discounts.",
        "label": "spam",
    },
    {
        "text": "Happy birthday! Wishing you a wonderful day filled with joy and success.",
        "label": "original",
    },
    {
        "text": "Win a brand new smartphone today. Register now and collect your prize instantly.",
        "label": "spam",
    },
    {
        "text": "The training session starts at 3 PM today. Please bring your laptop and ID card.",
        "label": "original",
    },
    {
        "text": "Final warning: pay your pending fee now or your service will be disconnected.",
        "label": "spam",
    },
    {
        "text": "Sharing the minutes from today's review meeting. Let me know if anything is missing.",
        "label": "original",
    },
    {
        "text": "You have been selected for a lucky draw. Send your details to receive the reward.",
        "label": "spam",
    },
    {
        "text": "Dinner plans are confirmed for Saturday night. See you at the restaurant.",
        "label": "original",
    },
    {
        "text": "Special promotion just for you. Get instant cashback on every purchase.",
        "label": "spam",
    },
    {
        "text": "Your leave request for next week has been approved by the manager.",
        "label": "original",
    },
]

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "been",
    "before",
    "by",
    "can",
    "for",
    "from",
    "has",
    "have",
    "here",
    "i",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "our",
    "the",
    "this",
    "to",
    "with",
    "you",
    "your",
}


class TextPreprocessor:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()

    def clean_text(self, text):
        text = re.sub(r"<.*?>", " ", text)
        text = re.sub(r"http\S+|www\.\S+", " ", text)
        text = text.lower().strip()
        text = re.sub(r"[^a-z\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text

    def tokenize(self, text):
        return text.split()

    def remove_stop_words(self, tokens):
        return [token for token in tokens if token not in STOP_WORDS]

    def stem_tokens(self, tokens):
        return [self.stemmer.stem(token) for token in tokens]

    def lemmatize_tokens(self, tokens):
        lemmatized = []
        for token in tokens:
            try:
                lemmatized.append(self.lemmatizer.lemmatize(token))
            except LookupError:
                lemmatized.append(token)
        return lemmatized

    def preprocess(self, text):
        cleaned_text = self.clean_text(text)
        tokens = self.tokenize(cleaned_text)
        filtered_tokens = self.remove_stop_words(tokens)
        return {
            "cleaned_text": cleaned_text,
            "filtered_tokens": filtered_tokens,
            "stemmed_tokens": self.stem_tokens(filtered_tokens),
            "lemmatized_tokens": self.lemmatize_tokens(filtered_tokens),
        }


class BagOfWordsVectorizer:
    def __init__(self):
        self.vocabulary = {}

    def fit(self, documents):
        all_words = sorted({word for document in documents for word in document})
        self.vocabulary = {word: index for index, word in enumerate(all_words)}

    def transform(self, documents):
        vectors = []
        for document in documents:
            vector = [0] * len(self.vocabulary)
            for word in document:
                if word in self.vocabulary:
                    vector[self.vocabulary[word]] += 1
            vectors.append(vector)
        return vectors

    def fit_transform(self, documents):
        self.fit(documents)
        return self.transform(documents)


class MultinomialNaiveBayes:
    def __init__(self):
        self.class_priors = {}
        self.word_counts = {}
        self.total_words = {}
        self.vocab_size = 0

    def fit(self, features, labels):
        self.vocab_size = len(features[0]) if features else 0
        class_document_counts = Counter(labels)
        total_documents = len(labels)

        self.word_counts = defaultdict(lambda: [0] * self.vocab_size)
        self.total_words = defaultdict(int)

        for row, label in zip(features, labels):
            self.class_priors[label] = class_document_counts[label] / total_documents
            for index, count in enumerate(row):
                self.word_counts[label][index] += count
                self.total_words[label] += count

    def predict_one(self, row):
        best_class = None
        best_score = float("-inf")

        for label, prior in self.class_priors.items():
            score = math.log(prior)
            for index, count in enumerate(row):
                if count == 0:
                    continue
                word_probability = (
                    self.word_counts[label][index] + 1
                ) / (self.total_words[label] + self.vocab_size)
                score += count * math.log(word_probability)

            if score > best_score:
                best_score = score
                best_class = label

        return best_class

    def predict(self, features):
        return [self.predict_one(row) for row in features]


def accuracy_score(actual, predicted):
    correct = sum(1 for truth, guess in zip(actual, predicted) if truth == guess)
    return correct / len(actual) if actual else 0.0


def split_dataset(dataset, train_ratio=0.75):
    grouped = defaultdict(list)
    for item in dataset:
        grouped[item["label"]].append(item)

    train_data = []
    test_data = []

    for label_items in grouped.values():
        split_index = max(1, int(len(label_items) * train_ratio))
        train_data.extend(label_items[:split_index])
        test_data.extend(label_items[split_index:])

    return train_data, test_data


def print_preprocessing_examples(processor, sample_count=3):
    print("TEXT CLEANING AND NORMALIZATION")
    print("-" * 50)
    for item in EMAIL_DATASET[:sample_count]:
        processed = processor.preprocess(item["text"])
        print(f"Original     : {item['text']}")
        print(f"Cleaned      : {processed['cleaned_text']}")
        print(f"Stop removed : {processed['filtered_tokens']}")
        print(f"Stemmed      : {processed['stemmed_tokens']}")
        print(f"Lemmatized   : {processed['lemmatized_tokens']}")
        print("-" * 50)


def print_feature_snapshot(vectorizer, documents, count=2):
    print("\nBAG OF WORDS FEATURE SNAPSHOT")
    print("-" * 50)
    feature_vectors = vectorizer.transform(documents[:count])
    for index, vector in enumerate(feature_vectors, start=1):
        non_zero_features = {
            word: vector[position]
            for word, position in vectorizer.vocabulary.items()
            if vector[position] > 0
        }
        print(f"Email {index}: {non_zero_features}")


def main():
    processor = TextPreprocessor()
    print_preprocessing_examples(processor)

    processed_dataset = []
    for item in EMAIL_DATASET:
        processed = processor.preprocess(item["text"])
        processed_dataset.append(
            {
                "text": item["text"],
                "label": item["label"],
                "tokens": processed["lemmatized_tokens"],
            }
        )

    train_data, test_data = split_dataset(processed_dataset)

    train_documents = [item["tokens"] for item in train_data]
    train_labels = [item["label"] for item in train_data]
    test_documents = [item["tokens"] for item in test_data]
    test_labels = [item["label"] for item in test_data]

    vectorizer = BagOfWordsVectorizer()
    train_features = vectorizer.fit_transform(train_documents)
    test_features = vectorizer.transform(test_documents)

    print_feature_snapshot(vectorizer, train_documents)

    classifier = MultinomialNaiveBayes()
    classifier.fit(train_features, train_labels)
    predictions = classifier.predict(test_features)

    print("\nCLASSIFICATION RESULTS")
    print("-" * 50)
    for email, actual, predicted in zip(test_data, test_labels, predictions):
        print(f"Email      : {' '.join(email['tokens'])}")
        print(f"Actual     : {actual}")
        print(f"Predicted  : {predicted}")
        print("-" * 50)

    accuracy = accuracy_score(test_labels, predictions)
    print(f"Accuracy on test set: {accuracy:.2%}")


if __name__ == "__main__":
    main()
