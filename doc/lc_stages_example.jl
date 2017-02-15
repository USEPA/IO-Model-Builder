######### gradle-to-gate calculation

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


######### additional requirements in the distribution phase

# additional requirements matrix of the distribution phase
K = [ 0.0  0.0  0.0 ;  # 1/Manufacturing/US
      0.3  0.0  0.1 ;  # 2/Transport/US
      0.0  0.0  0.0 ]  # 3/Energy/US

# demand vector of the distribution phase
fd = K * f  # [0.0  65.0  0.0]'

# the scaling vector of the distribution phase
sd = (I - A) \ fd

# the total LCI result of the distribution phase
gd = B * sd  # 160.131 kg CO2

# the direct contribution results of the distribution phase
Gd = B * diagm(sd)   # [72.0117  42.6385  45.481]  kg CO2


######### additional emissions in the distribution phase

Bd = [ 0.0  0.0  5.0]  # kg CO2

gd2 = Bd * f   # 250.0 kg CO2

Gd2 = Bd * diagm(f)  # [0.0  0.0  250.0] kg CO2
