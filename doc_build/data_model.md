iomb - Data model
=================

`iomb` processes simple CSV files in a specific format. Entities in
the model (industry and commodity sectors, elementary flows, LCIA
categories) are identified by a combination of attributes. These
attributes are concatenated to a single, lower case character string 
which is then used in the respective row and column headers of the CSV 
files.

Industry and commodity sectors are identified by the following attributes:

    <sector code>/<sector name>/<location code>

    e.g. 1111a0/oilseed farming/us


