"""
The main block for all of the classes and data loaders
maybe one day this will not live here altogether in
collective harmony.

The needs of the many outweight the needs of the few. ~ Spock
"""
import numpy as np
import pandas as pd


class TimeSeries:
    """
    A data container for a regularly spaced time series
    """
    def __init__(self, data, agg_func):
        self.data = data
        self.default_agg_func = agg_func

    def __call__(self):
        """
        Returns the time series as the raw data set
        """
        return self.data

    def window(self, rate, unit):
        """
        Creates a custom windowing function

        Args:
            rate (int): the number increments to increase the window unit by
            unit (str): the time unit to increase the window by.

            available units: sec, min, hour, day, month, year, custom_datetime

        Returns:
            returns the TimeSeries object windowed across the TimeIndex using the
            built in aggregate function
        """
        from datetime import datetime
        start = datetime(self.data.index.min())
        end = datetime(self.data.index.max())
        diff = end - start
        
        periods = 
        ts_index = pd.date_range(start=self.data.index.min(), end=self.data.index.max(), periods=rate

    def apply(self, func):
        """
        applies a custom aggregate function instead of the existing aggregate function

        Args:
            func (function): function to be applied
            
        Returns:
            returns a TimeSeries object reduced with the current function applied
        """
        pass

def load_csv(file_loc, agg_func):
    """
    loads a time series from a CSV

    Args:
        file_loc (str): location of data file
        agg_func (function): function to make default aggregation

    Returns:
        TimeSeries (object): time series object
    """
    data_frame
        

if __name__ == '__main__':

    ts = load_csv('~/data/sinusoidal.csv', agg_func=np.mean)
    print(ts().head())
    print(ts().tail())
    print(ts.window(5, 'min').head())
    print(ts
    print(ts.apply(lambda x: 0 if x < 0 else np.max(x)))
