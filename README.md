iomb - input-output model builder
=================================
iomb is a Python package for creating, calculating, and converting 
environmentally extended input-output models. It processes CSV files in a simple 
[data format](doc/data_format.md) to create and calculate input-output models.
Such models can then be also converted into a [JSON-LD data package](https://github.com/GreenDelta/olca-schema) that can
be imported into [openLCA](http://openlca.org).

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
In this case, on option would be to just use the 32bit version of Python 
(because for this a pre-compiled version of NumPy is available).

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
The following examples show what you can do with the `iomb` package. For detailed
information of the data format see the sections [below](#data-format). 

### Logging
By default `iomb` logs only warnings and errors to the standard output. You can
configure the logging so that all logs are written:

```python
import iomb
iomb.log_all()
```

### Reading a model and calculate results
```python
import iomb
model = iomb.make_model('drc.csv',  # the coefficients matrix
                        ['sat_table1.csv', 'sat_table1.csv'],  # satellite tables
                        'sector_meta_data.csv')  # sector meta data
result = iomb.calculate(model, {'1111a0/oilseed farming/us': 1})
print(result.total_result)
```

### Calculating a coefficients matrix
The `iomb` package can calculate a direct requirements coefficient matrix from
a given supply and use table as described in the 
[Concepts and Methods of the U.S. Input-Output Accounts, Chapter 12][1]:

[1]:http://www.bea.gov/papers/pdf/IOmanual_092906.pdf "Karen J. Horowitz, Mark A. Planting: Concepts and Methods of the U.S. Input-Output Accounts. 2006"

```python
import iomb
drc = iomb.coefficients_from_sut('supply_table.csv', 'use_table_2007.csv')
drc.to_csv('drc.csv')
```

### Using result data frames
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
import iomb
io_model = iomb.make_io_model('make_table.csv',
                              'use_table.csv')
# visual check of the totals in the make and use tables
io_model.viz_totals()
# visual shape of the make and use tables
io_model.viz_make_table()
io_model.viz_use_table()
```

### Reading satellite tables
A satellite table can be created from a set of CSV files (see the format
specification [below](#satellite-tables):

```python
import iomb
sat_table = iomb.make_sat_table('sat_file1.csv',
                                'sat_file2.csv',
                                'sat_file3.csv')
```

### Creating a JSON-LD data package
TODO: doc
