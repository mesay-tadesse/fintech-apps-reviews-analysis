import pandas as pd
from collections import Counter
from typing import Tuple, List, Dict

def note_biases(df: pd.DataFrame, sentiment_col: str = 'sentiment', rating_col: str = 'rating') -> str:
    """
    Identify and note potential review biases in the dataset.
    """
    n_reviews = len(df)
    n_neg = (df[sentiment_col] == 'negative').sum()
    n_pos = (df[sentiment_col] == 'positive').sum()
    neg_ratio = n_neg / n_reviews if n_reviews else 0
    pos_ratio = n_pos / n_reviews if n_reviews else 0
    bias_note = (
        f"Out of {n_reviews} reviews, {n_neg} are negative ({neg_ratio:.1%}), "
        f"{n_pos} are positive ({pos_ratio:.1%}). "
    )
    if neg_ratio > 0.6:
        bias_note += "There is a notable negative skew, which may indicate review bias (e.g., dissatisfied customers more likely to leave feedback).\n"
    if pos_ratio > 0.6:
        bias_note += "There is a notable positive skew, which may indicate review bias (e.g., incentivized or solicited positive reviews).\n"
    bias_note += "Consider these biases when interpreting insights and recommendations."
    return bias_note


def extract_drivers_painpoints(df: pd.DataFrame, sentiment_col: str = 'sentiment', text_col: str = 'review_text', bank_col: str = 'bank', keywords_col: str = 'keywords') -> Dict[str, Dict[str, List[str]]]:
    """
    Identify top drivers and pain points for each bank based on sentiment and keywords.
    Returns a dictionary: {bank: {'drivers': [...], 'painpoints': [...]}}
    """
    results = {}
    for bank in df[bank_col].unique():
        bank_df = df[df[bank_col] == bank]
        # Drivers: Top keywords/themes in positive reviews
        pos_keywords = bank_df[bank_df[sentiment_col] == 'positive'][keywords_col].sum()
        drivers = [kw for kw, _ in Counter(pos_keywords).most_common(3)]
        # Pain points: Top keywords/themes in negative reviews
        neg_keywords = bank_df[bank_df[sentiment_col] == 'negative'][keywords_col].sum()
        painpoints = [kw for kw, _ in Counter(neg_keywords).most_common(3)]
        results[bank] = {'drivers': drivers, 'painpoints': painpoints}
    return results

def compare_banks(df: pd.DataFrame, bank_col: str = 'bank', sentiment_col: str = 'sentiment') -> pd.DataFrame:
    """
    Compare banks by sentiment counts and return a summary DataFrame.
    """
    return df.groupby([bank_col, sentiment_col]).size().unstack(fill_value=0)