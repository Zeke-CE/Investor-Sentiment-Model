import numpy as np
import pandas as pd
import warnings


def calculate_sentiment_signal(sentiment_scores, threshold=0):
    
    '''
    Generate trading signals based on sentiment scores.
    
    Parameters:
    - sentiment_scores: A pandas Series of sentiment scores.
    - threshold: A float value above which we take a long position, and below which we take a short position.
    
    Returns:
    - A pandas Series of trading signals: +1 for long, -1 for short, and 0 for no position.
    '''
    
    # +1 = long, -1 = short, 0 = no position
    signal = np.select(
        [sentiment_scores > threshold, sentiment_scores < -threshold],
        [1, -1],
        default=0
    )
    
    return signal

def calculate_return(signal, returns, price=None, holding_period='6M'):
    
    '''
    Calculate strategy returns from sentiment signals and forward returns.
    
    Parameters:
    - signal: A pandas Series of trading signals (+1, -1, 0).
    - returns: A pandas Series of asset returns for the evaluation horizon.
    - price: Unused (kept for backwards compatibility).
    - holding_period: Included for API compatibility.
    
    Returns:
    - A pandas Series of strategy returns.
    '''

    if holding_period not in {'6M', '1M', '1W'}:
        raise ValueError("Invalid holding period. Use '6M', '1M', or '1W'.")

    signal_series = pd.Series(signal, copy=False)
    returns_series = pd.Series(returns, copy=False)

    # Align on a common index.
    aligned = pd.concat([signal_series, returns_series], axis=1)
    aligned.columns = ['signal', 'returns']

    non_null_signal = aligned['signal'].dropna()
    if not non_null_signal.isin([-1, 0, 1]).all():
        raise ValueError("Signal must only contain -1, 0, or 1 values.")

    if aligned[['signal', 'returns']].isna().any().any():
        warnings.warn("NaN detected in signal/returns; using flat signal for missing signal and preserving NaN returns.", RuntimeWarning, stacklevel=2)
    aligned['returns'] = pd.to_numeric(aligned['returns'], errors='coerce')
    signal_clean = aligned['signal'].fillna(0.0)

    # Trading rule:
    # spread > 0 -> long (+1), spread < 0 -> short (-1), spread == 0 -> keep prior position.
    position = signal_clean.replace(0, np.nan).ffill().fillna(0.0)
    strategy_returns = position * aligned['returns']

    return strategy_returns