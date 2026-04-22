import numpy as np
import pandas as pd

'''

Get financial metrics to compare strategy performance: 
[Sharpe ratio, alpha, beta]

'''


def sharpe_ratio(excess_returns):

    sharpe_ratio = excess_returns.mean() / excess_returns.std()

    return sharpe_ratio


def beta(excess_returns, market_excess_returns):

    covariance = np.cov(excess_returns, market_excess_returns)[0][1]
    
    market_variance = np.var(market_excess_returns)

    return covariance / market_variance

def alpha(excess_returns, market_excess_returns):

    alpha = excess_returns.mean() - beta(excess_returns, market_excess_returns) * market_excess_returns.mean()

    return alpha

def cumulative_return(returns):
    
    cumulative = (1 + returns).prod() - 1

    return cumulative

def compare_strategies(dataframe, strategy_return_columns, market_excess_return_column):

    columns = list(strategy_return_columns) + [market_excess_return_column]

    strategy_returns = dataframe[columns]

    comparison_df = pd.DataFrame({

        'Strategy': strategy_returns.columns,
        'Sharpe Ratio': strategy_returns.apply(sharpe_ratio),
        'Beta': strategy_returns.apply(beta, market_excess_returns=strategy_returns[market_excess_return_column]),
        'Alpha': strategy_returns.apply(alpha, market_excess_returns=strategy_returns[market_excess_return_column]),
        'Cumulative Return': strategy_returns.apply(cumulative_return),

    })

    return comparison_df


