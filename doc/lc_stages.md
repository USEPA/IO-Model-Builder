# Integration of Life Cycle Stages
The `iomb` model can be extended to include additional life cycle stages. The
direct requirements coefficients matrix describes then the cradle-to-gate phase
of the system and additional coefficients tables that describe the requirements
of the other life cycle stages can be added with the optional parameter
`lc_stages` when creating the model:

```python
model = iomb.make_model('drc.csv',
                        ['satellite_table1.csv', 'satellite_table2.csv'],
                        "sector_meta_data.csv",
                        ['LCIA_factors1.csv', 'LCIA_factors1.csv'],
                        lc_stages=['use_drc.csv', 'distribution_drc.csv'])
```

The data format of the coefficients table is as follows:

```
Index  Field                        Type
-----------------------------------------------------------------
0      Life cycle phase             string (e.g. "use phase")
1      Consuming sector - code      string (e.g. "1111A0")
2      Consuming sector - name      string (e.g. "Oilseed farming")
3      Consuming sector - location  string (e.g. "US")
4      Supplying sector - code      string
5      Supplying sector - name      string
6      Supplying sector - location  string
7      Amount                       float (e.g. 0.3)

# additional columns for documentation, uncertainty, or data quality information
# could be added
```

A row in such a table means that a sector (the consuming sector) needs an input
of the given amount from another sector (the supplying sector) per 1 unit of
output in the given life cycle stage.

Additionally, direct emissions and resources of a sector in a life cycle stage
per 1 unit of output can be added in the satellite tables by adding the name of
the life cycle stage to the respective satellite table row (see also the
satellite table format):

```
Index  Field                                    Type
---------------------------------------------------------------
0      Flow name                                string
1      CAS number                               string
2      Category                                 string
3      Sub-category                             string
...
8      Amount                                   float
9      Unit                                     string

# Optional columns
...
24     Life cycle phase                         string (e.g. "use phase")
```

## Numerical example
Suppose we have the following direct requirements coefficients, demand vector,
and satellite table:

Direct requirements coefficients:
```
                    , 1/Manufacturing/US , 2/Transport/US , 3/Energy/US
1/Manufacturing/US  , 0.4                , 0.2            , 0.1
2/Transport/US      , 0.2                , 0.1            , 0.1
3/Energy/US         , 0.3                , 0.3            , 0.2
```

Demand vector:
```
1/Manufacturing/US  , 200
2/Transport/US      ,   0
3/Energy/US         ,  50 
```

Satellite table:
```
     , 1/Manufacturing/US , 2/Transport/US , 3/Energy/US
CO2  , 2                  , 0.5            , 1
```

The cradle-to-gate inventory result could be calculated with the following
script:

```julia
# the direct requirements coefficients
A = [0.4  0.2  0.1 ;  # 1/Manufacturing/US
     0.2  0.1  0.1 ;  # 2/Transport/US
     0.3  0.3  0.2 ]  # 3/Energy/US

# the satellite table
B = [2.0  0.5  1]     # CO2

# the demand vector
f = [200.0 ;
       0.0 ;
      50.0 ]

# the scaling vector
I = eye(size(A)[1])
s = (I - A) \ f

# the total LCI result
g = B * s  # 1163.27 kg CO2

# the direct contribution results
G = B * diagm(s)   # [836.735  61.2245  265.306]  kg CO2
```

So, the cradle-to-gate LCI result would be 1163.27 kg CO2 with direct
contributions from the manufacturing, transport, and energy sector of
836.73, 61.22, and 265.31 kg CO2 respectively.

### Adding additional requirements
Suppose that for the distribution phase of the manufacturing sector an 
additional input of 0.3 USD and for the energy sector an additional input of 
0.1 USD from the transport sector per 1.0 USD output are required. Then we would
add the following table via the `lc_stages` parameter to our model: 

```
Phase        , cons.-code , cons.-name    , cons.-loc. , supp.-code , supp.-name , supp.-loc. , amount
distribution , 1          , Manufacturing , US         , 2          , Transport  , US         , 0.3
distribution , 3          , Energy        , US         , 2          , Transport  , US         , 0.1
```

Combining this with the final demand vector above, we need `200 * 0.3 + 50 * 0.1`
USD from transport sector in the use phase. In general, we can calculate the
demand vector `fd` for the distribution phase by creating a coefficients matrix
for the additional requirements and multiplying it with final demand vector:

```julia
# additional requirements matrix of the distribution phase
K = [ 0.0  0.0  0.0 ;  # 1/Manufacturing/US
      0.3  0.0  0.1 ;  # 2/Transport/US
      0.0  0.0  0.0 ]  # 3/Energy/US

# demand vector of the distribution phase
fd = K * f  # [0.0  65.0  0.0]'
```

The calculation of the LCI result and direct contributions of the distribution
are calculated in the same way as for the cradle-to-gate phase:

```julia
# the scaling vector of the distribution phase
sd = (I - A) \ fd

# the total LCI result of the distribution phase
gd = B * sd  # 160.131 kg CO2

# the direct contribution results of the distribution phase
Gd = B * diagm(sd)   # [72.0117  42.6385  45.481]  kg CO2
```

So we would have 160.13 kg CO2 emissions in the distribution phase for our final
demand with contributions of the manufacturing, transport, and energy sector of
72.01, 42.64, and 45.48 kg CO2 respectively. Note that these emissions are
related to the complete life cycle for providing the additional requirements 
(transport in our example) in the distribution phase.

## Adding additional emissions or resources
It is also possible to add additional emissions or resources of a sector in a 
life cycle phase by tagging the respective rows in the satellite table with
the name of the life cycle phase. If the energy sector in our example would have
an emission of 5 kg CO2 per 1 USD output in the distribution phase, we would add
the following line to a satellite table:

```
Flow name , ... , Sector name, Sector code, Sector loc, Amount , Unit , ... , Life cycle phase
CO2       , ... , Energy     , 3          , US        , 5      , kg   , ... , distribution
```

In the calculation, we would then have an additional satellite table for the
distribution phase `Bd`:

```julia
Bd = [ 0.0  0.0  5.0]  # kg CO2
```

The LCI result the direct contributions for this can be calculated with the
final demand vector:

```julia
gd2 = Bd * f   # 250.0 kg CO2

Gd2 = Bd * f'  # [0.0  0.0  250.0] kg CO2
```

Thus, for the example the energy sector would add 250.0 kg CO2 of additional
emissions in the use phase for the final demand vector. Together with the
cradle-to-gate phase and the additional requirements, we would have 
`1163.27 + 160.13 + 250.00 = 1573.4` kg CO2 of total emissions. The contribution
of the use phase would be `160.13 + 250.00 = 410.13` kg CO2 and the contribution
of the energy sector would be `265.31` kg CO2 in the cradle-to-gate phase and
`45.48 + 250.0 = 295.48` kg CO2 in the use phase where the `45.48` kg are related
to the energy use for providing transport as additional requirement and the `250`
kg to the additional emissions of this sector in the use phase.
