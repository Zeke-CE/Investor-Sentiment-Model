import numpy as np
import pandas as pd


def calculate_sentiment_signal(sentiment_scores, threshold=0):
    
    '''

    Generate trading signals based on sentiment scores.
    
    Parameters:
    - sentiment_scores: Series of sentiment scores.
    - threshold: Sentiment spread threshold before we take a side.
    
    Returns:
    - Series of sentiment signals: +1 = long, -1 = short, 0 = no position

    '''
    

    signal = np.select(
        [sentiment_scores > threshold, sentiment_scores < -threshold],
        [1, -1],
        default=0
    )
    
    return signal

'''

Example use:

signal = pd.Series([1, 0, -1, 0, 0, 1, -1]) #Signal must be 1, 0, or -1. 0s will be turned to NaN's to use with forward fill to represent the holding period not changing. So the signal data must be cleaned properly before passing in so 0s can be replaced accurately
returns = pd.Series([1, 1, 1, 1,1, 1,1]) #Returns must be aligned to represent forward returns corresponding to the signal at that time

print(calculate_return(signal, returns))

'''

def calculate_return(signal, returns, price=None, contrarian=False):
    
    '''

    Calculate strategy forward returns from signals and forward returns.
    
    Parameters:
    - signal: A pandas Series of trading signals (+1, -1, 0) (buy, short, hold: for the period).
    - returns: A pandas Series of returns (for the holding period of the signal data, default: weekly trading so weekly forward asset return).
    - price: Unused (meant for price based calculations).
    - contrarian: Indicated contrarian strategy where signals are inverted (performs better).
    
    Returns:
    - A pandas Series of strategy returns.

    '''



    #added these checks to ensure that strategy data isnt polluted
    if signal.isna().any():
        raise ValueError("Ensure Signal does not contain NaN values. Pass in cleaned signal and retruns series. They need to be aligned as needed before passing.")
    
    elif returns.isna().any():
        raise ValueError("Ensure Returns does not contain NaN values. Pass in cleaned signal and retruns series. They need to be aligned as needed before passing.")
    
    elif not signal.isin([-1, 0, 1]).all():
        raise ValueError("Signal must only contain -1, 0, or 1 values.")


    if contrarian:
        signal = -signal

    # Trading rule:
    # spread > threshold -> long (+1), spread < -threshold -> short (-1), -threshold < spread < threshold -> keep prior position.
    position = signal.replace(0, np.nan).ffill() #forward fill 0 with prior number (this should recreate strategy)
    strategy_returns = position * returns #Multiply the forward return time the position (signal) for that period

    return strategy_returns


def multiple_return(dataframe, signals, returns):

    results = {}

    for s, r in zip(signals, returns):

        

        results[s.split('_')[0]] = calculate_return(dataframe[s], dataframe[r], price=None, contrarian=False).fillna(0)

    return pd.DataFrame.from_dict(results)
