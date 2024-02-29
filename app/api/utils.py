import pickle
import re
from typing import Callable

# nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
# grouping together the inflected forms ("better" -> "good")

# Load
with open("models/pipeline.pkl", "rb") as f:
    loaded_pipe = pickle.load(f)

# Defining dictionary containing all emojis with their meanings.
emojis = {
    ":)": "smile",
    ":-)": "smile",
    ";d": "wink",
    ":-E": "vampire",
    ":(": "sad",
    ":-(": "sad",
    ":-<": "sad",
    ":P": "raspberry",
    ":O": "surprised",
    ":-@": "shocked",
    ":@": "shocked",
    ":-$": "confused",
    ":\\": "annoyed",
    ":#": "mute",
    ":X": "mute",
    ":^)": "smile",
    ":-&": "confused",
    "$_$": "greedy",
    "@@": "eyeroll",
    ":-!": "confused",
    ":-D": "smile",
    ":-0": "yell",
    "O.o": "confused",
    "<(-_-)>": "robot",
    "d[-_-]b": "dj",
    ":'-)": "sadsmile",
    ";)": "wink",
    ";-)": "wink",
    "O:-)": "angel",
    "O*-)": "angel",
    "(:-D": "gossip",
    "=^.^=": "cat",
}

# Defining set containing all stopwords in english.
stopwords_manual = [
    "a",
    "about",
    "above",
    "after",
    "again",
    "ain",
    "all",
    "am",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "be",
    "because",
    "been",
    "before",
    "being",
    "below",
    "between",
    "both",
    "by",
    "can",
    "d",
    "did",
    "do",
    "does",
    "doing",
    "down",
    "during",
    "each",
    "few",
    "for",
    "from",
    "further",
    "had",
    "has",
    "have",
    "having",
    "he",
    "her",
    "here",
    "hers",
    "herself",
    "him",
    "himself",
    "his",
    "how",
    "i",
    "if",
    "in",
    "into",
    "is",
    "it",
    "its",
    "itself",
    "just",
    "ll",
    "m",
    "ma",
    "me",
    "more",
    "most",
    "my",
    "myself",
    "now",
    "o",
    "of",
    "on",
    "once",
    "only",
    "or",
    "other",
    "our",
    "ours",
    "ourselves",
    "out",
    "own",
    "re",
    "s",
    "same",
    "she",
    "shes",
    "should",
    "shouldve",
    "so",
    "some",
    "such",
    "t",
    "than",
    "that",
    "thatll",
    "the",
    "their",
    "theirs",
    "them",
    "themselves",
    "then",
    "there",
    "these",
    "they",
    "this",
    "those",
    "through",
    "to",
    "too",
    "under",
    "until",
    "up",
    "ve",
    "very",
    "was",
    "we",
    "were",
    "what",
    "when",
    "where",
    "which",
    "while",
    "who",
    "whom",
    "why",
    "will",
    "with",
    "won",
    "y",
    "you",
    "youd",
    "youll",
    "youre",
    "youve",
    "your",
    "yours",
    "yourself",
    "yourselves",
]

stopwords_nltk = stopwords.words("english")
all_stopwords = list(set(stopwords_manual + stopwords_nltk))


def preprocess(text_data: list[str]) -> list[str]:
    """
    Preprocesses the given text data by replacing URLs,
    emojis, usernames, non-alphabetic characters, and
    consecutive letters. It also removes stopwords and
    lemmatizes the words before returning the processed text.

    Args:
        text_data (list[str]): The list of text data to be preprocessed.

    Returns:
        list[str]: The preprocessed text data.
    """
    processed_text = []

    # Defining regex patterns
    url_pattern = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)"
    user_pattern = r"@[^\s]+"
    alpha_pattern = r"[^a-zA-Z0-9]"
    sequence_pattern = r"(.)\1\1+"
    seq_replace_pattern = r"\1\1"

    for tweet in text_data:
        tweet = tweet.lower()

        # Replace all URls with 'URL'
        tweet = re.sub(url_pattern, " URL", tweet)
        # Replace all emojis
        for emoji in emojis:
            tweet = tweet.replace(emoji, "EMOJI" + emojis[emoji])
        # Replace @USERNAME to 'USER'
        tweet = re.sub(user_pattern, " USER", tweet)
        # Replace all non alphabets
        tweet = re.sub(alpha_pattern, " ", tweet)
        # Replace 3 or more consecutive letters by 2 letter
        tweet = re.sub(sequence_pattern, seq_replace_pattern, tweet)

        preprocessed_words = []
        for word in tweet.split():
            # Check if the word is a stopword
            if len(word) > 1 and word not in all_stopwords:
                # Lemmatizing the word
                word = lemmatizer.lemmatize(word)
                preprocessed_words.append(word)

        processed_text.append(" ".join(preprocessed_words))

    return processed_text


def predict(model, text: list[str]) -> list:
    """
    Predict the sentiment of the given text using the provided model.

    Args:
        model (object): The trained model for sentiment prediction.
        text (list[str]): The input list of text data for sentiment prediction.

    Returns:
        list: A list of tuples containing the input text, predicted sentiment,
        and the corresponding sentiment label.
    """
    # Predict the sentiment
    preprocessed_text = preprocess(text)
    predictions = model.predict(preprocessed_text)

    pred_to_label = {0: "Negative", 1: "Positive"}

    # Make a list of text with sentiment.
    data = []
    for t, pred in zip(text, predictions):
        data.append({"text": t, "pred": int(pred), "label": pred_to_label[pred]})

    return data


def predict_pipeline(text: list[str]) -> Callable:
    """
    Function to create a prediction pipeline using the given text as input.

    Args:
        text (list[str]): The input list of text data for prediction.

    Returns:
        Callable: A callable object for making predictions using the
        loaded pipeline.
    """
    return predict(loaded_pipe, text)


if __name__ == "__main__":
    # Text to classify should be in a list.
    text = [
        "I hate twitter",
        "May the Force be with you.",
        "Mr. Stark, I don't feel so good",
    ]

    predictions = predict_pipeline(text)
    print(predictions)
