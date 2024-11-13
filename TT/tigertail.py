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
        grouped_by = [self.__dict__[ts].window(freq=freq, fillnan=True) for ts in self.__dict__]
        names = [self.__dict__[ts].data.columns[0] for ts in self.__dict__]
        if fillnan == True:
            return pd.concat(grouped_by, axis=1, keys=names).fillna(0)
        else:
            return pd.concat(grouped_by, axis=1, keys=names)
    
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
            return self.data.groupby(pd.Grouper(freq=freq)).apply(self.agg_func).fillna(0)
        else:
            return self.data.groupby(pd.Grouper(freq=freq)).apply(self.agg_func)

    def apply(self):
        raise NotImplementedError('TODO!')

class EventSeries:
    def __init__(self, data, agg_func=None):
        self.data = data
        self.agg_func = agg_func

    def window(self, freq, fillnan=True):
        if fillnan == True:
            return self.data.groupby(pd.Grouper(freq=freq)).apply(self.agg_func).fillna(0)
        else:
            return self.data.groupby(pd.Grouper(freq=freq)).apply(self.agg_func)

if __name__ == '__main__':

    print('Hello there... ~obi-wan kenobi')

    