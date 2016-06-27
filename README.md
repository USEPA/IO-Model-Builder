iomb - input-output model builder
=================================
iomb is a package for creating, calculating, and converting environmentally 
extended input-output models. 

Installation
------------
The installation of the package requires that [Python >= 3.4](https://docs.python.org/3/using/) 
is installed on your system. Unzip the source code and navigate via the command 
line to the source code folder:

```bash
    cd iomb
```

Then you can install it and its dependencies by creating an egg-link with pip:    
 
```bash
    pip install -e .
```

After this you should be able to use the `iomb` package in your Python scripts.
If you want to use it in [Jupyter notebooks](http://jupyter.org/) you have to 
install Jupyter too (via `pip install jupyter`). 

> (We plan to also publish this package on [PyPI](https://pypi.python.org/pypi)
>  when this is ready you will be able to install the package via
   `pip install iomb`)   

To uninstall the package run

```bash
    pip uninstall iomb
```

Usage
-----

### Logging
By default `iomb` logs only warnings and errors to the standard output. You can
configure the logging so that all logs are written:

```python
    import iomb
    iomb.log_all()
```

### Reading an input-output model
`iomb` currently supports the creation of input-output models from supply and
use tables. These tables are read as [pandas data frames](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html)
where sectors are identified by a combination of the following attributes in
lower case:

```
    <sector code>/<sector name>/<location code>
    e.g. 1111a0/oilseed farming/us
```

The `make_io_model` function creates an input-output model:

```python
    import iomb
    io_model = iomb.make_io_model('make_table.csv',
                                  'use_table.csv')
```

### Calculating the coefficients matrix
The `iomb` package can calculate a direct requirements coefficient matrix from
a given supply and use table as described in the 
[Concepts and Methods of the U.S. Input-Output Accounts, Chapter 12][1]:

[1]:http://www.bea.gov/papers/pdf/IOmanual_092906.pdf "Karen J. Horowitz, Mark A. Planting: Concepts and Methods of the U.S. Input-Output Accounts. 2006"

```python
    drc = io_model.get_dr_coefficients()
```

The intermediate tables for this calculation can be also directly retrieved 
from the IO model (e.g. via `get_market_shares`, `get_transformation_matrix`, 
`get_direct_requirements`, etc.).

The `iomb` package directly uses the [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html)
class of the [pandas framework](http://pandas.pydata.org/) for the input-output
tables and calculation results. Thus, it is possible to directly write result
tables to a CSV file or to create a chart using the 
[pandas visualization functions](http://pandas.pydata.org/pandas-docs/stable/visualization.html)

```python
    # save as CSV file
    drc.to_csv('drc.csv') 
    
    # creating a histogram
    import matplotlib.pyplot as plt
    drc['1111a0/oilseed farming/us-ga'].plot.hist()
    plt.show()    
```

### More visualization functions
The `iomb` model types often provide some specific visualization functions that 
start with a prefix `viz_`:


```python
    io_model = iomb.make_io_model('make_table.csv',
                                  'use_table.csv')
    
    # visual check of the totals in the make and use tables
    io_model.viz_totals()
    # visual shape of the make and use tables
    io_model.viz_make_table()
    io_model.viz_use_table()
```

### Reading satellite tables
A satellite table can be created from a set of CSV files with a defined format (
TODO: link to format spec.).

```python
    sat_table = iomb.make_sat_table('sat_file1.csv', 
                                    'sat_file2.csv', 
                                    'sat_file3.csv')
```

### Calculation
TODO: doc

```python

    demand = {'1111a0/oilseed farming/us': 42.0,
              '112300/poultry and egg production/us': 24.0}
    iomb.calculate(io_model, sat_table, demand)    
```

### Creating a JSON-LD data package
TODO: doc

