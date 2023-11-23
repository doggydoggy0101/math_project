******************************************************************************
* Logistic Regression Analysis - 
* Example Outbreak p573
******************************************************************************;

options	nodate nonumber;
libname regress 'D:\Courses_2023_1121\Regression Analysis\Data';

proc format;
		value yesnoft	0='NO'
						1='YES';
		value sesft		1='Upper'
				 		2='Middle'
				 		3='Low';
		run;

data outbreak;
		infile 'D:\Courses_2023_1121\Regression Analysis\Data\APPENC10.txt';
		input id x1 x2 x4 x5 y_d;

		label id='Case'
				x1='age'
				x2='ses'
				x4='sector'
				y_d='disease'
				x5='savings account'
				;
		run;

data outbreak2;
		set outbreak;
		if x2=2 then  x22=1;
		else		  x22=0;
		if x2=3 then  x3=1;
		else		  x3=0;

		if x4=1	then  x4=0;
		else 		  x4=1;

		if id>98	then delete;
		run;


proc logistic	data=outbreak2;
		model		y_d(event="1") = x1 x22 x3 x4 / lackfit influence ;
		run;
		quit;

proc logistic	data=outbreak2 descending;
		model		y_d = x1 x22 x3 x4 x1*x22 x1*x3 x1*x4 / selection=stepwise lackfit;
		run;
		quit;

proc logistic	data=outbreak2;
		class	x2(ref="1");
		model	y_d(event="1") = x1 x2;
		run;
		quit;



proc freq 		data=outbreak2 ;
		tables 	y_d*(x2 x4) / chisq;
		tables 	(x2 x4)*y_d / nopercent chisq;  **norow nocol;
		format	y_d yesnoft.	x2	sesft.;
		tables 	(x2 x4)*y_d;
		run;

proc means	data=outbreak2 n nmiss mean std max min q1 q3 maxdec=3;
		class	y_d;
		var		x1;
		run;


proc univariate	data=outbreak2 normal;
		var	x1;
		run;

**not normal;



proc ttest	data=outbreak2;
		class 	y_d;
		var		x1;
		run;


PROC NPAR1WAY DATA=outbreak2 WILCOXON;
		class	y_d;
		var		x1;
		run;		
