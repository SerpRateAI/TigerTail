"""
The TigerTail module contains the following classes:

- `TimeFrame` - Dict mapping to TimeSeries and EventSeries objects.
- `TimeSeries` - Wrapper for DataFrames of time series data.
- `EventSeries` - Wrapper for DataFrames of event series data.
"""

import numpy as np
import pandas as pd
from collections.abc import MutableMapping

class TimeFrame(MutableMapping):
    """
    The TimeFrame class follows the structure of a pandas DataFrame and is meant to contain TimeSeries and EventSeries objects. 
    It inherits from the MutableMapping class to be a mapping that works like both a dict and a mutable object, 
    i.e. d = D(foo='bar')
        d.foo returns 'bar'.

    Methods:
        __setitem__: Sets a key-value pair.
        __getitem__: Returns the value associated with a key.
        __delitem__: Deletes a key-value pair.
        __iter__: Returns an iterator based on self.__dict__
        __len__: Returns the length of the dict mapping.
        __str__: Returns a string representation of the dict mapping.
        __repr__: Returns a string containing the class, id, & reproducible representation in the REPL.
        window: Windows the data of each TimeSeries or EventSeries object in self.__dict__ according to the input frequency and 
                concatenates them into a single DataFrame.
    
    Attributes:
        N/A
    """
    # ``__init__`` method required to create instance from class.
    def __init__(self, *args, **kwargs):
        '''Use the object dict'''
        self.__dict__.update(*args, **kwargs)

    # The next five methods are requirements of the ABC.
    def __setitem__(self, key, value):
        """
        __setitem__ is used for setting a key-value pair for the TimeFrame dict.
        
        Args:
            key (str): String for the dict key.
            value: Value to pair with the key.
        
        Returns: N/A
        """
        self.__dict__[key] = value

    def __getitem__(self, key):
        """
        __getitem__ is used for getting the value associated with the inputted key from the TimeFrame dict.
        
        Args:
            key (str): String for the dict key.
        
        Returns: self.__dict__[key]
        """
        return self.__dict__[key]
    
    def __delitem__(self, key):
        """
        __delitem__ is used for deleting a key-value pair for the dict representation of the mapping.
        
        Args:
            key (str): String for the dict key.
        
        Returns: N/A
        """
        del self.__dict__[key]

    def __iter__(self):
        """
        __iter__ is used to generate an iterator using self.__dict__.
        
        Args: N/A
        
        Returns: Iterator object
        """
        return iter(self.__dict__)
    
    def __len__(self):
        """
        __len__ is used for getting the length of the dict representation of the mapping.
        
        Args: N/A
        
        Returns: The length of self.__dict__.
        """
        return len(self.__dict__)
    
    # The final two methods aren't required, but nice for demo purposes:
    def __str__(self):
        """
        __str__ returns a simple dict representation of the mapping.
        
        Args: N/A
        
        Returns: String version of self.__dict__.
        """
        return str(self.__dict__)
    
    def __repr__(self):
        """
        __repr__ returns a string containing the class, id, & reproducible representation in the REPL.
        
        Args: N/A
        
        Returns: String containing the class, id, & reproducible representation in the REPL.
        """
        # TODO : remake this to print out the minimum window available
        #        to put all the data together
        return '{}, D({})'.format(super(D, self).__repr__(), 
                                  self.__dict__)

    def window(self, freq, fillnan=True):
        """
        The window function windows all the time and event series data stored in the object according to either a certain uniform time or event timestamps. It first calls the window function of each 
        TimeSeries or EventSeries object. It then concatenates all of the returned windowed DataFrames together.
        
        Args:
            freq (str or EventSeries): Either a string representing the uniform length of time to window by (i.e. '1h' for one hour), or an EventSeries object containing the data to be used for windowing.
                                        See here for list of default frequencies: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
            fillnan (bool, default True): Determines whether NaN values in the result DataFrame are replaced by 0s.
        
        Returns:
            windowed_df: A DataFrame of the concatenated windowed data.
        """
        grouped_by = []
        for ts in self.__dict__:
            if freq.__class__ == EventSeries and self.__dict__[ts].__class__ == TimeSeries:
                grouped_by.append(self.__dict__[ts].nonstationary_window(es=freq, fillnan=True))
            elif freq.__class__ == EventSeries and self.__dict__[ts].__class__ == EventSeries:
                grouped_by.append(self.__dict__[ts].data)
            else:
                grouped_by.append(self.__dict__[ts].window(freq=freq, fillnan=True))
        
        names = sum([[col for col in self.__dict__[ts].data.columns] for ts in self.__dict__], [])
        
        if fillnan == True:
            windowed_df = pd.concat(grouped_by, axis=1).fillna(0)
            windowed_df.columns = names
            return windowed_df
        else:
            windowed_df = pd.concat(grouped_by, axis=1)
            windowed_df.columns = names
            return windowed_df
    
