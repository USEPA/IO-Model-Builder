# Data format
iomb processes simple CSV files in a defined format that is described in the 
following sections. In principle there are two types of files:
 
1. **Data files** mainly contain input and output amounts of economic 
   and environmental flows and information directly associated with these 
   amounts (like uncertainty or data quality). Entities in these files, like 
   sectors of flows, are identified by a combination of key attributes as
   described below. 
2. **Metadata files** contain additional information that further describe
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

#### Flow identifiers
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

0. The name of the impact assessment method, e.g. `TRACI`
1. The name of the impact assessment category, e.g. `Climate change`
2. The reference unit, e.g. `kg CO2 eq.`

The key of the example would be:

    traci/climate change/kg co2 eq.

### Data frames
The `iomb` package directly uses the [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html)
class of the [pandas framework](http://pandas.pydata.org/) for the input-output
tables and calculation results. The identifiers of input-output sectors, flows,
and impact categories as described above are directly used in the row and column
indices of the data frames. Thus the selection of a process contribution to an
impact category result could look like this:

```python
result = ...
v = result['climate change gwp 100/kg co2 eq.']['1111a0/oilseed farming/us']
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

```
Index  Field                                    Type
---------------------------------------------------------------
0      Flow name                                string
1      CAS number                               string
2      Category                                 string
3      Sub-category                             string
4      Flow UUID                                UUID
5      Process/Sector name                      string
6      Process/Sector code                      string
7      Process/Sector location                  string
8      Amount                                   float
9      Unit                                     string

optional columns: 

10     Uncertainty: distribution type           enumeration
11     Uncertainty: expected value              float 
12     Uncertainty: dispersion                  float
13     Uncertainty: minimum                     float
14     Uncertainty: maximum                     float
15     Data quality: reliability                'n.a.', [1..5]
16     Data quality: temporal correlation       'n.a.', [1..5]
17     Data quality: geographical correlation   'n.a.', [1..5]
18     Data quality: technological correlation  'n.a.', [1..5]
19     Data quality: data collection            'n.a.', [1..5]
20     Year of data                             
21     Tags
22     Sources
23     Other
```

#### Characterization factors
Characterization factors for impact assessments are stored in CSV files with the
following columns:

0. Name of the impact assessment method, e.g. `TRACI`
1. Name of the impact assessment category, e.g. `Climate change`
2. Reference unit of the impact assessment category, e.g. `kg CO2 eq.`
3. Elementary flow name, e.g. `Methane`
4. Flow category / compartment, e.g. `Air`
5. Flow sub-category / sub-compartment, e.g. `Unspecified`
6. Flow unit, e.g. `kg`
7. Flow UUID
8. The value of the characterization factor

### Metadata files
Metadata files are used when the input-output model is converted to an JSON-LD
data package that can be imported into openLCA or the LCA Harmonization tool.
These files contain additional information about flows, processes, etc. and 
mappings to reference data like flow properties, locations, etc. 

Metadata files are stored in CSV files with a defined column order as described
below. The first row of a metadata file are the column headers which are ignored
by iomb. For some of the metadata files (like for units, locations, 
compartments) the iomb package contains a default file which can be replaced by
a more specific version in the JSON-LD export TODO: example

#### Metadata of elementary flows

> TODO: Metadata files of elementary flows are currently not used as all
> information about a flow is currently also available in the satellite tables.
> However, it could be useful to extract fields like CAS number, flow UUID,
> chemical formula, description, etc. from the satellite tables and add them to
> a metadata file.

A metadata file for elementary flows contains the following columns:

0. Name of the flow
1. Compartment of the flow
2. Sub-compartment of the flow
3. Unit of the flow
4. UUID of the flow
5. CAS number
6. Chemical formula
7. Description

#### Metadata of sectors/processes

```
Index  Field
0      Sector code
1      Name
2      Category
3      Sub-category
4      Location code

optional columns:

5      Description
6      Start date 
7      End date 
8      Geography description
9      Technology description
10     Intended application
11     Data set owner
12     Data generator
13     Data documentor
14     Access use restrictions
15     Project description
16     LCI method
17     Modeling constants
18     Data completeness
19     Data treatment
20     Sampling procedure
21     Data collection period
22     Reviewer
23     Data set other evaluation
24     Data quality: process review score
25     Data quality: process completeness score
26..35 Sources
```

#### Metadata files for units
iomb directly contains a file for mapping unit names to a unit and quantity
UUID that is used in the JSON-LD package. However, in the JSON-LD export this
mapping can be changed ... TODO: example

A metadata file for units should have the following columns with the first row
containing the column headers:

0. Unit name, e.g. `kg`
1. UUID of the unit
2. Quantity / Flow property name, e.g. `Mass`
3. UUID of the quantity

```csv
Unit , Unit-UUID         , Quantity , Quantity-UUID
kg   , 20aadc24-a391-... , Mass     , 93a60a56-a3c8-...
```

#### Metadata files for locations
As for units, iomb directly contains a file for mapping location codes to 
location information. When creating a JSON-LD package this also can be changed
 ... TODO: example

A metadata file for locations should have the following columns:

0. Location code, e.g. `US`
1. Location name, e.g. `United States`
2. Location UUID


#### Metadata files for compartments
TODO: add doc