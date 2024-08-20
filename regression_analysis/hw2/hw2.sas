libname regress "D:\SAS\regression_analysis\workspace";
options nodate nonumber FORMCHAR="|----|+|---+=|-/\<>*"

/data step;
/*load dataset*/
data dataset;
	set regress.dataset_gpa; 
	xx = act*act;
run;

/*1.19*/
proc reg data=dataset;
	model gpa = act;
	output out=outut ;
run;
quit;

/*2.13*/
proc means data=dataset n nmiss mean std min max median maxdec=3;
	var act gpa xx;
run;
