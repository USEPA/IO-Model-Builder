# Data files of the OpenIO model builder

## Basic file format
All data is stored in simple CSV files with the following properties:

* Commas (`,`) are used as column separators
* Character strings have to be enclosed in double quotes (`"`) if they contain 
  a comma or contain multiple lines. In other cases the quoting is optional.
* Numbers or boolean values (true, false) are never enclosed in quotes. The
  decimal separator is a point (`.`).
* Leading and trailing whitespaces of values are ignored
* The file encoding is UTF-8 with Windows line endings (`CR` `LF`)

## Matrix files
A dense and sparse CSV format is allowed to store matrix data. The model builder
can handle both formats but the dense format is used by default as it is easier
to explore files in this format in Excel or other spreadsheet software. In the
matrix files the rows and columns are identified by string identifiers instead 
of integer numbers. These identifiers are readable short names of the content 
(e.g. `1113A0 - Fruit farming`) and are used to link data between different 
data tables. 

### The dense matrix format
The following table shows sample data in the dense matrix format:
 
             , sector A , sector B , sector C , Scrap
    sector A ,      300 ,      25  ,        0 ,     3
    sector B ,       30 ,     360  ,       20 ,     2
    sector C ,        0 ,      15  ,      250 ,     0

As described above rows and columns are identified by readable short names 
(`sector A`, `sector B`, etc.). The order of the rows and columns in dense
matrix files does not matter as the values are identified by their row and 
column identifier. The top-left cell of the file has to be empty because this
is how the dense matrix format is distinguished from a sparse matrix format
when reading a matrix file.

### The sparse matrix format
The following table shows the same data as above but in the sparse matrix format:

    sector A , sector A , 300
    sector A , sector B ,  25
    sector A , Scrap    ,   3
    sector B , sector A ,  30
    sector B , sector B , 360
    sector B , sector C ,  20
    sector B , Scrap    ,   2
    sector C , sector B ,  15
    sector C , sector C , 250

The first column contains the row identifiers, the second the column identifiers,
and the third column contains the values. The order of the rows does not matter.

## Meta-data files
Meta-data files describe entities like industry sectors, substances, or LCIA
categories with additional attributes. The first row in a meta-data file 
contains the column headers and can contain any content that describe the
respective column. The first column contains the identifier of the entity as
it is used in the other data tables, e.g.:

    sector ID , process name  , process uuid                         , ...
    sector A  , Grain farming , 764c14f3-6e45-4749-91a9-940447b53bdb , ...
    sector B  , Fruit farming , 11a531e6-6b03-48ad-8489-b07164c0d7c2 , ...
    
