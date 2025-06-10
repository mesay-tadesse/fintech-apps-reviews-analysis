import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import pandas as pd
from typing import Optional

sns.set(style="whitegrid")

def plot_sentiment_trends(df: pd.DataFrame, date_col: str = 'date', sentiment_col: str = 'sentiment', bank_col: str = 'bank'):
    """
    Plot sentiment trends over time for each bank.
    """
    df[date_col] = pd.to_datetime(df[date_col])
    trend = df.groupby([bank_col, pd.Grouper(key=date_col, freq='M')])[sentiment_col].value_counts().unstack().fillna(0)
    for bank in df[bank_col].unique():
        trend.loc[bank].plot(kind='line', title=f'Sentiment Trend for {bank}')
        plt.xlabel('Month')
        plt.ylabel('Count')
        plt.legend(title='Sentiment')
        plt.show()