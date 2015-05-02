#=============================================================
#AUTHOR: Benoit Sluysmans & Nicolas Stevens, UCL-EPL
#DATE: 11/04/2015
#=============================================================
#MIQP for ELDP: Sin problem
# Parameters
param length := 20;

param  n;
param  a{1..n};
param  b{1..n};
param  c{1..n};   
param  d{1..n};   
param  e{1..n};    
param  p_min{1..n};
param  p_max{1..n}; 

param D;

param m{1..n};
param alpha{i in 1..n,j in 1..m[i]};
param beta{i in 1..n,j in 1..m[i]};

param Xi{i in 1..n,j in 1..length};

# Variables
var p{1..n};
var t{1..n}>=0;
var k{1..n}, integer;
var eta{i in 1..n,j in 1..m[i]}, binary;
var xsi{i in 1..n,j in 1..m[i]} >=0;

# Objective
minimize objectif : sum{i in 1..n}(a[i]*p[i]^2 + b[i]*p[i] + c[i] + d[i]*sum{j in 1..m[i]}(alpha[i,j]*xsi[i,j] + beta[i,j]*eta[i,j]));     

# Constraints
subject to demand : sum{i in 1..n} p[i]  = D;

subject to powerU{i in 1..n} : p[i] >= p_min[i];
subject to powerL{i in 1..n} : p_max[i] >= p[i];

subject to periode1{i in 1..n} : t[i] >= e[i]*(p[i] - p_min[i]) - 3.141592*k[i];
subject to periode2{i in 1..n} : e[i]*(p[i] - p_min[i]) - 3.141592*k[i] >= -t[i];

subject to segment1{i in 1..n, j in 1..m[i]} : xsi[i,j] >= Xi[i,j]*eta[i,j];
subject to segment2{i in 1..n, j in 1..m[i]} : Xi[i,j+1]*eta[i,j] >= xsi[i,j];

subject to assoc{i in 1..n} : t[i] = sum{j in 1..m[i]} xsi[i,j];
subject to bina{i in 1..n} : sum{j in 1..m[i]} eta[i,j] = 1;

