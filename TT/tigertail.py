"""
The main block for all of the classes and data loaders
maybe one day this will not live here altogether in
collective harmony.

The needs of the many outweight the needs of the few. ~ Spock
"""
import numpy as np
import pandas as pd
from collections.abc import MutableMapping

class TimeFrame(MutableMapping):
    '''
    Mapping that works like both a dict and a mutable object, i.e.
    d = D(foo='bar')
    and 
    d.foo returns 'bar'
    '''
    # ``__init__`` method required to create instance from class.
    def __init__(self, *args, **kwargs):
        '''Use the object dict'''
        self.__dict__.update(*args, **kwargs)

    # The next five methods are requirements of the ABC.
    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)
    
    def __len__(self):
        return len(self.__dict__)
    
    # The final two methods aren't required, but nice for demo purposes:
    def __str__(self):
        '''returns simple dict representation of the mapping'''
        return str(self.__dict__)
    
    def __repr__(self):
        '''echoes class, id, & reproducible representation in the REPL'''
        # TODO : remake this to print out the minimum window available
        #        to put all the data together
        return '{}, D({})'.format(super(D, self).__repr__(), 
                                  self.__dict__)

    def window(self, freq, fillnan=True):
        grouped_by = []
        for ts in self.__dict__:
            # print(ts.__class__)
            if freq.__class__ == EventSeries and self.__dict__[ts].__class__ == TimeSeries:
                grouped_by.append(self.__dict__[ts].nonstationary_window(es=freq, fillnan=True))
            elif freq.__class__ == EventSeries and self.__dict__[ts].__class__ == EventSeries:
                grouped_by.append(self.__dict__[ts].data)
            else:
                grouped_by.append(self.__dict__[ts].window(freq=freq, fillnan=True))
        
        # grouped_by = [self.__dict__[ts].window(freq=freq, fillnan=True) for ts in self.__dict__]
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
        if es.ns_window == None:
            es.calc_start_end()

        windowed_dfs = []
        windowed_df_index = []

        interval_mask = self.data.index <= es.ns_window[0][0]
        if fillnan == True:
            wndw_df = pd.DataFrame(self.data[interval_mask]).apply(self.agg_func).fillna(0)
            windowed_df_index.append(es.ns_window[0][1])
            windowed_dfs.append(wndw_df.to_frame())
        else:
            wndw_df = pd.DataFrame(self.data[interval_mask]).apply(self.agg_func)
            windowed_df_index.append(es.ns_window[0][1])
            windowed_dfs.append(wndw_df.to_frame())

        for interval in es.ns_window[1:]:
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
    def __init__(self, data, agg_func=None, ns_window=None):
        self.data = data
        self.agg_func = agg_func
        self.ns_window = ns_window

    def window(self, freq, fillnan=True):
        if fillnan == True:
            windowed_df = self.data.groupby(pd.Grouper(freq=freq)).apply(self.agg_func).fillna(0)
            windowed_df.columns = self.data.columns
            return windowed_df
        else:
            windowed_df = self.data.groupby(pd.Grouper(freq=freq)).apply(self.agg_func)
            windowed_df.columns = self.data.columns
            return windowed_df
        
    def calc_start_end(self):
        # sort dataframe by timestamp (assuming that index has timestamps)
        # deal with duplicate timestamps using list(set())
        timestamps = list(set(self.data.index.to_list()))
        timestamps.sort()
        start_end_intervals = []
        for i in range(0, len(timestamps)):
            if i + 1 < len(timestamps):
                start_end_intervals.append((timestamps[i], timestamps[i+1]))
        self.ns_window = start_end_intervals

if __name__ == '__main__':

    print('Hello there... ~obi-wan kenobi')

    