**************************************************
* Regression Analysis - 
* Multiple Linear Regression Analysis  Chapter 7  
* Example: Extra sums of squares p256 
**************************************************;


libname regress 'D:\Courses_2023_1121\Regression Analysis\Data';

**read the data set;
data temp;
		infile 'D:\Courses_2023_1121\Regression Analysis\Data\CH07TA01.txt';
		input X1 X2 X3	Y;
		run;

proc reg 		data=temp;
	    model	Y = X1;
		run;
		quit;

proc reg 		data=temp;
	    model	Y = X2;
		run;
		quit;

proc reg 		data=temp;
	    model	Y = X1 X2;
		run;
		quit;

proc reg 		data=temp;
	    model	Y = X1 X2 X3;
		run;
		quit;


proc reg 		data=temp;
	    model	Y = X1 X2 X3 / ss1;
		run;
		quit;
