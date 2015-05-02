# -*- coding: utf-8 -*-
from math import *

"""
AUTHORS: Sluysmans Benoît & Stevens Nicolas
Template for the input file of ELDP_bbox.py
This example is a typical dataset in the litterature with 3 generation units

Don't change the name of the variables, just change these data with yours.
"""

"""
Breakpoints
-----------
"""
# Insert the breakpoints of your cost functions representing the valve-point effect here, each line for one generation unit
breakpoints = 	{0:[100.000000, 199.733100, 299.466200, 399.199300, 498.932400, 598.665501, 698.398601], 
				1:[100.000000, 174.799825, 249.599650, 324.399475, 399.199300, 473.999125], 
				2:[50.000000,  99.866550, 149.733100, 199.599650,  249.466200]}
"""
Parameters
----------
"""
# Insert the parameters for the problem here
# n: number of generation units
n = 3
# a, b and c: vectors of length n
# each quadratic cost function of a generation unit (without valve-point effect) is a_i*p_i^2 + b_i*p_i+c_i
a = [0.001562, 0.00194, 0.00482 ]
b = [7.92, 7.85, 7.97]
c = [561, 310, 78]
# p_min and p_max: vectors of length n representing the generator capacity constraints: p_min_i <= p_i <= p_max_i
p_min = [100, 100, 50]
p_max = [600, 400, 200]
# D: the demand to satisfy, sum_i p_i = D
D = 850

"""
Concave functions
-----------------
"""
# Define the piecwise concave cost functions representing the valve-point effect here.
# There must be n functions
d = [300, 200, 150]
e = [0.0315, 0.042, 0.063]
def fun0(p):
	return d[0]*abs(sin(e[0]*(p-p_min[0])))
	
def fun1(p):
	return d[1]*abs(sin(e[1]*(p-p_min[1])))
	
def fun2(p):
	return d[2]*abs(sin(e[2]*(p-p_min[2])))

"""
List of functions
-----------------
"""
# a vector of length n with each cost functions
cost_functions = [fun0, fun1, fun2]
	
