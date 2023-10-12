**************************************************
* Regression Analysis - 
* Multiple Linear Regression Analysis 10/5/2023
**************************************************;


libname regress 'D:\Courses_2023_1121\Regression Analysis\Data';

**read the data set;
data temp;
		infile 'D:\Courses_2023_1121\Regression Analysis\Data\CH06PR15.txt';
		input y x1 x2 x3;
		label y='patient satisfaction'
			 	x1='patient age'
				x2='severity of illness'
				x3='anxiety';
		run;


** scatter plot matrix and correlation matrix;
goptions reset=all;
proc sgscatter data=temp;
 		title "Scatterplot Matrix";
  		matrix y x1 x2 x3;
		run;


proc corr data=temp plots=matrix(histogram); 
 		title "Scatterplot Matrix and Correlation Matrix";
		run;


**model fitting;
**model 1;
proc reg		data=temp;
		model	y = x1;
   /*lack of fit*/
		*title	'Results of Multiple Regression Analysis';
	 	*output 	out=results
				predicted=pred
				residual=resid
				;
		run;	
		quit;
proc reg		data=temp;
		model	y = x1 x2 x3;
   /*lack of fit*/
		*title	'Results of Multiple Regression Analysis';
	 	*output 	out=results
				predicted=pred
				residual=resid
				;
		run;	
		quit;


proc reg		data=temp;
		model	y = x1 x2 x3 / lackfit covb
				SELECTION=ADJRSQ best=2;
   /*lack of fit*/
		title	'Results of Multiple Regression Analysis';
	 	output 	out=results
				predicted=pred
				residual=resid
				;

		run;	
		quit;


**Prediction;
proc glm		data=temp;
		model	y = x1 x2 x3;
		estimate "y_pred" intercept 1 x1 8 x2 16 x3 2
				;
run; 


**model 2;
proc glm		data=temp;
		model	y = x1 x2 x3 x1*x2 x1*x3 x2*x3;
		title	'Results of Multiple Regression Analysis: 
				with all the interaction terms';
	 	output 	out=results2
				predicted=pred
				residual=resid
				;
		run;	
		quit;


**model 3;
proc reg		data=temp;
		model	y = x1;
		title	'Results of Multiple Regression Analysis: 
				y = x1';
	 	output 	out=results3
				predicted=pred
				residual=resid
				;
		run;	
		quit;

proc glm		data=temp;
		model	y = x1;
		title	'Results of Multiple Regression Analysis: 
				y = x1';
	 	output 	out=results3
				predicted=pred
				residual=resid
				;
		run;	
		quit;