class TimeSeries:
    """
    The TimeSeries class provides a wrapper for a pandas DataFrame of time series data. The class 
    functions allow the time series data to be windowed according to uniform periods of time (frequencies) or event timestamps 
    (nonstationary windowing).
    
    Methods:
        window: Uses groupby to group the data by the input frequency and applies the aggregation function to each group.
        nonstationary_window: Groups the data using the timestamps of the inputted EventSeries data and
                            applies the aggregation function to each group.
    
    Attributes:
        data (pandas DataFrame): pandas DataFrame containing time series data.
        agg_func (numpy method): The aggregation function to be used when windowing the data.
    """
    def __init__(self, data, agg_func=None):
        self.data = data
        self.agg_func = agg_func

    def __add__(self, other):
        if isinstance(other, TimeSeries):
            ts1 = TimeSeries(self.data, self.agg_func)
            ts2 = other
            tf = TimeFrame(ts1) + TimeFrame(ts2)
            return tf
        else:
            raise ValueError('You can only add TimeSeries objects to TimeSeries objects.')

    def window(self, freq, fillnan=True):
        """
        The window function uses groupby (from pandas) to group the data by the input frequency and applies 
        the aggregation function (the class agg_func attribute) to each group.
        
        Args:
            freq (str): The uniform length of time to window by. For example, '1h' for one hour.
                        See here for list of default frequencies: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
            fillnan (bool, default True): Determines whether NaN values in the resulting are replaced by 0s.
        
        Returns:
            windowed_df (DataFrame): A DataFrame of the windowed data.
        """
        if fillnan == True:
            windowed_df = self.data.groupby(pd.Grouper(freq=freq)).apply(self.agg_func).fillna(0)
            windowed_df.columns = self.data.columns
            return windowed_df
        else:
            windowed_df = self.data.groupby(pd.Grouper(freq=freq)).apply(self.agg_func)
            windowed_df.columns = self.data.columns
            return windowed_df

    def apply(self):
        raise NotImplementedError('TODO!')
    
    def nonstationary_window(self, es, fillnan=True):
        """
        The nonstationary window function groups the data by the time intervals between events from an EventSeries object and applies 
        the aggregation function (the class agg_func attribute) to each group.
        
        Args:
            es (EventSeries): The EventSeries object that contains the event data to use for windowing.
            fillnan (bool, default True): Determines whether NaN values in the result DataFrame are replaced by 0s.
        
        Returns:
            ns_window_result_df (DataFrame): A DataFrame of the nonstationary windowed data.
        """
        if es.ns_window == None:
            es.calc_start_end()
        
        if len(es.ns_window) == 1 and isinstance(es.ns_window[0], tuple) == False:
            interval_mask = self.data.index <= es.ns_window[0]
            if fillnan == True:
                wndw_df = pd.DataFrame(self.data[interval_mask]).apply(self.agg_func).fillna(0).to_frame()
                wndw_df.index = es.ns_window
                wndw_df.columns = self.data.columns
            else:
                wndw_df = pd.DataFrame(self.data[interval_mask]).apply(self.agg_func).to_frame()
                wndw_df.index = es.ns_window
                wndw_df.columns = self.data.columns
            return wndw_df

        else:
            windowed_dfs = []
            windowed_df_index = []

            interval_mask = self.data.index <= es.ns_window[0][0]
            if fillnan == True:
                wndw_df = pd.DataFrame(self.data[interval_mask]).apply(self.agg_func).fillna(0)
                windowed_df_index.append(es.ns_window[0][0])
                windowed_dfs.append(wndw_df.to_frame())
            else:
                wndw_df = pd.DataFrame(self.data[interval_mask]).apply(self.agg_func)
                windowed_df_index.append(es.ns_window[0][1])
                windowed_dfs.append(wndw_df.to_frame())

            for interval in es.ns_window:
                interval_mask = (self.data.index > interval[0]) & (self.data.index <= interval[1])
                if fillnan == True:
                    wndw_df = pd.DataFrame(self.data[interval_mask]).apply(self.agg_func).fillna(0)
                    windowed_df_index.append(interval[1])
                    windowed_dfs.append(wndw_df.to_frame())
                else:
                    wndw_df = pd.DataFrame(self.data[interval_mask]).apply(self.agg_func)
                    windowed_df_index.append(interval[1])
                    windowed_dfs.append(wndw_df.to_frame())

            ns_window_result_df = pd.concat(windowed_dfs, ignore_index=True)
            ns_window_result_df.index = windowed_df_index
            ns_window_result_df.columns = self.data.columns
            return ns_window_result_df


