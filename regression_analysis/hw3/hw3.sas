libname regress "D:\SAS\regression_analysis\workspace";
options nodate nonumber FORMCHAR="|----|+|---+=|-/\<>*"

/data step;
/*load dataset*/
data dataset;
	set regress.dataset_brand; 
	x_1x_2=x_1*x_2 ;
	run;

/*scatter plot matrix*/
proc sgscatter data=dataset;
    matrix y x_1 x_2;
	run;

/*correlation matrix*/
proc corr data=dataset;
	run;

/*regression*/
proc reg data=dataset;
    model y=x_1 x_2 / lackfit;
    output out = output residual=residual predicted=prediction;
	run;
	quit;

/*6.5(b) box plot*/
proc sgplot data=output;
	vbox residual;
	run;

/*6.5(c) residual-x1x2*/
proc sgplot data=output;
	scatter x=x_1x_2 y=residual / markerattrs=(size=10 symbol=Circle color=steel);
	run;

/*6.7(b)*/
proc reg data=output;
    model y=prediction;
	run;
	quit;	

/*7.3(a)*/
proc glm data=dataset;
	model y=x_1 x_2;
run;
