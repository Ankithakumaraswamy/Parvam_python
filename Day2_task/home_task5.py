#News Article Categorization Engine
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
        "text": "The football team secured a dramatic win after extra time in the national championship match.",
        "label": "sports",
    },
    {
        "text": "The central bank announced new policies to control inflation and support long-term growth.",
        "label": "business",
    },
    {
        "text": "Researchers unveiled an AI-powered medical imaging tool that improves early disease detection.",
        "label": "technology",
    },
    {
        "text": "Parliament passed a new education bill after hours of debate between opposition leaders.",
        "label": "politics",
    },
    {
        "text": "The star batsman scored a century while the bowlers dominated the final overs.",
        "label": "sports",
    },
    {
        "text": "Stock markets rose sharply as investors reacted to stronger quarterly earnings reports.",
        "label": "business",
    },
    {
        "text": "A software company launched a cloud security platform with advanced automation features.",
        "label": "technology",
    },
    {
        "text": "The prime minister addressed parliament and outlined the government's foreign policy strategy.",
        "label": "politics",
    },
    {
        "text": "The tennis player returned from injury and won the tournament in straight sets.",
        "label": "sports",
    },
    {
        "text": "Retail sales improved this quarter as consumer spending increased across urban markets.",
        "label": "business",
    },
    {
        "text": "Scientists developed a faster battery charging system for next-generation electric vehicles.",
        "label": "technology",
    },
    {
        "text": "Election officials released updated voting guidelines ahead of the regional polls.",
        "label": "politics",
    },
    {
        "text": "The coach praised the young striker for his disciplined performance throughout the season.",
        "label": "sports",
    },
    {
        "text": "The startup raised fresh funding to expand its digital payments business internationally.",
        "label": "business",
    },
    {
        "text": "Engineers tested a robotics system that can assist workers in large warehouses.",
        "label": "technology",
    },
    {
        "text": "Lawmakers discussed tax reforms and welfare spending during the budget session.",
        "label": "politics",
    },
    {
        "text": "Fans celebrated as the club lifted the trophy after an unbeaten season.",
        "label": "sports",
    },
    {
        "text": "Oil prices fell after new trade data raised concerns about global demand.",
        "label": "business",
    },
    {
        "text": "A major smartphone brand introduced a device with enhanced camera and chip performance.",
        "label": "technology",
    },
    {
        "text": "The opposition party criticized the administration's handling of public infrastructure projects.",
        "label": "politics",
    },
]

STOP_WORDS = {
    "a",
    "after",
    "an",
    "and",
    "as",
    "of",
    "the",
    "to",
    "for",
    "from",
    "in",
    "its",
    "of",
    "that",
    "this",
    "with",
    "while",
    "during",
    "his",
    "their",
    "new",
}


class NewsPreprocessor:
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


def print_preprocessing_examples(processor, sample_count=3):
    print("NEWS PREPROCESSING PIPELINE")
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

    classifier = MultinomialNaiveBayes()
    classifier.fit(train_features, train_labels)
    predictions = classifier.predict(test_features)
    accuracy = accuracy_score(test_labels, predictions)

    print(f"\n{name.upper()} + BOW RESULTS")
    print("-" * 60)
    for article, actual, predicted in zip(test_data, test_labels, predictions):
        print(f"Article     : {' '.join(article['tokens'])}")
        print(f"Actual      : {actual}")
        print(f"Predicted   : {predicted}")
        print("-" * 60)

    return accuracy, vectorizer


def print_feature_snapshot(vectorizer, documents, title):
    print(f"\n{title}")
    print("-" * 60)
    sample_vectors = vectorizer.transform(documents[:2])
    for index, vector in enumerate(sample_vectors, start=1):
        features = {
            word: vector[position]
            for word, position in vectorizer.vocabulary.items()
            if vector[position] > 0
        }
        print(f"Article {index}: {features}")


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
