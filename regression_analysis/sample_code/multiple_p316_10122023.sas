******************************************************************************
* Regression Analysis - Case Example
* Interaction (p316) 10/6/2022
* Chapter 8
******************************************************************************;

options	nodate nonumber;

libname regress 'D:\Courses_2023_1121\Regression Analysis\Data';

proc format;
		value X2ft 0='Mutual'
				   1='Stock';
		run;


**read the data set;
data temp;
		infile 'D:\Courses_2023_1121\Regression Analysis\Data\CH08TA02.txt';
		input 	Y X1 X2;
		label 	Y='Number of Months Elapsed'
			   	X1='Size of Firm'
				X2='Type of Firm';
		*format	X2 X2ft.;

		retain Firm 0;
		Firm = Firm + 1;

		X1X2 = X1*X2;

		run;

proc print data=temp noobs;
format	X2 X2ft.;
var	firm y x1 x2;
run;


proc freq	data=temp;
	 tables	x2;
	 format	X2 X2ft.;
	 run;

proc means	data=temp maxdec=3;
	 class	x2;
	 var	x1;
	 run;


proc reg	data=temp;
		model	y = x1 x2 / clb;
		run;
		quit;

proc reg	data=temp;
		model	y = x1 x2 x1x2;
		run;
		quit;
