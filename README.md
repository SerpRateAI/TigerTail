# TigerTail
a time series analytics library

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
