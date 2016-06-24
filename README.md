iomb - input-output model builder
=================================
iomb is a package for creating environmentally extended input-output models. 

Installation
------------
The installation of the package requires that [Python >= 3.4](https://docs.python.org/3/using/) 
is installed on your system. Unzip the source code and navigate via the command line to the 
source code folder:

```bash
    cd iomb
```

Then you can install it and its dependencies by creating an egg-link with pip:    
 
```bash
    pip install -e .
```

After this you should be able to use the `iomb` package in your Python script
files. If you want to use it in [Jupyter notebooks](http://jupyter.org/) you
have to install Jupyter too (via `pip install jupyter`). 

> (We plan to also publish this package on [PyPI](https://pypi.python.org/pypi)
>  when this is ready you will be able to install the package via
   `pip install iomb`)   

To uninstall the package run

```bash
    pip uninstall iomb
```

Usage
-----
If you have Python and the iomb package installed as described above you can use
at in plain Python scripts on your computer and execute it with the python command:

```bash
    python <your_script.py>
```

In the following examples the main functions of the `iomb` package are shown.


### Calculating the coefficients matrix from supply and use tables
The `iomb` package can calculate a direct requirements coefficient matrix from
a given supply and use table as described in the 
[Concepts and Methods of the U.S. Input-Output Accounts][1] (see Chapter 12).

[1]:http://www.bea.gov/papers/pdf/IOmanual_092906.pdf "Karen J. Horowitz, Mark A. Planting: Concepts and Methods of the U.S. Input-Output Accounts. 2006"

The following example shows how this works:

```python
# drc_example.py
import iomb

io_model = iomb.make_io_model('make_table.csv',
                              'use_table.csv')
drc = io_model.get_dr_coefficients()
drc.to_csv('drc.csv')
```