# -*- coding: utf-8 -*-
"""
=============================================================
AUTHOR: Benoit Sluysmans & Nicolas Stevens, UCL-EPL
DATE: 22/03/2015
=============================================================
MIQP for ELDP: sin problem
"""

# Imports
from __future__ import division
from pyomo.environ import *
from numpy import *
from math import *
from time import time


# Options
data = "eldp25.dat"
solver_name = "couenne"
solver_manager_name = "neos"
solver_manager_use = False

epsilon = pow(10,-2)
length = 20
bound = 1000
MaxIter = 50


# Information
print "===================================================================="
print "=       MIQP for ELDP with valve-point effect: sin problem         ="
print "=          Benoit Sluysmans & Nicolas Stevens, UCL-EPL             ="
print "===================================================================="
print ""
print "Solver:",solver_name
if solver_manager_use:
	print "SolverManager:",solver_manager_name

start_total_time = time()
model = AbstractModel()


# Parameters
model.n = Param()
model.I = RangeSet(model.n)
model.a = Param(model.I)
model.b = Param(model.I)
model.c = Param(model.I)
model.d = Param(model.I)
model.e = Param(model.I)
model.p_min = Param(model.I)
model.p_max = Param(model.I)
model.D = Param(within=NonNegativeIntegers)

model.m = Param(model.I, default = 1, mutable=True)
model.J = RangeSet(length)

model.alpha = Param(model.I,model.J, default = bound, mutable=True)
model.beta = Param(model.I,model.J, default = bound, mutable=True)

model.eps = Param(default = epsilon)
model.delta = Param(default = epsilon + 1.0, mutable=True)

model.Xi = Param(model.I, model.J, default = bound, mutable=True)


# Variables
model.p = Var(model.I, domain = NonNegativeReals)
model.t = Var(model.I, domain = NonNegativeReals)
model.k = Var(model.I, domain = Integers)
model.eta = Var(model.I, model.J, domain = Binary)
model.xsi = Var(model.I, model.J, domain = NonNegativeReals)


# Objective
def obj_expression(model):
	return sum((model.a[i]*model.p[i]*model.p[i] + model.b[i]*model.p[i] + model.c[i] + model.d[i]*sum((model.alpha[i,j]*model.xsi[i,j] + model.beta[i,j]*model.eta[i,j]) for j in xrange(1,model.m[i]+1))) for i in model.I) 
model.OBJ = Objective(rule=obj_expression, sense=minimize)


# Constraints
def demand(model):
	return sum(model.p[i] for i in model.I) == model.D
model.Demand = Constraint(rule=demand)

def powerL(model, i):
	return model.p[i] >= model.p_min[i]
model.PowerL = Constraint(model.I, rule = powerL)
def powerU(model, i):
	return model.p[i] <= model.p_max[i]
model.PowerU = Constraint(model.I, rule = powerU)

def periode1(model, i):
	return model.t[i] >= model.e[i]*(model.p[i] - model.p_min[i]) - pi*model.k[i]
model.Periode1 = Constraint(model.I, rule = periode1)
def periode2(model, i):
	return - model.t[i] <= model.e[i]*(model.p[i] - model.p_min[i]) - pi*model.k[i]
model.Periode2 = Constraint(model.I, rule = periode2)

def segment1(model, i, j):
    if model.Xi[i,j] != bound:
        return model.xsi[i,j] >= model.Xi[i,j]*model.eta[i,j]
    else:
        return Constraint.Feasible
model.Segment1 = Constraint(model.I, model.J, rule = segment1)
def segment2(model, i, j):
    if j == length:
        return Constraint.Feasible
    elif model.Xi[i,j+1] != bound:
        return model.xsi[i,j] <= model.Xi[i,j+1]*model.eta[i,j]
    else:
        return Constraint.Feasible
model.Segment2 = Constraint(model.I, model.J, rule = segment2)

def assoc(model, i):
    return 1.0 == sum(model.eta[i,j] for j in xrange(1,model.m[i]+1))
model.Assoc = Constraint(model.I, rule = assoc)
def bina(model, i):
    return model.t[i] == sum(model.xsi[i,j] for j in xrange(1,model.m[i]+1))
model.Bina = Constraint(model.I, rule = bina)


# Data
instance = model.create(data)
solver = SolverFactory(solver_name)
if solver_manager_use:
	solver_manager = SolverManagerFactory(solver_manager_name)


# Init
count = 0
max_m = max(value(instance.m[i]) for i in instance.I)

for i in instance.I:
	instance.Xi[i,1] = 0.0
	instance.Xi[i,2] = pi/2.0


# Iterations
while (value(instance.delta) > value(instance.eps) and count < MaxIter and max_m < length):
	start_time = time()
	count = count + 1
	
	print ""
	print ""
	print "========================="
	print "=     ITERATION ",count,"     ="
	print "========================="

	# alpha & beta
	for i in instance.I:
		for j in xrange(1,instance.m[i]+1):
			instance.alpha[i,j] = (sin(instance.Xi[i,j+1])-sin(instance.Xi[i,j]))/(instance.Xi[i,j+1]-instance.Xi[i,j])
			instance.beta[i,j] = sin(instance.Xi[i,j])-instance.alpha[i,j]*instance.Xi[i,j]

	# Solve
	if solver_manager_use:
		results = solver_manager.solve(instance, opt=solver)
	else:
		results = solver.solve(instance)
    
	instance.load(results);
    
    # delta
	instance.delta = sum((instance.a[i]*instance.p[i]*instance.p[i] + instance.b[i]*instance.p[i] + instance.c[i] + instance.d[i]*abs(sin(instance.e[i]*(instance.p[i]-instance.p_min[i])))) for i in instance.I) - instance.OBJ
	
	# Impose value for t
	for i in instance.I:
		instance.t[i] = sum(value(instance.xsi[i,j]) for j in xrange(1,instance.m[i]+1))
	
	
	print "OBJ + delta:",value(instance.OBJ)+value(instance.delta)
	print "delta:",value(instance.delta)
	print ""
	
	for i in instance.I:
		print "t[",i,"]:",value(instance.t[i])


    # Add breakpoints
	for i in instance.I:
		line = []
		add = True

		for j in xrange(1,instance.m[i]+2):
			line.append(value(instance.Xi[i,j]))
			if (abs(value(instance.t[i]) - value(instance.Xi[i,j])) <= value(instance.eps)):
				add = False
        
		if add:
			line.append(value(instance.t[i]))
			line.sort()
			instance.m[i] = instance.m[i]+1
            
		for j in xrange(1,instance.m[i]+2):
			instance.Xi[i,j] = line[j-1]
            
		print "Xi[",i,",:]:",line
    
	max_m = max(value(instance.m[i]) for i in instance.I)

	print ""
	print("--- Iteration time: %s seconds ---" % (time() - start_time))

print ""
print "=============================="
print "====== OPTIMAL SOLUTION ======"
print "=============================="
print "OBJ:",value(instance.OBJ)
for i in instance.I:
	print "p[",i,"]:",value(instance.p[i])
print "=============================="
print ""
print("--- Total time: %s seconds ---" % (time() - start_total_time))
print "-------------------------------------------------"


