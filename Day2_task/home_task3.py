#Fake News Detection System
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
sys.path = [path for path in sys.path if Path(path or ".").resolve() != CURRENT_DIR]

from nltk.stem import PorterStemmer, WordNetLemmatizer


NEWS_DATASET = [
    {
        "text": "Breaking!!! Scientists confirm a major vaccine breakthrough after successful trials and hospital reports.",
        "label": "real",
    },
    {
        "text": "SHOCKING secret cure hidden by doctors!!! Click now before this story disappears forever.",
        "label": "fake",
    },
    {
        "text": "The finance ministry released its quarterly report showing stable inflation and moderate growth.",
        "label": "real",
    },
    {
        "text": "Celebrity says aliens control the weather and government satellites are spying through rain clouds!!!",
        "label": "fake",
    },
    {
        "text": "Local authorities opened a new public health center to improve emergency care in rural areas.",
        "label": "real",
    },
    {
        "text": "<div>Miracle weight-loss pill melts fat overnight</div> experts hate this one weird trick.",
        "label": "fake",
    },
    {
        "text": "Researchers published peer-reviewed findings on climate patterns in an international science journal.",
        "label": "real",
    },
    {
        "text": "Urgent alert: drinking hot lemon soda cures every infection instantly according to unnamed insiders.",
        "label": "fake",
    },
    {
        "text": "The election commission announced updated polling schedules and voter assistance helplines for citizens.",
        "label": "real",
    },
    {
        "text": "You won't believe this banned video proving the moon landing was filmed inside a shopping mall.",
        "label": "fake",
    },
    {
        "text": "A university study found improved crop yields after new irrigation methods were tested across districts.",
        "label": "real",
    },
    {
        "text": "Doctors furious after teenager exposes instant memory hack that works in five minutes!!!",
        "label": "fake",
    },
    {
        "text": "Railway officials confirmed service restoration after heavy rain caused temporary delays on two routes.",
        "label": "real",
    },
    {
        "text": "Ancient crystal device discovered in village can charge phones without electricity, witnesses claim.",
        "label": "fake",
    },
    {
        "text": "The city council approved a new waste management plan after reviewing environmental data.",
        "label": "real",
    },
    {
        "text": "Hidden market formula guarantees massive profits with zero risk, leaked by anonymous billionaire.",
        "label": "fake",
    },
    {
        "text": "Health officials reported a decline in seasonal infections following the vaccination campaign.",
        "label": "real",
    },
    {
        "text": "Secret ancient herb reverses aging in 24 hours and scientists are terrified to discuss it.",
        "label": "fake",
    },
    {
        "text": "Meteorological experts issued a rainfall advisory based on satellite observations and historical records.",
        "label": "real",
    },
    {
        "text": "Exclusive rumor reveals schools will replace textbooks with mind-reading chips next month.",
        "label": "fake",
    },
]

STOP_WORDS = {
    "a",
    "after",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "in",
    "inside",
    "its",
    "is",
    "it",
    "new",
    "of",
    "on",
    "the",
    "this",
    "to",
    "was",
    "were",
    "with",
}

POSITIVE_WORDS = {
    "approved",
    "breakthrough",
    "confirmed",
    "effective",
    "growth",
    "improve",
    "improved",
    "restoration",
    "stable",
    "successful",
    "support",
}

NEGATIVE_WORDS = {
    "alert",
    "banned",
    "furious",
    "hate",
    "hidden",
    "leaked",
    "risk",
    "secret",
    "shocking",
    "terrified",
    "urgent",
    "weird",
}


