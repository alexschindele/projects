import matplotlib
import os

import numpy as np
from scipy import stats
from scipy.interpolate import UnivariateSpline
from numpy import polyfit
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from statsmodels.graphics.regressionplots import plot_fit
import pylab

def import_files():
    fpath1 = r'C:\Users\alexschindele\Documents\COS 424 Machine Learning\hw1_sample1_train.txt'
    fpath2 = r'C:\Users\alexschindele\Documents\COS 424 Machine Learning\hw1_sample2_train.txt'

    with open(fpath1) as file:
        data = file.readlines()

    x = [float(x.split('\t')[0].strip()) for x in data]
    y = [float(x.split('\t')[1].strip()) for x in data]
    return x, y


# use the statsmodels package to graph (not as good as numpy/scipy)
def regression_statsmodels(x, y):

    model = sm.OLS(x, y)

    results = model.fit()
    # print(results.summary())
    plot_fit(results, 0)


# the classic matplotlib plot
def plot(x, y):
    fig, ax = plt.subplots(figsize=(8,6))

    ax.plot(x, y, 'o', label="data")


# different kinds of regression using numpy/scipy
def regression_numpy(x, y, regression_type = 'linear'):
    x_cont = np.arange(min(x), max(x), 0.2)
    if regression_type == 'linear':
        slope, intercept, r_value, p_value, std_error = stats.linregress(x, y)
        line_func = lambda x_null : x_null * slope + intercept
        plt.figure(1)
        plt.plot(x_cont, line_func(x_cont), 'b', x, y, 'ro')
    if regression_type == 'cubic':
        fit = np.polyfit(x, y, deg=3)
        fit = np.poly1d(fit)
        plt.figure(1)
        plt.plot(x_cont, fit(x_cont), 'b', x, y, 'ro')
    if regression_type == 'cubic spline':
        spline = UnivariateSpline(x, y, s=1)
        plt.figure(1)
        plt.plot(x_cont, spline(x_cont), 'b', x, y, 'ro')

def main():
    x,y =import_files()
    # regression_statsmodels(x, y)
    regression_numpy(x, y, 'cubic spline')
    pylab.show()


if __name__ == '__main__':
    main()