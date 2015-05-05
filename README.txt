------------------------------------------------------
----------------------- README -----------------------
------------------------------------------------------

This README comes to provide some help for the installation and the use of the codes found at https://github.com/bsluysmans/ELDP_bbox.

This README is divided into three sections : 	
						(1) an installation guide for "Pyomo" as well as the solvers "Couenne" and "Bonmin"; 
						(2) documentation for the use of the AMPL codes; 
						(3) documentation for the use of the Pyomo codes.

For more informations about the project and the mathematical background of the codes, we refer the user to our article [1] (see "References" at the end of the README).

A special attention was devoted to the development of a software tool that would allow a user uninformed of Mixed Integer Programming (MIP) techniques to use our algorithm easily. This software should ideally rely on open-source solvers.


------------------------------
1) SOFTWARE INSTALLATION GUIDE
------------------------------

1.1 Pyomo
---------
For this project, we would like to provide open source codes in order to ease the use of our model. We opted for Pyomo which is a python-based, open-source optimization modeling language (such as AMPL). Download links as well as installation steps are described at :

			http://www.pyomo.org/installation/


1.2 Solvers
-----------
BONMIN & COUENNE are open sources MINLP (mixed integer non-linear programming). For more documentation about these solvers we refer the reader to

	https://projects.coin-or.org/Bonmin		for BONMIN

	https://projects.coin-or.org/Couenne		for COUENNE

where a user manual is availiable for each of them.

The installation turns out to be tedious which is why we strongly advice the user to follow the steps carefully. We recommend the user to install both solvers via the single "Couenne" package which includes both Couenne and Bonmin solvers. This package is available at:

		http://www.coin-or.org/download/binary/Couenne/

The "full" installation process is detailed at the previous web page. However, we give here some advices which might ease the job : 
	
	- First you will need some "Third party" packages. There are available at 

		https://projects.coin-or.org/Bonmin/wiki/ThirdParty

	Just follow the procedure explained.

	- Then you have to download the actual solvers available at 
		 
		http://www.coin-or.org/download/binary/Couenne/

	- The installation steps are detailed at 

		https://projects.coin-or.org/Couenne

	- Note that for the sixth step, where you have to run 

			"../configure -C" 

we strongly advice you to run instead 

			"../configure -C --prefix=/usr/local" 

This will install the library at the "usr/local/bin" folder of your computer. This is very useful as it allows to call the solvers in the code directly by their name (i.e. instead of writing "/usr/myName/.../folder/couenne" you will simply write "couenne" in the Pyomo code).


1.3 AMPL 
---------

AMPL is a commercial language which includes commercial solvers (such as Gurobi or Cplex). You thus need to purchase a licence. Note that free academic licences are also available. For more information, see

				http://ampl.com 		
		

-------------
2) AMPL CODES
-------------

The AMPL codes, in the folder "AMPL" implements two models :

	- "ELDP_sin.mod" implements the periodic sinusoidal model described in the article [2]. 
	To launch it, write your data file name at the proper place in "ELDP_sin.run". Then, launch "ELDP_sin.run" via your AMPL editor.

	- "ELDP_bbox_sin.mod" implements the "black box" model using a sinusoidal function as a black box, as described in [1]. To launch it, write your data file name at the 	proper place in "ELDP_bbox_sin.run". Then, launch "ELDP_bbox_sin.run" via your AMPL editor.


--------------
3) PYOMO CODES
--------------

The Pyomo codes, in the folder "Python" implements three models : 

	- "ELDP_sin.py", which implements the same model as previously "ELDP_sin.mod" in AMPL.

	- "ELDP_bbox_sin.py", which implements the same model as previously "ELDP_bbox_sin.mod" in AMPL.


	- ***** "ELDP_bbox.py" *****, which implements the FULL BLACK BOX MODEL and is the true FINAL PRODUCT of this project. The user has to provide a data file written in Python. Note that a "template" of such data file is presented at "template_data.py" in order to make it clear. The code can be fully used through the terminal without opening the code. The required arguments are the following : 

--------------------------------------------------------------------
You must insert at least an input file with -i:
ELDP_bbox.py ...
-i <inputfile> 		!!! NO DEFAULT!!!	the .py file with needed parameters and cost functions
-s <solvername> 	def: couenne		the solver used must be installed on your computer (ex: couenne, bonmin...)
-m <managername>	def: none		the solver manager used, non mandatory (ex: neos )
-y <epsilonY>   	def: 0.1		the precision on the cost
-x <epsilonX>   	def: 0.01		the precision on the power
-l <lengthXi>   	def: 25			the length for the vectors allocated to the Xi
-t <maxIter>    	def: 25			the the maximum number of iterations allowed
--------------------------------------------------------------------


NB : The way it works is the following. The user provide the "myData.py" data file. The program read it and automatically  generates a "data.dat" file including all the needed parameters, such that you can easily use AMPL with ".dat" data file in the future if you want to.


-------------
4) DATA FILES
-------------

The data files in ".dat" used in [1] and [2] are available in the folder "Data". These are the most common data found in the literature about this subject. There are a 3-units setting, a 13-units setting and a 40-units setting. These are both available in the "sin" template and in the "sin black box" template.




--------------------
 *** REFERENCES ***
--------------------

[1] Benoit SLUYSMANS, Nicolas STEVENS, P.-A. ABSIL. "MIP to Globally Minimize the Economic Load Dispatch Problem With Valve-Point Effect Represented by a Piecewise Concave Function"

[2] Michael Azzam, S Selvan, Augustin Lefevre, and P-A Absil. "Mixed integer programming to globally minimize the economic load dispatch problem with valve-point effect". arXiv preprint arXiv:1407.4261, 2014.








