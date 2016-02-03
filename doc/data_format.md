# Data format of the OpenIO model builder


## Basic file format
All data is stored in simple CSV files with the following properties:

* Commas (`,`) are used as column separators
* Character strings have to be enclosed in double quotes (`"`) if they contain 
  a comma or contain multiple lines. In other cases the quoting is optional.
* Numbers or boolean values (true, false) are never enclosed in quotes. The
  decimal separator is a point (`.`).
* The file encoding is UTF-8 with Windows line endings (`CR` `LF`)

## Matrix files
A dense and sparse CSV format is allowed to store matrix data. The model builder
can handle both formats but the dense format is used by default as it is easier
to explore files in this format in Excel or other spreadsheet software. In the
matrix files the rows and columns are identified by string identifiers instead 
of integer numbers. These identifiers are readable short names of the content 
(e.g. `1113A0 - Fruit farming`) and are used to link data between different 
data tables. 

### Dense matrix format
The following table shows the principle of the dense matrix format:
 
    |          | sector A | sector B | sector C | Scrap |
    | sector A |      300 |      25  |        0 |     3 |
    | sector B |       30 |     360  |       20 |     2 |
    | sector C |        0 |      15  |      250 |     0 |


"A","A",300
"A","B",25
"A","Scrap",3
"B","A",30
"B","B",360
"B","C",20
"B","Scrap",2
"C","B",15
"C","C",250

## Meta-data files
