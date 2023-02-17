from string import punctuation
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from joblib import Parallel, delayed
import re


def clear_text(text):
    """
    Helper function to clean text
    """
    lemmatizer = WordNetLemmatizer()
    text = str(text)
    text = re.sub(r"https?://[^,\s]+,?", "", text)
    text = re.sub(r"@[^,\s]+,?", "", text)

    stop_words = stopwords.words("english")
    transform_text = text.translate(str.maketrans("", "", punctuation))
    transform_text = re.sub(" +", " ", transform_text)

    text_tokens = word_tokenize(transform_text)

    lemma_text = [
        lemmatizer.lemmatize(word.lower()) for word in text_tokens
    ]
    cleaned_text = " ".join(
        [str(word) for word in lemma_text if word not in stop_words]
    )
    return cleaned_text


def clear_data(source_path: str, target_path: str, n_jobs: int):
    """Baseline process df

    Parameters
    ----------
    source_path : str
        Path to load dataframe from

    target_path : str
        Path to save dataframe to
        :param source_path:
        :param target_path:
        :param n_jobs:
    """
    data = pd.read_parquet(source_path)
    data = data.copy().dropna().reset_index(drop=True)
    clear_text_result = Parallel(n_jobs=n_jobs, backend="multiprocessing")(
        delayed(clear_text)(text) for text in data["text"]
    )
    data["cleaned_text"] = clear_text_result
    data.to_parquet(target_path)
