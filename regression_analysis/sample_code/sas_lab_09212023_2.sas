**************************
* 9/21/2023 regression;
* Example: Toluca Company on page 19;
**************************;


/*Locate a folder where you want to save the dataset*/
libname regress "D:\Courses_2023_1121\Regression Analysis\Data";

options nodate nonumber FORMCHAR="|----|+|---+=|-/\<>*";

 *data step;
data toluca; *name of data set;
		input lot work;
		label lot='Lot Size' 
			  work='Work Hours';
		cards;
80 399
30 121
50 221
90 376
70 361
60 224
120 546
80 352
100 353
50 157
40 160
70 252
90 389
20 113
110 435
100 420
30 212
50 268
90 377
110 421
30 273
90 468
40 244
80 342
70 323
;
run;

data toluca2; **new data set;
		set	toluca; *old data set;

		new_work =log(work+1); *create new variable;

		work2 = work*work;
		run;


data regress.toluca_0921; 
		set	toluca2;
		run;

*above is called the data step;



proc means data=regress.toluca_0921;
		var		work lot;
		run;


proc means data=regress.toluca_0921 n nmiss mean std min max median maxdec=3;
		var		work lot;
		run;


goptions reset=all;
symbol1 color=black value=dot w=3 ;
axis1 order=(20 to 120 by 10)  minor=none;
axis2 order=(100 to 600 by 100) minor=none ;
proc gplot	data=regress.toluca_0915;
		plot		work*lot / haxis=axis1 vaxis=axis2 ;
	 	run;
	 	quit;


goptions reset=all;
proc sgplot data=regress.toluca;
	 *xaxis label = "Work hours";
	 *yaxis label = "Lot";
	 scatter x=lot y=work / markerattrs=(size=10 symbol=Circle color=red);
	 run;



proc reg data=regress.toluca_0921; **data=toluca2;
	 model work = lot;
	 run;
quit;


goptions reset=all;
symbol1 color=black value=dot w=3 ;

proc reg	data=regress.toluca;
	 model	work = lot / lackfit p clm clb;   /*lack of fit*/
	 *title	'Results of Regression Analysis';
	 plot	work*lot; /*plot the regression line*/
	 output out=results /*name of the output dataset;*/
			predicted=pred
			residual=resid
			;
	 run;	
	 quit;



goptions reset=all;
proc gplot	data=results;
	 plot	resid*lot;
	 run;
	 quit;



/*normality check*/
proc univariate data=results normal;
		var		resid;
		*qqplot  resid / normal(mu=est sigma=est) square;
		run;


proc univariate data=toluca2 normal;
		var		work new_work;
		qqplot  work / normal(mu=est sigma=est) square;
		run;
