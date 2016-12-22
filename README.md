iomb - Input-Output Model Builder
=================================
`iomb` is an open source Python library for creating environmentally extended input-output
models (EEIO models) from CSV files in a simple [data format](doc/data_format.md).
It includes functions to calculate different result types (e.g. life cycle 
assessment results, direct and upstream contributions, etc.) from such models
and convert them into [JSON-LD data packages](https://github.com/GreenDelta/olca-schema) 
that can be imported into [openLCA](http://openlca.org).

Installation
------------
`iomb` is tested with [Python 3.5](https://docs.python.org/3/) but should
also work with older versions of Python 3. The easiest way to install the 
package is currently to [download the source code](https://github.com/USEPA/IO-Model-Builder/archive/master.zip),
extract it to a folder, and create an 
['egg-link' with pip](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs) 
from the command line:

```
pip install -e C:\path\to\iomb
```

This will also install the dependencies of `iomb` ([NumPy](http://www.numpy.org/), 
[pandas](http://pandas.pydata.org/), and [matplotlib](http://matplotlib.org/))
if required. After this you should be able to use the `iomb` package in your
Python code. To uninstall the package, you can again use pip from the command
line: 

```
pip uninstall iomb
```

Usage
-----
You can find a more detailed [example here](example/example.ipynb) in form of a 
[Jupyter notebook](http://jupyter.org/) which is a convenient way to use `iomb`.
The following script shows the basic usage of `iomb`. For detailed information 
about the data format see the [data format specification](doc/data_format.md)


```python
import iomb

# optionally show all logging information of iomb
iomb.log_all()

# create a direct requirements coefficients matrix from a supply and use table
# and save it to a CSV file
drc = iomb.coefficients_from_sut('supply_table.csv', 'use_table.csv')
drc.to_csv('drc.csv')

# create an EEIO model from a coefficients matrix, satellite tables, and a
# LCIA method
model = iomb.make_model('drc.csv',
                        ['satellite_table1.csv', 'satellite_table2.csv'],
                        "sector_meta_data.csv",
                        ['LCIA_factors1.csv', 'LCIA_factors1.csv'])

# validate the model
import iomb.validation as val
vr = validation.validate(model)
print(vr)

# calculate results for a given demand
result = iomb.calculate(model, {'1111a0/oilseed farming/us': 1})
print(result.total_result)

# export the model to a JSON-LD package
import iomb.olca as olca
olca.Export(model).to('model_as_json-ld.zip')

```

## License
This work is licensed under a [Creative Commons Attribution-NonCommercial 3.0 Unported License](https://creativecommons.org/licenses/by-nc/3.0/deed.en_US).

![Creative Commons License](https://i.creativecommons.org/l/by-nc/3.0/88x31.png)