class NewsPreprocessor:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()

    def clean_text(self, text):
        text = re.sub(r"<.*?>", " ", text)
        text = re.sub(r"http\S+|www\.\S+", " ", text)
        text = text.lower()
        text = re.sub(r"[^a-z\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def tokenize(self, text):
        return text.split()

    def remove_stop_words(self, tokens):
        return [token for token in tokens if token not in STOP_WORDS]

    def stem_tokens(self, tokens):
        return [self.stemmer.stem(token) for token in tokens]

    def lemmatize_tokens(self, tokens):
        processed = []
        for token in tokens:
            try:
                processed.append(self.lemmatizer.lemmatize(token))
            except LookupError:
                processed.append(token)
        return processed

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
        words = sorted({word for document in documents for word in document})
        self.vocabulary = {word: index for index, word in enumerate(words)}

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
        class_counts = Counter(labels)
        total_docs = len(labels)

        self.word_counts = defaultdict(lambda: [0] * self.vocab_size)
        self.total_words = defaultdict(int)

        for row, label in zip(features, labels):
            self.class_priors[label] = class_counts[label] / total_docs
            for index, count in enumerate(row):
                self.word_counts[label][index] += count
                self.total_words[label] += count

    def predict_one(self, row):
        best_label = None
        best_score = float("-inf")

        for label, prior in self.class_priors.items():
            score = math.log(prior)
            for index, count in enumerate(row):
                if count == 0:
                    continue
                probability = (
                    self.word_counts[label][index] + 1
                ) / (self.total_words[label] + self.vocab_size)
                score += count * math.log(probability)

            if score > best_score:
                best_score = score
                best_label = label

        return best_label

    def predict(self, features):
        return [self.predict_one(row) for row in features]


def accuracy_score(actual, predicted):
    matches = sum(1 for truth, guess in zip(actual, predicted) if truth == guess)
    return matches / len(actual) if actual else 0.0


def split_dataset(dataset, train_ratio=0.7):
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


def sentiment_polarity(tokens):
    positive_count = sum(1 for token in tokens if token in POSITIVE_WORDS)
    negative_count = sum(1 for token in tokens if token in NEGATIVE_WORDS)
    total = len(tokens) if tokens else 1
    return (positive_count - negative_count) / total


def augment_with_sentiment(vectors, documents):
    augmented_vectors = []
    for vector, tokens in zip(vectors, documents):
        polarity_bucket = round(sentiment_polarity(tokens), 3)
        augmented_vectors.append(vector + [polarity_bucket])
    return augmented_vectors


def print_preprocessing_examples(processor, sample_count=3):
    print("NEWS CLEANING PIPELINE")
    print("-" * 60)
    for item in NEWS_DATASET[:sample_count]:
        processed = processor.preprocess(item["text"])
        print(f"Original     : {item['text']}")
        print(f"Cleaned      : {processed['cleaned_text']}")
        print(f"Stop removed : {processed['filtered_tokens']}")
        print(f"Stemmed      : {processed['stemmed_tokens']}")
        print(f"Lemmatized   : {processed['lemmatized_tokens']}")
        print("-" * 60)


def build_processed_dataset(processor, mode):
    key = "stemmed_tokens" if mode == "stemming" else "lemmatized_tokens"
    processed_dataset = []
    for item in NEWS_DATASET:
        processed = processor.preprocess(item["text"])
        processed_dataset.append(
            {
                "text": item["text"],
                "label": item["label"],
                "tokens": processed[key],
            }
        )
    return processed_dataset


def evaluate_pipeline(name, dataset):
    train_data, test_data = split_dataset(dataset)
    train_documents = [item["tokens"] for item in train_data]
    train_labels = [item["label"] for item in train_data]
    test_documents = [item["tokens"] for item in test_data]
    test_labels = [item["label"] for item in test_data]

    vectorizer = BagOfWordsVectorizer()
    train_features = vectorizer.fit_transform(train_documents)
    test_features = vectorizer.transform(test_documents)

    train_features = augment_with_sentiment(train_features, train_documents)
    test_features = augment_with_sentiment(test_features, test_documents)

    classifier = MultinomialNaiveBayes()
    classifier.fit(train_features, train_labels)
    predictions = classifier.predict(test_features)
    accuracy = accuracy_score(test_labels, predictions)

    print(f"\n{name.upper()} + BOW + SENTIMENT RESULTS")
    print("-" * 60)
    for article, actual, predicted in zip(test_data, test_labels, predictions):
        print(f"Article     : {' '.join(article['tokens'])}")
        print(f"Polarity    : {sentiment_polarity(article['tokens']):.3f}")
        print(f"Actual      : {actual}")
        print(f"Predicted   : {predicted}")
        print("-" * 60)

    return accuracy, vectorizer


def print_feature_snapshot(vectorizer, documents, title):
    print(f"\n{title}")
    print("-" * 60)
    sample_vectors = vectorizer.transform(documents[:2])
    for index, (vector, tokens) in enumerate(zip(sample_vectors, documents[:2]), start=1):
        features = {
            word: vector[position]
            for word, position in vectorizer.vocabulary.items()
            if vector[position] > 0
        }
        print(f"Article {index}: {features}")
        print(f"Sentiment polarity: {sentiment_polarity(tokens):.3f}")


def main():
    processor = NewsPreprocessor()
    print_preprocessing_examples(processor)

    stemmed_dataset = build_processed_dataset(processor, "stemming")
    lemmatized_dataset = build_processed_dataset(processor, "lemmatization")

    stem_accuracy, stem_vectorizer = evaluate_pipeline("stemming", stemmed_dataset)
    lemma_accuracy, lemma_vectorizer = evaluate_pipeline("lemmatization", lemmatized_dataset)

    print_feature_snapshot(
        stem_vectorizer,
        [item["tokens"] for item in stemmed_dataset],
        "STEMMING FEATURE SNAPSHOT",
    )
    print_feature_snapshot(
        lemma_vectorizer,
        [item["tokens"] for item in lemmatized_dataset],
        "LEMMATIZATION FEATURE SNAPSHOT",
    )

    print("\nACCURACY COMPARISON")
    print("-" * 60)
    print(f"Stemming accuracy     : {stem_accuracy:.2%}")
    print(f"Lemmatization accuracy: {lemma_accuracy:.2%}")
    if stem_accuracy > lemma_accuracy:
        print("Better approach       : Stemming performed better on this dataset.")
    elif lemma_accuracy > stem_accuracy:
        print("Better approach       : Lemmatization performed better on this dataset.")
    else:
        print("Better approach       : Both approaches achieved the same accuracy.")


if __name__ == "__main__":
    main()
