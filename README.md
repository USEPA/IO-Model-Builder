iomb - input-output model builder
=================================
iomb is a package for creating, calculating, and converting environmentally 
extended input-output models. It processes [simple CSV files](#data-format) and can
create [JSON-LD data packages](https://github.com/GreenDelta/olca-schema) that can
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
information of the data format see the section [below](#data-format). 

### Logging
By default `iomb` logs only warnings and errors to the standard output. You can
configure the logging so that all logs are written:

```python
    import iomb
    iomb.log_all()
```

### Reading an input-output model
```python
    import iomb
    io_model = iomb.make_io_model('make_table.csv',
                                  'use_table.csv')
```

### Calculating a coefficients matrix
The `iomb` package can calculate a direct requirements coefficient matrix from
a given supply and use table as described in the 
[Concepts and Methods of the U.S. Input-Output Accounts, Chapter 12][1]:

[1]:http://www.bea.gov/papers/pdf/IOmanual_092906.pdf "Karen J. Horowitz, Mark A. Planting: Concepts and Methods of the U.S. Input-Output Accounts. 2006"

```python
    drc = io_model.get_dr_coefficients()
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
iomb processes simple CSV files in a defined format that is described in the 
following sections. In principle there are two types of files:
 
1. **Data files** mainly contain input and output amounts of economic 
   and environmental flows and information directly associated with these 
   amounts (like uncertainty or data quality). Entities in these files, like 
   sectors of flows, are identified by a combination of key attributes as
   described below. 
2. **Metadata files** contain additional information that further describes 
   the entities in the data files and provide mappings to reference data. Meta
   data files are not required when calculating and analyzing models with iomb
   but are used when creating JSON-LD data packages.
 
In addition to the format specifications below, all CSV files that are processed
with iomb should have the following properties:

* Commas (`,`) are used as column separators.
* Character strings have to be enclosed in double quotes (`"`) if they contain 
  a comma or multiple lines. In other cases the quoting is optional.
* Numbers or Boolean values (true, false) are never enclosed in quotes. The
  decimal separator is a point (`.`).
* Leading and trailing whitespaces are ignored.
* The file encoding is UTF-8.

### Identifiers
Entities like sectors, flows, impact categories etc. are not identified by 
artificial keys like [UUIDs](https://en.wikipedia.org/wiki/Universally_unique_identifier) 
in the CSV files but by a combination of key attributes of the respective 
entity as they are human readable. However, UUIDs are used in metadata files 
as they are required for generating JSON-LD packages. The key attributes are 
combined in a single string by removing leading and trailing whitespaces, 
setting the attributes to lower case, and joining them with a slash `/` as 
separator:

    [" Some key", "Attributes "] => "some key/attributes"

The `iomb.util` package provides a function `as_path` which exactly does this.
It also contains a function `make_uuid` which generates a hash-based UUID from
a set of attributes which are used in the JSON-LD packages when there is no
mapping to a UUID in a metadata file.

#### Sector identifiers
Input-output sectors are identified by the following attributes:

0. The sector code, e.g. `1111A0`
1. The sector name, e.g. `Oilseed farming`
2. The location code, e.g. `US`

The sector key of the example values would be:

    1111a0/oilseed farming/us

#### Flow indentifiers
Flows in the satellite tables are identified by the following
attributes:

0. The category / compartment, e.g. `air`
1. The sub-category / sub-compartment, e.g. `unspecified`
2. The name of the flow, e.g. `Carbon dioxide`
3. The unit of the flow, e.g. `kg`

Thus, the key of the example would be

    air/unspecified/carbon dioxide/kg

#### Impact category identifiers
Impact categories are identified by the following attributes

0. The name, e.g. `Climate change GWP 100`
1. The reference unit, e.g. `kg CO2 eq.`

The key of the example would be:

    climate change gwp 100/kg co2 eq.

### Data frames
The `iomb` package directly uses the [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html)
class of the [pandas framework](http://pandas.pydata.org/) for the input-output
tables and calculation results. The identifiers of input-output sectors, flows,
and impact categories as described above are directly used in the row and column
indices of the data frames. Thus the selection of a process contribution to an
impact category result could look like this:

```python
    result = ...
    result['climate change gwp 100/kg co2 eq.']['1111a0/oilseed farming/us']
``` 

The data frame class also directly provides a method for storing it as a CSV
file (`to_csv`) and 
[visualization functions](http://pandas.pydata.org/pandas-docs/stable/visualization.html).

### Data files

#### Input-output tables
The calculations in `iomb` as based on the direct requirements coefficients
matrix `A` of an input-output model but it also provides a method for 
calculating this coefficients matrix from raw supply and use tables as
provided by the [BEA](http://www.bea.gov/industry/io_annual.htm).

The format of these tables that `iomb` expects is just a table with numbers
with the industry and commodity [sector identifiers](#sector-identifiers) 
as row and column headers, e.g.:

```csv
                            1111a0/oilseed farming/us , 1111b0/grain farming/us , ...
1111a0/oilseed farming/us , 21.073                    , 0.0                     , ...
1111b0/grain farming/us   , 0.0                       , 54.738                  , ...
...                       , ...                       , ...                     , ...
```

#### Satellite tables
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