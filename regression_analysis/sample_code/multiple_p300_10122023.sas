***********************************************
* Regression Analysis - Case Example - 
* Polynomial Regression (p300) 10/12/2023
* Chapter 8
***********************************************;

options	nodate nonumber;

libname regress 'D:\Courses_2023_1121\Regression Analysis\Data';

**read the data set;
data temp;
		infile 'D:\Courses_2023_1121\Regression Analysis\Data\CH08TA01.txt';
		input Y X1 X2;
		label Y='Number of Cycles'
				X1='Charge of Rate'
				X2='Temperature';
		run;


proc means data=temp n nmiss mean std min max maxdec=3;
		 var		y x1 x2;
		 run;

proc freq data=temp;
	 tables	x1 x2;
	 run;



data temp2;
		set temp;

		** centering X1 and X2 around their respective means and also scaled them in convenient units;
		XX1 = (X1 - 1) / 0.4;
		XX2 = (X2 - 20) / 10; 

		XX1SQ = XX1**2;
		XX2SQ = XX2**2;
		X1X2 = XX1*XX2;

		retain Cell 0;
		Cell = Cell + 1;
		run;

proc print data=temp2;
run;

** model fitting;
proc reg data=temp2;
		model Y = XX1 XX2 XX1SQ XX2SQ X1X2 / ss1;
		run;
		quit;

** model refitting;
proc reg data=temp2;
		model Y = XX1 xx2 ;
		run;
		quit;


proc reg data=temp2;
		model Y = X1 x2 ;
		run;
		quit;


proc reg data=temp2;
		model Y = xX1;
		run;
		quit;

proc reg data=temp2;
		model Y = xX1;
		run;
		quit;
