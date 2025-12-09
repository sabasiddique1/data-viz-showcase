# Honey Production - Linear Regression
#
# Loads honey production data, fits a linear regression by year,
# and projects future production through 2050 with simple plots.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


def main():
    df = pd.read_csv(
        "https://content.codecademy.com/programs/data-science-path/linear_regression/honeyproduction.csv"
    )
    print(df.head())

    prod_per_year = df.groupby("year").totalprod.mean().reset_index()

    X = prod_per_year["year"].values.reshape(-1, 1)
    y = prod_per_year["totalprod"]

    plt.scatter(X, y)
    plt.xlabel("Year")
    plt.ylabel("Total Honey Production")
    plt.show()

    regr = LinearRegression()
    regr.fit(X, y)

    print("Slope:", regr.coef_)
    print("Intercept:", regr.intercept_)

    y_predict = regr.predict(X)
    plt.scatter(X, y)
    plt.plot(X, y_predict)
    plt.xlabel("Year")
    plt.ylabel("Total Honey Production")
    plt.show()

    X_future = np.array(range(2013, 2051)).reshape(-1, 1)
    future_predict = regr.predict(X_future)

    plt.plot(X_future, future_predict)
    plt.xlabel("Year")
    plt.ylabel("Predicted Honey Production")
    plt.show()

    print("Predicted honey production in 2050:", future_predict[-1])


if __name__ == "__main__":
    main()

