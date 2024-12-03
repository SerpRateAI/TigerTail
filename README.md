# TigerTail

TigerTail is an event analysis library that helps analysts calculate non-stationary time windows prior to events of interest 
across multivariate time series data sets.

TigerTail implements three classes and attempts to follow `pandas`. These classes are the `TimeSeries`, `EventSeries`, and 
`TimeFrame`. The `TimeFrame` acts as a pandas-like dataframe except that each data dimension, or column, within the `TimeFrame` 
is allowed to have varying time-based indices. That means that you can store multiple time series with different sample rates, 
and different event occurences altogther and window across these together. Users can provide custom aggregation functions for 
windowing.

## install

```
pip install tigertail
```

## getting started

```
from TT import tdf

tdf = tdf.read_data('data_loc.csv')
tdf.window(5, 'seconds').plot()
```
![img](example_plot.png)
