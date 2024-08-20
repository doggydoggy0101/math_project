libname regress "D:\SAS\regression_analysis\workspace";
options nodate nonumber FORMCHAR="|----|+|---+=|-/\<>*"

/data step;
/*load dataset*/
data dataset;
	set regress.dataset_brand; 
	x1x2 = x1*x2 ;
run;

/*6.5 (a) scatter plot matrix*/
proc sgscatter data=dataset;
    matrix y x1 x2;
run;

/*6.5 (a) correlation matrix*/
proc corr data=dataset;
run;

/*6.5 (b) regression*/
proc reg data=dataset;
    model y=x1 x2 / lackfit;
    output out = output residual=residual predicted=prediction;
run;

/*6.5 (c) box plot of residual*/
proc sgplot data=output;
	vbox residual;
run;

/*6.5 (d) residual-x1x2*/
proc sgplot data=output;
	scatter x=x1x2 y=residual / markerattrs=(size=10 symbol=Circle color=steel);
run;

/*6.7 (b) r-square between Y and \hat{Y}*/
proc reg data=output plots=none;
    model y=prediction / rsquare;
run;

/*7.3 (a) extra sum of squares*/
proc glm data=dataset plots=none;
	model y=x1 x2;
run;

/*7.12 check the other way*/
proc glm data=dataset plots=none;
	model y=x2 x1;
run;

/*7.12 R_{12}^2*/
proc glm data=dataset plots=none;
	model x1= x2; 
run;
