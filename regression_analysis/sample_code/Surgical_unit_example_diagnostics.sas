******************************************************************************
* Regression Analysis - 
* Surgical Unit Example p350
* 11/23/2023 Diagnostics
******************************************************************************;

options	nodate nonumber;
libname regress 'D:\Courses_2023_1121\Regression Analysis\Data';

data surgical;
		infile 'D:\Courses_2023_1121\Regression Analysis\Data\CH09TA01.txt'  dlm='09'x;
		input x1 x2 x3 x4 x5 x6 x7 x8 y lny;

		retain case 0;
		case = case + 1;

		label x1='blood clotting score'
				x2='prognostic index'
				x3='enzyme function test score'
				x4='liver function test score'
				x5='age'
				x6='gender'
				x7='alcohol use: moderate'
				x8='alcohol use: heavy'
				y='survival time'
				lny='ln y'
				case='case number';
		run;



** Diagnostics;

ods html style=statistical;
ods graphics on; **for diagnostics plots;

proc reg data=surgical;
		model	lny = x1 x2 x3 x8 / vif influence;
		output 	out=results
					predicted=pred
					residual=resid;
		run;
		quit;

ods graphics off;
ods html close;


proc sort data=results out=results2;
		 by	resid;
		 run;

proc print data=results2;
		run;


**to check if there is need to include x5;
proc gplot	data=results;
		plot		resid*x5;
		plot		resid*pred;
		run;
		quit;

