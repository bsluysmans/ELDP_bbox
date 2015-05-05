# -*- coding: utf-8 -*-
"""
=============================================================
AUTHOR: Benoit Sluysmans & Nicolas Stevens, UCL-EPL
DATE: 20/04/2015
=============================================================
MIQP for ELDP: general problem

You must insert at least an input file with -i:
ELDP_bbox.py ...
-i <inputfile> 		!!! NO DEFAULT!!!	the .py file with needed parameters and cost functions
-s <solvername> 	def: couenne		the solver used (ex: couenne, bonmin, gurobi...), must be installed on your computer
-m <managername>	def: none		the solver manager used, non mandatory (ex: neos )
-y <epsilonY>   	def: 0.1		the precision on the cost
-x <epsilonX>   	def: 0.01		the precision on the power
-l <lengthXi>   	def: 25			the length for the vectors allocated to the Xi
-t <maxIter>    	def: 25			the the maximum number of iterations allowed

For more informations, see the readme on www.github....
"""

# Imports
from __future__ import division
from pyomo.environ import *
#from numpy import *
#from math import *
import time
import os
import sys
import getopt

if __name__ == '__main__':
	# Options
	py_file = ""
	solver_name = "couenne"
	solver_manager_name = "neos"
	solver_manager_use = False

	epsilony = pow(10,-2)
	epsilonx = pow(10,-1)
	length = 25
	maxIter = 25

	data = "data.dat"
	bound = -1

	options, remainder = getopt.getopt(sys.argv[1:], 'hi:s:m:y:x:l:t:', ['help','input=','solver=','manager=','epsilony=','epsilonx=','length=','maxiter='])

	for opt, arg in options:
		if opt in ('-h', '--help'):
			py_file = ""
		elif opt in ('-i', '--input'):
			arg = arg.split('.')[0]
			arg = arg.split('/')[-1]
			py_file = arg
		elif opt in ('-s', '--solver'):
			solver_name = arg
		elif opt in ('-m', '--manager'):
			solver_manager_name = arg
			solver_manager_use = True
		elif opt in ('-y', '--epsilony'):
			epsilony = float(arg)
		elif opt in ('-x', '--epsilonx'):
			epsilonx = float(arg)
		elif opt in ('-l', '--length'):
			length = int(arg)
		elif opt in ('-t', '--maxiter'):
			maxIter = int(arg)

	if py_file == "":
		print "You must insert at least an input file with -i:"
		print "ELDP_bbox.py ..."
		print "-i <inputfile>\t!!NO DEFAULT!!  the .py file with needed parameters and cost functions"
		print "-s <solvername>\tdef: couenne\tsolver used (ex: couenne, bonmin, gurobi...), must be installed on your computer"
		print "-m <managername>def: none\tsolver manager used, non mandatory (ex: neos )"
		print "-y <epsilonY>\tdef: 0.1\tprecision on the cost"
		print "-x <epsilonX>\tdef: 0.01\tprecision on the power"
		print "-l <lengthXi>\tdef: 25\t\tlength for the vectors allocated to the Xi"
		print "-t <maxIter>\tdef: 25\t\tmaximum number of iterations allowed"
		print "For more informations, see the readme on www.github...."
		sys.exit()	

	mod = __import__(py_file)

	# Information
	print "===================================================================="
	print "=     MIQP for ELDP with valve-point effect: general problem       ="
	print "=         Benoit Sluysmans & Nicolas Stevens, UCL-EPL              ="
	print "===================================================================="
	print ""
	print "Solver:",solver_name
	if solver_manager_use:
		print "SolverManager:",solver_manager_name

	# Pre-processing

	print ""
	print "Breakpoints:"

	# Add middle of breakpoints
	Xi = {}
	for i in xrange(len(mod.breakpoints)):
		line = []
		line.append(mod.breakpoints[i][0])
		for j in xrange(1,len(mod.breakpoints[i])):
			line.append((mod.breakpoints[i][j] + mod.breakpoints[i][j-1])/2.0)
			line.append(mod.breakpoints[i][j])
		line.sort()
		Xi[i] = line
	
		print ""
		print Xi[i]

	# Count intervals
	m = []
	for i in xrange(len(Xi)):
		m.append(len(Xi[i])-1)
	
	# Write n, a, b, c, p_min, p_max, D, m and Xi in .dat file if it's not there
	if data in os.listdir(os.curdir):
		os.remove(data)
	f = open(data,'a')

	# n
	f.write('\n param n := '+str(mod.n)+';\n')

	# a, b, c, p_min, p_max
	f.write('\n param: a b c p_min p_max := \n')
	for i in xrange(1,mod.n+1):
		f.write(str(i) + ' ' + str(mod.a[i-1]) + ' ' + str(mod.b[i-1]) + ' ' + str(mod.c[i-1]) + ' ' + str(mod.p_min[i-1]) + ' ' + str(mod.p_max[i-1]))
		if i == mod.n:
			f.write(';')
		f.write('\n')

	# D
	f.write('\n param D := '+str(mod.D)+';\n')

	# m
	f.write('\n param m :=\n')
	for i in xrange(len(m)):
		f.write(str(i+1)+' '+str(m[i]))
		if i == len(m)-1:
			f.write(';')
		f.write('\n')
	
	# Xi
	f.write('\n param Xi : ')
	for i in xrange(1,length+1):
		f.write(str(i)+' ')
	f.write(':=\n')

	for i in xrange(1,len(m)+1):
		f.write(str(i))
		for j in xrange(1,length+1):
			if j < m[i-1]+2:
				f.write(' '+str(Xi[i-1][j-1]))
			else:
				f.write(' 0')
			if(i == len(m) and j == length):
				f.write(';')
		f.write('\n')
	
	f.close()

	# Start time and create model
	start_total_time = time.time()
	model = AbstractModel()

	# Parameters
	model.n = Param(default=13)
	model.I = RangeSet(model.n)
	model.a = Param(model.I)
	model.b = Param(model.I)
	model.c = Param(model.I)
	model.p_min = Param(model.I)
	model.p_max = Param(model.I)
	model.D = Param(within=NonNegativeIntegers)

	model.m = Param(model.I, default = 1, mutable=True)
	model.J = RangeSet(length)

	model.alpha = Param(model.I,model.J, default = bound, mutable=True)
	model.beta = Param(model.I,model.J, default = bound, mutable=True)

	model.epsy = Param(default = epsilony)
	model.epsx = Param(default = epsilonx)
	model.delta = Param(default = epsilony + 1.0, mutable=True)

	model.Xi = Param(model.I, model.J, default = bound, mutable=True)


	# Variables
	model.p = Var(model.I, domain = NonNegativeReals)
	model.eta = Var(model.I, model.J, domain = Binary)
	model.xsi = Var(model.I, model.J, domain = NonNegativeReals)


	# Objective
	def obj_expression(model):
		return sum((model.a[i]*model.p[i]*model.p[i] + model.b[i]*model.p[i] + model.c[i] + sum((model.alpha[i,j]*model.xsi[i,j] + model.beta[i,j]*model.eta[i,j]) for j in xrange(1,model.m[i]+1))) for i in model.I)
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
		return model.p[i] == sum(model.xsi[i,j] for j in xrange(1,model.m[i]+1))
	model.Bina = Constraint(model.I, rule = bina)

	# Data
	instance = model.create(data)		

	solver = SolverFactory(solver_name)
	if solver_manager_use:
		solver_manager = SolverManagerFactory(solver_manager_name)

	# Init
	count = 0
	max_m = max(value(instance.m[i]) for i in instance.I)

	# Iterations
	while (value(instance.delta) > value(instance.epsy) and count < maxIter and max_m < length):
		start_time = time.time()
		count = count + 1
	
		print ""
		print ""
		print "========================="
		print "=     ITERATION ",count,"     ="
		print "========================="
	
		if count == 1:
			for i in instance.I:
				instance.m[i] = m[i-1]
				for j in xrange(1,instance.m[i]+2):
					instance.Xi[i,j] = Xi[i-1][j-1]
	
	
		# alpha & beta
		for i in instance.I:
			for j in xrange(1,instance.m[i]+1):
				instance.alpha[i,j] = (mod.cost_functions[i-1](value(instance.Xi[i,j+1]))-mod.cost_functions[i-1](value(instance.Xi[i,j])))/(value(instance.Xi[i,j+1])-value(instance.Xi[i,j]))
				instance.beta[i,j] = mod.cost_functions[i-1](value(instance.Xi[i,j]))-instance.alpha[i,j]*instance.Xi[i,j]
	
	
		# Solve
		if solver_manager_use:
			results = solver_manager.solve(instance, opt=solver)
		else:
			results = solver.solve(instance)
	
		instance.load(results)
	
	
	
		# delta
		instance.delta = (sum((instance.a[i]*instance.p[i]*instance.p[i] + instance.b[i]*instance.p[i] + instance.c[i] + mod.cost_functions[i-1](value(instance.p[i]))) for i in instance.I)) - instance.OBJ
	
		print "OBJ:",value(instance.OBJ)
		print "OBJ + delta:",value(instance.OBJ)+value(instance.delta)
		print "delta:",value(instance.delta)
		print ""
	
		# Add breakpoints
		for i in instance.I:
			line = []
			add = True
		
			for j in xrange(1,instance.m[i]+2):
				line.append(value(instance.Xi[i,j]))
				if (abs(value(instance.p[i]) - value(instance.Xi[i,j])) <= value(instance.epsx)):
					add = False
		    
			if add:
				line.append(value(instance.p[i]))
				line.sort()
				instance.m[i] = instance.m[i]+1
		        
			for j in xrange(1,instance.m[i]+2):
				instance.Xi[i,j] = line[j-1]
		        
			print "Xi[",i,",:]:",line

		max(value(instance.m[i]) for i in instance.I)

		print ""
		print("--- Iteration time: %s seconds ---" % (time.time() - start_time))
	print ""
	print "=============================="
	print "====== OPTIMAL SOLUTION ======"
	print "=============================="
	print "OBJ:",value(instance.OBJ)
	for i in instance.I:
		print "p[",i,"]:",value(instance.p[i])
	print "=============================="
	print ""
	print("--- Total time: %s seconds ---" % (time.time() - start_total_time))
