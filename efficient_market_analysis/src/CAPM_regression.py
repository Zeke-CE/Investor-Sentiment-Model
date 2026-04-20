import statsmodels.api as sm #(change to the version from jacob (gmail))



def fit_ols(dataframe, outcome_var, independent_var):
    y = dataframe[outcome_var]
    x = dataframe[independent_var]
    x = sm.add_constant(x)  

    model = sm.OLS(y, x).fit()

    print(model.summary())
    return model