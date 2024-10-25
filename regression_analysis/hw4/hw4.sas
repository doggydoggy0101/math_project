libname regress "D:\SAS\regression_analysis\workspace";
options nodate nonumber FORMCHAR="|----|+|---+=|-/\<>*"

/data step;
/*load dataset*/
data dataset;
	set regress.dataset_job; 
	retain case 0;
	case = case + 1;
	x1x3 = x1*x3 ;
run;

/*9.10 (b) scatter plot matrix*/
proc sgscatter data=dataset;
    matrix y x1 x2 x3 x4;
run;

/*9.10 (b) correlation matrix*/
proc corr data=dataset;
run;

/*9.10 (c) regression*/
proc reg data=dataset;
    model y=x1 x2 x3 x4 / lackfit;
run;

/*9.18 (a) alpha=0.1*/
proc reg data=dataset plots=none;
	model y = x1 - x4 / selection=forward slentry=0.1;
run;
quit;

/*9.18 (a) alpha=0.05*/
proc reg data=dataset plots=none;
	model y = x1 - x4 / selection=forward slentry=0.05;
run;
quit;

/*9.18 (b) / 9.11 (a)*/
proc reg data=dataset plots=none;
	model y=x1 x2 x3 x4 / selection=adjrsq best=4;
run;

/*10.19 (a)*/
proc reg data=dataset;
    model y=x1 x2 x3 x4 x1x3 / lackfit;
run;

/*10.19 (b)*/
/*Partial regression plots (added variable plots) are formed by:*/
/*(1) Computing the residuals of regressing the response variable against the independent variables but omitting Xi*/
/*(2). Computing the residuals from regressing Xi against the remaining independent variables*/
/*(3) Plotting the residuals from (1) against the residuals from (2).*/
proc reg data=dataset plots=none;
	model y=x1;
	output out=regressModelx1 residual=regressResidx1;
	model x3=x1;
	output out=remainModelx1 residual=remainResidx1;
	model y=x3;
	output out=regressModelx3 residual=regressResidx3;
	model x1=x3;
	output out=remainModelx3 residual=remainResidx3;
run;

data partialRegressionPlots;
	set regressModelx1; label regressResidx1="residual of y & x1";
	set remainModelx1; label remainResidx1="residual of x3 & x1";
	set regressModelx3; label regressResidx3="residual of y & x3";
	set remainModelx3; label remainResidx3="residual of x1 & x3";
	by case;
run;

proc gplot data=partialRegressionPlots; 
	plot regressResidx1*remainResidx1;
	plot regressResidx3*remainResidx3;
run;
quit;

/*10.19 (d), (f), (g)*/
proc reg data=dataset plots=none;
	model y = x1 x3 / vif influence; 
	output out=result predicted=pred residual=resid rstudent=rstudent;
run; 
quit;

/*10.19 (d)*/
proc gplot data=result;
	axis1 order=(0 to 25 by 1) minor=none;
	plot rstudent*case / haxis=axis1; 
run;
quit;
