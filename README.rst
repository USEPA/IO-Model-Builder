iomb - Input-Output Model Builder
=================================

``iomb`` is an open source Python library for creating environmentally
extended input-output models (EEIO models) from CSV files in a simple
`data format <doc/data_format.md>`__. It includes functions to calculate
different result types (e.g. life cycle assessment results, direct and
upstream contributions, etc.) from such models and convert them into
`JSON-LD data packages <https://github.com/GreenDelta/olca-schema>`__
that can be imported into `openLCA <http://openlca.org>`__.

Installation
------------

``iomb`` is tested with `Python 3.5 <https://docs.python.org/3/>`__ but
should also work with older versions of Python 3. The easiest way to
install the package is to do so using pip, which is generally
packaged with a Python installation. Open up the command line and enter:

::

    pip install iomb

This will also install the dependencies of ``iomb``
(`NumPy <http://www.numpy.org/>`__,
`pandas <http://pandas.pydata.org/>`__, and
`matplotlib <http://matplotlib.org/>`__) if required. After this you
should be able to use the ``iomb`` package in your Python code. To
uninstall the package, you can again use pip from the command line:

::

    pip uninstall iomb

Usage
-----

You can find a more detailed `example here <example/example.ipynb>`__ in
form of a `Jupyter notebook <http://jupyter.org/>`__ which is a
convenient way to use ``iomb``. The following script shows the basic
usage of ``iomb``. For detailed information about the data format see
the `data format specification <doc/data_format.md>`__

.. code:: python

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

License
-------

This project is in the worldwide public domain, released under the `CC0
1.0 Universal Public Domain
Dedication <https://creativecommons.org/publicdomain/zero/1.0/>`__.

.. figure:: https://licensebuttons.net/p/zero/1.0/88x31.png
   :alt: Public Domain Dedication

   Public Domain Dedication

Citation
--------

Please cite as: Srocka, M. and W. Ingwersen (2017). IO Model Builder,
v1.1 (or current version). US Environmental Protection Agency.
https://www.github.com/usepa/io-model-builder

A brief description of the iomb is also included in: Yang, Y.,
Ingwersen, W.W., Hawkins, T.R., Srocka, M., Meyer, D.E., 2017. USEEIO: A
New and Transparent United States Environmentally-Extended Input-Output
Model. Journal of Cleaner Production 158, 308-318. DOI:
`10.1016/j.jclepro.2017.04.150 <https://doi.org/10.1016/j.jclepro.2017.04.150>`__
