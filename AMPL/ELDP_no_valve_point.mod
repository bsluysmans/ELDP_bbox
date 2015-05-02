#=============================================================
#AUTHOR: Benoit Sluysmans & Nicolas Stevens, UCL-EPL
#DATE: 11/04/2015
#=============================================================
#MIQP for ELDP: The model without valve point effect
# Parameters
param  n;
param  a{1..n};
param  b{1..n};
param  c{1..n};   
param  d{1..n};   
param  e{1..n};    
param  p_min{1..n};
param  p_max{1..n}; 

param D;

# Variables
var pNV{1..n};

# Objective
minimize objectifNV : sum{i in 1..n}(a[i]*pNV[i]^2 + b[i]*pNV[i] + c[i]);      

# Constraints
s.t.
demandNV : 
	sum{i in 1..n} pNV[i]  = D;

powerUNV{i in 1..n} : 
	pNV[i] >= p_min[i];
	
powerLNV{i in 1..n} : 
	p_max[i] >= pNV[i];
	
end;