class EventSeries:
    """
    The EventSeries class provides a wrapper for a pandas DataFrame of event data. The class 
    functions allow the event series data to be windowed according to uniform periods of time (frequencies).
    
    Methods:
        window: Uses groupby to group the data by the input frequency and applies the aggregation function to each group.
        calc_start_end: Calculates a list of tuples of the start and end timestamps between events and assigns it to 
                        self.ns_window.
    
    Attributes:
        data (pandas DataFrame): pandas DataFrame containing event data.
        agg_func (numpy method): The numpy aggregation function to be used when windowing the data.
        ns_window (list): Contains a list of the intervals between events calculated by calc_start_end().
    """
    def __init__(self, data, agg_func=None, ns_window=None):
        self.data = data
        self.agg_func = agg_func
        self.ns_window = ns_window

    def window(self, freq, fillnan=True):
        """
        The window function uses groupby (from pandas) to group the data by the input frequency and applies 
        the aggregation function (the class agg_func attribute) to each group.
        
        Args:
            freq (str): The length of the time. For example, '1h' for one hour.
                        See here for list of default frequencies: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
            fillnan (bool, default True): Determines whether NaN values in the resulting are replaced by 0s.
        
        Returns:
            windowed_df: A DataFrame of the windowed data.
        """
        if fillnan == True:
            windowed_df = self.data.groupby(pd.Grouper(freq=freq)).apply(self.agg_func).fillna(0)
            windowed_df.columns = self.data.columns
            return windowed_df
        else:
            windowed_df = self.data.groupby(pd.Grouper(freq=freq)).apply(self.agg_func)
            windowed_df.columns = self.data.columns
            return windowed_df
        
    def calc_start_end(self):
        """
        The calc_start_end function calculates the time intervals between events. It sets self.ns_window
        to be the resulting list of tuples of start and end times between events.
        
        Args: N/A
        Returns: N/A
        """
        # sort dataframe by timestamp (assuming that index has timestamps)
        # deal with duplicate timestamps using list(set())
        timestamps = list(set(self.data.index.to_list()))
        timestamps.sort()

        # handle a list of just one timestamp
        if len(timestamps) == 1:
            self.ns_window = timestamps
        else:
            start_end_intervals = []
            for i in range(0, len(timestamps)):
                if i + 1 < len(timestamps):
                    start_end_intervals.append((timestamps[i], timestamps[i+1]))
            self.ns_window = start_end_intervals

if __name__ == '__main__':

    print('Hello there... ~obi-wan kenobi')

    