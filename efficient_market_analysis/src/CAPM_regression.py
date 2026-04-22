import statsmodels.api as sm 



def fit_ols(dataframe, outcome_var, independent_var):

    y = dataframe[outcome_var]
    x = dataframe[independent_var]
    x = sm.add_constant(x)  

    model = sm.OLS(y, x).fit()

    print(model.summary())
    return model