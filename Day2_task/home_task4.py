#Social Media Toxic Comment Filter
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
sys.path = [path for path in sys.path if Path(path or ".").resolve() != CURRENT_DIR]


COMMENT_DATASET = [
    {"text": "@user1 You are so stupid and annoying!!! #worst 😡", "label": "toxic"},
    {"text": "Great job on the presentation, really clear and helpful. 😊", "label": "non-toxic"},
    {"text": "Nobody likes your useless content. Just stop posting. #trash", "label": "toxic"},
    {"text": "@friend Thanks for sharing this update, it was super informative!", "label": "non-toxic"},
    {"text": "What a pathetic excuse for an article... total garbage 🤮", "label": "toxic"},
    {"text": "Loved this recipe! Turned out perfect and my family enjoyed it.", "label": "non-toxic"},
    {"text": "You are an idiot, learn to speak properly before commenting.", "label": "toxic"},
    {"text": "This tutorial saved me a lot of time, thank you so much!", "label": "non-toxic"},
    {"text": "#loser your ideas are dumb and embarrassing 😂", "label": "toxic"},
    {"text": "Really appreciate the quick response from the support team.", "label": "non-toxic"},
    {"text": "@abc Shut up, nobody asked for your fake opinion.", "label": "toxic"},
    {"text": "The app update looks clean and works smoothly on my phone.", "label": "non-toxic"},
    {"text": "Such a hateful and disgusting comment, go away.", "label": "toxic"},
    {"text": "Beautiful artwork! The colors and style are amazing.", "label": "non-toxic"},
    {"text": "You clueless clown, this is the worst take ever.", "label": "toxic"},
    {"text": "Thanks everyone, the event was organized really well.", "label": "non-toxic"},
    {"text": "Absolute nonsense. Your page is full of lies and rubbish.", "label": "toxic"},
    {"text": "Happy to see this feature finally released, nice work team!", "label": "non-toxic"},
]

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "for",
    "from",
    "is",
    "it",
    "me",
    "my",
    "of",
    "on",
    "so",
    "the",
    "this",
    "to",
    "was",
    "your",
}

POSITIVE_WORDS = {
    "amazing",
    "appreciate",
    "beautiful",
    "clear",
    "enjoyed",
    "great",
    "happy",
    "helpful",
    "informative",
    "loved",
    "nice",
    "perfect",
    "saved",
    "smoothly",
    "thanks",
    "well",
}

NEGATIVE_WORDS = {
    "annoying",
    "clown",
    "disgusting",
    "dumb",
    "fake",
    "garbage",
    "hateful",
    "idiot",
    "lies",
    "nonsense",
    "pathetic",
    "rubbish",
    "shut",
    "stupid",
    "trash",
    "useless",
    "worst",
}


class CommentPreprocessor:
    def clean_text(self, text):
        text = re.sub(r"@\w+", " ", text)
        text = re.sub(r"#\w+", " ", text)
        text = re.sub(r"http\S+|www\.\S+", " ", text)
        text = text.encode("ascii", "ignore").decode("ascii")
        text = text.lower()
        text = re.sub(r"[^a-z\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def tokenize(self, text):
        return text.split()

    def remove_stop_words(self, tokens):
        return [token for token in tokens if token not in STOP_WORDS]

    def preprocess(self, text):
        cleaned_text = self.clean_text(text)
        tokens = self.tokenize(cleaned_text)
        filtered_tokens = self.remove_stop_words(tokens)
        return {
            "cleaned_text": cleaned_text,
            "filtered_tokens": filtered_tokens,
        }


def safe_display(text):
    return text.encode("ascii", "ignore").decode("ascii")


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
    augmented = []
    for vector, tokens in zip(vectors, documents):
        polarity_bucket = round(sentiment_polarity(tokens) + 1, 3)
        augmented.append(vector + [polarity_bucket])
    return augmented


def print_preprocessing_examples(processor, sample_count=3):
    print("TOXIC COMMENT CLEANING PIPELINE")
    print("-" * 60)
    for item in COMMENT_DATASET[:sample_count]:
        processed = processor.preprocess(item["text"])
        print(f"Original     : {safe_display(item['text'])}")
        print(f"Cleaned      : {processed['cleaned_text']}")
        print(f"Stop removed : {processed['filtered_tokens']}")
        print("-" * 60)


def build_processed_dataset(processor):
    processed_dataset = []
    for item in COMMENT_DATASET:
        processed = processor.preprocess(item["text"])
        processed_dataset.append(
            {
                "text": item["text"],
                "label": item["label"],
                "tokens": processed["filtered_tokens"],
            }
        )
    return processed_dataset


def evaluate_pipeline(dataset):
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

    print("\nCLASSIFICATION RESULTS")
    print("-" * 60)
    for comment, actual, predicted in zip(test_data, test_labels, predictions):
        print(f"Comment     : {' '.join(comment['tokens'])}")
        print(f"Polarity    : {sentiment_polarity(comment['tokens']):.3f}")
        print(f"Actual      : {actual}")
        print(f"Predicted   : {predicted}")
        print("-" * 60)

    return accuracy, vectorizer, dataset


def print_feature_snapshot(vectorizer, documents):
    print("\nBOW + SENTIMENT FEATURE SNAPSHOT")
    print("-" * 60)
    sample_vectors = vectorizer.transform(documents[:2])
    for index, (vector, tokens) in enumerate(zip(sample_vectors, documents[:2]), start=1):
        features = {
            word: vector[position]
            for word, position in vectorizer.vocabulary.items()
            if vector[position] > 0
        }
        print(f"Comment {index}: {features}")
        print(f"Sentiment polarity: {sentiment_polarity(tokens):.3f}")


def main():
    processor = CommentPreprocessor()
    print_preprocessing_examples(processor)

    processed_dataset = build_processed_dataset(processor)
    accuracy, vectorizer, dataset = evaluate_pipeline(processed_dataset)

    print_feature_snapshot(vectorizer, [item["tokens"] for item in dataset])

    print("\nMODEL SUMMARY")
    print("-" * 60)
    print("Features used        : Bag of Words counts + sentiment polarity")
    print(f"Accuracy on test set : {accuracy:.2%}")


if __name__ == "__main__":
    main()
