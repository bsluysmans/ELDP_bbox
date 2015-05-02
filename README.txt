------------------------------------------------------
----------------------- README -----------------------
------------------------------------------------------

This README comes to provide some help for the installation and the use of the codes found at https://github.com/bsluysmans/ELDP_bbox.

This README is divided into three sections : (1) an installation guide for "Pyomo" as well as the solvers "Couenne" and "Bonmin"; (2) documentation for the use of the AMPL codes and (3) documentation for the use of the Pyomo codes.

For more informations about the project and the mathematical background of the codes, we refer the user to our article "MIP to Globally Minimize the Economic Load Dispatch Problem With Valve-Point Effect Represented by an Unknown Piecewise Concave Function"


------------------------------
1) SOFTWARE INSTALLATION GUIDE
------------------------------

1.1 Pyomo
---------
For this project we would like to provide open source codes in order to ease the use of our model. We opted for Pyomo which is a python-based, open-source optimization modeling language (such as AMPL). Download links as well as instalation steps are described at :

http://www.pyomo.org/installation/


1.2 Solvers
-----------
BONMIN & COUENNE are open sources MINLP (mixed integer non-linear programming). For more documentation obout these solvers we refer the reader to
https://projects.coin-or.org/Bonmin		for BONMIN
https://projects.coin-or.org/Couenne	for COUENNE
where a user manual is avialiable for each of them.

The installation turns out to be tedious which is why we strongly advice the user to follow the steps carefully. We recommend the user to install both solvers via the single



-------------
2) AMPL CODES
-------------
The AMPL codes, in the folder "AMPL" implements two models :
	- "ELDP_sin.mod" implements the periodic sinusoidal model described in ??? AZAM article ???. To lauch it, write your data file name at the proper place in "ELDP_sin.run". Then, launch "ELDP_sin.run" via your AMPL editor.
	- "ELDP_bbox.mod" implements the "black box" model using a sinusoidal function as a black box, as described in ??? our article ???. To lauch it, write your data file name at the proper place in "ELDP_bbox.run". Then, launch "ELDP_bbox.run" via your AMPL editor.

--------------
3) PYOMO CODES
--------------

A "data.dat" file is also automatically generated from the ".py" with all the needed parameters, such that you can easily use AMPL with dat data file in the future if you want to.


