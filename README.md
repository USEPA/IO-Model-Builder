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

----------------------------------------------------------------------------------------

**Note** that `iomb` uses [NumPy](http://www.numpy.org/) for matrix computations
and there is currently no precompiled standard package available for 
[Windows 64 bit](https://pypi.python.org/pypi/numpy) which results in an error when
installing iomb. An easy solution is to download and install the precompiled NumPy 
package for Windows from http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy as described 
[here](http://stackoverflow.com/questions/28413824/installing-numpy-on-windows)
and run the installation of iomb after this:

```bash
    pip install "numpy-...-win_amd64.whl"
```

However, this seems not to work on all 
[Windows platforms](http://stackoverflow.com/questions/31025322/install-numpy-windows-8-64-with-python-3-5).

----------------------------------------------------------------------------------------

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


Data format
-----------
`iomb` processes simple CSV files in a specific format. The format of these 
files is described in the following sections. All CSV files should have the 
following properties:

* Commas (`,`) are used as column separators
* Character strings have to be enclosed in double quotes (`"`) if they contain 
  a comma or multiple lines. In other cases the quoting is optional.
* Numbers or boolean values (true, false) are never enclosed in quotes. The
  decimal separator is a point (`.`).
* Leading and trailing whitespaces are ignored
* The file encoding is UTF-8

### Format of satellite tables
Satellite tables are saved in a CSV file with the following columns:

0. Elementary flow name
1. CAS number of the flow
2. Flow category
3. Flow sub-category
4. Flow UUID
5. Process/Sector name
6. Process/Sector code
7. Process/Sector location
8. Amount
9. Unit
...

### Meta data files
Meta data files are used when the input-output model is converted to an JSON-LD
data package that can be imported into openLCA or the LCA Harmonization tool.
These files contain additional information about flows, processes, etc. and 
mappings to reference data like flow properties, locations, etc. Like all other
files, the meta data files are stored in a simple CSV format which is described
in the following.

### Meta-data files for elementary flows
A meta data file for elementary flows contains the following fields:

0. Name of the flow
1. Category of the flow
2. Sub-category of the flow
3. Unit of the flow
4. Flow direction (input/output)
5. UUID of the (mapped) flow
6. UUID of the flow property (e.g. UUID for mass)
7. UUID of the flows unit
8. Conversion factor ...

### Meta-data files for sectors/processes

0. Code
1. Name
2. Category
3. Sub-category
4. Location-Code
5. Location-UUID
...