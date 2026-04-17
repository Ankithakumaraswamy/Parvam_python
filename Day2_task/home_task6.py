#speech-to-text post processing
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
nltk.download('stopwords', quiet=True)

DEFAULT_STOP_WORDS = set(stopwords.words('english'))
EXTRA_STOP_WORDS = {
    'um', 'uh', 'like', 'you', 'know', 'okay', 'yeah', 'right', 'actually',
    'basically', 'sort', 'kind', 'gonna', 'wanna', 'gotta', 'let', 'lets',
    'hey', 'mm', 'hmm', 'oh', 'ohh'
}

POSITIVE_WORDS = {
    'love', 'amazing', 'great', 'good', 'fantastic', 'excellent', 'happy',
    'awesome', 'wonderful', 'positive', 'enjoy', 'enjoyed', 'enjoying',
    'nice', 'perfect', 'best', 'recommend', 'recommendation'
}
NEGATIVE_WORDS = {
    'bad', 'terrible', 'awful', 'horrible', 'poor', 'worse', 'worst',
    'hate', 'disappoint', 'disappointed', 'problem', 'issue', 'noise',
    'annoying', 'slow', 'difficult', 'hard', 'failed', 'useless'
}

def clean_transcript(text: str) -> str:
    """Clean raw speech transcript text using regex and text normalization."""
    text = text.lower()
    text = re.sub(r"\[(?:noise|laugh|cough|music)\]", " ", text)
    text = re.sub(r"[^\w\s']", " ", text)
    text = re.sub(r"\b(um|uh|like|you know|you|know|okay|yeah|right|actually|basically|sort|kind|gonna|wanna|gotta|let's|lets|hey|mm|hmm|oh|ohh)\b", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> list[str]:
    return text.split()


def remove_stop_words(tokens: list[str], stop_words: set[str] | None = None) -> list[str]:
    stop_words = DEFAULT_STOP_WORDS.union(EXTRA_STOP_WORDS) if stop_words is None else set(stop_words)
    return [token for token in tokens if token not in stop_words]


def lemmatize_tokens(tokens: list[str]) -> list[str]:
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]


def sentiment_analysis(tokens: list[str]) -> dict[str, int | str]:
    positive_count = sum(1 for token in tokens if token in POSITIVE_WORDS)
    negative_count = sum(1 for token in tokens if token in NEGATIVE_WORDS)
    score = positive_count - negative_count
    label = 'positive' if score > 0 else 'negative' if score < 0 else 'neutral'
    return {
        'positive_count': positive_count,
        'negative_count': negative_count,
        'score': score,
        'sentiment': label,
    }


def process_speech_transcript(text: str) -> dict[str, object]:
    cleaned = clean_transcript(text)
    tokens = tokenize(cleaned)
    filtered_tokens = remove_stop_words(tokens)
    normalized_tokens = lemmatize_tokens(filtered_tokens)
    sentiment = sentiment_analysis(normalized_tokens)

    return {
        'raw': text,
        'cleaned': cleaned,
        'tokens': tokens,
        'filtered_tokens': filtered_tokens,
        'normalized_tokens': normalized_tokens,
        'sentiment': sentiment,
    }


if __name__ == '__main__':
    sample_transcript = (
        "Um, I really loved the product demo, but the audio quality was terrible and the "
        "speaker kept saying um and uh. It was still a great experience overall."
    )
    result = process_speech_transcript(sample_transcript)
    print('Raw transcript:')
    print(result['raw'])
    print('\nCleaned transcript:')
    print(result['cleaned'])
    print('\nFiltered tokens:')
    print(result['filtered_tokens'])
    print('\nNormalized tokens:')
    print(result['normalized_tokens'])
    print('\nSentiment:')
    print(result['sentiment'])
