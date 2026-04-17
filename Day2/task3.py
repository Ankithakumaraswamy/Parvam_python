#build a simple sentence classifier that labels sentences as a question, exclamation or statement.
def classify_sentence(sentence):
    sentence = sentence.strip()

    if sentence.endswith("?"):
        return "Question"
    if sentence.endswith("!"):
        return "Exclamation"
    return "Statement"


sample_sentences = [
    "How are you?",
    "Python is fun.",
    "What a beautiful day!",
]

for text in sample_sentences:
    print(f"{text} -> {classify_sentence(text)}")
