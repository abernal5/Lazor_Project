# -*- coding: utf-8 -*-
"""
EN.640.635 Software Carpentry
Lazor Project

@author: Alonso, Cam C., Cam G.
"""
import numpy as np
import matplotlib.pyplot as plt


class Function(object):
    '''
    This class serves as a wrapper for a lambda function.

    **Parameters**

        lam: *lambda function*
            The lambda function that describes the function being utilized.
    '''

    def __init__(self, lam):
        '''
        Initializes function.
        '''
        self.lam = lam

    def __call__(self, x):
        '''
        Given number x, solve function f(x).
        '''
        return self.lam(x)

    def __add__(self, other):
        '''
        If other is a number, add it to function such that:
        f(x) = f(x) + other.
        If other is another Function object, add it to the function such that:
        f(x) = f(x) + other(x)
        '''
        if type(other) == float or type(other) == int:
            return Function(lambda x: self.lam(x) + other)
        else:
            return Function(lambda x: self.lam(x) + other.lam(x))

    def __sub__(self, other):
        '''
        If other is a number, subtract it from the function such that:
        f(x) = f(x) - other.
        If other is another Function object, subtract it from the function
        such that:
        f(x) = f(x) - other(x)
        '''
        if type(other) == float or type(other) == int:
            return Function(lambda x: self.lam(x) - other)
        else:
            return Function(lambda x: self.lam(x) - other.lam(x))

    def __mul__(self, other):
        '''
        If other is a number, multiply it by the function such that:
        f(x) = f(x) * other.
        If other is another Function object, multiply it by the function
        such that:
        f(x) = f(x) * other(x)
        '''
        if type(other) == float or type(other) == int:
            return Function(lambda x: self.lam(x) * other)
        else:
            return Function(lambda x: self.lam(x) * other.lam(x))

    def __truediv__(self, other):
        '''
        If other is a number, divide the function by it such that:
        f(x) = f(x) / other.
        If other is another Function object, divide the function by it
        such that:
        f(x) = f(x) / other(x)
        '''
        if type(other) == float or type(other) == int:
            return Function(lambda x: self.lam(x) / other)
        else:
            return Function(lambda x: self.lam(x) / other.lam(x))


class Plotter(object):
    '''
    This class serves as a wrapper for Matplotlib's plot function.
    *Please note this function is not intended to handle two plots being
    created at once. Initialize and .plot the desired plot before
    beginning a second Plotter object.

    **Parameters**

        x_low: *int, float*
            The lowest (or most negative) value in the domain
        x_high: *int, float*
            The highest (or most positive) value in the domain
        x_step: *int, float*
            The size of the steps taken between x_low and x_high.
    '''

    def __init__(self, x_low, x_high, x_step):
        '''
        Initializes the plot.
        '''
        self.x_step = x_step
        self.x_low = x_low
        self.x_high = x_high

    def __call__(self):
        '''
        Allows user to simply run the self.plot command by writting self().
        This will use default names.
        '''
        return self.plot()

    def add_func(self, name, fun):
        '''
        Given a function name and a Function object, this adds the
        described function to the plot being created by this class.
        '''
        x = np.arange(self.x_low, self.x_high, self.x_step)
        # Uses Function call to create y values for domain given.
        y = fun(x)
        plt.plot(x, y, label=name)

    def plot(self, title_name='Functions', file_name='Function Plotter'):
        '''
        Runs Matplotlib's figure creation and saves it to the current folder.
        User also has the option of providing names for both the title of the
        plot and for the image file being saved.
        '''
        # Creating all the elements of the plot
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title(title_name)
        plt.axis([self.x_low, self.x_high, -200, 400])
        plt.legend()
        # Creating figure and saving it
        fig = plt.gcf()
        plt.show()
        fig.savefig(file_name + ".png")


if __name__ == "__main__":
    # For each Function object , we simply input the lambda function to it.
    # Note: be sure to include "import numpy as np" at the beginning of your
    # Python script so that we can make use of numpy’s sine function.
    f1 = Function(lambda x: x ** 2)
    f2 = Function(lambda x: x + 3)
    f3 = Function(lambda x: np.sin(x))
    # Combine our first 3 Function objects together to create a new fourth
    # Function object.
    f4 = (f1 + f2) * f3 / 2.0
    # Create a new Plotter object , where our domain ranges from 0 to 20 and we
    # have a step size of 0.1.
    plot = Plotter(0, 20, 0.1)
    # Add all the functions to the Plotter object. The first argument specifies
    # the function’s label and the second argument is the actual Function
    # object. Keep in mind that you must write the functions add func and plot.
    plot.add_func("Function 1", f1)
    plot.add_func("Function 2", f2)
    plot.add_func("Function 3", f3)
    plot.add_func("Function 4", f4)
    plot.plot()
