import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def plot_returns(dataframe, returns, ax):
    plt.figure(figsize=(12,6))


    cummulative_return = (1+ dataframe[returns]).cumprod() - 1

    sns.lineplot(data=dataframe, x='Date', y=cummulative_return, label= returns, ax=ax)



    return ax



def plot_correlation_matrix(dataframe, columns, ax):
    
    correlation_matrix = dataframe[columns].corr(method='pearson')

    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)

    ax.set_title('Correlation Matrix of Sentiment and S&P 500 Metrics')

    return ax

    
  


def plot_regression(dataframe, model, outcome, independent, ax):

    plot_df = dataframe.dropna()

    sns.scatterplot(data=plot_df, x=independent, y=outcome, ax = ax, hue='Signal', alpha=0.8)

    x_sorted = np.sort(plot_df[independent].to_numpy())
    
    y_fit = model.params['const'] + model.params[independent] * x_sorted
    
    ax.plot(x_sorted, y_fit, color='red', label='OLS Fit')

    ax.set_title(f'CAPM Regression on {outcome}')

    ax.set_xlabel(independent)
    ax.set_ylabel(outcome)

    ax.legend()

    return ax