libname regress "D:\SAS\regression_analysis\workspace";
options nodate nonumber FORMCHAR="|----|+|---+=|-/\<>*"

/data step;
/*load dataset*/
data dataset;
	set regress.group_project_data; 
run;

/*scatter plot matrix*/
proc sgscatter data=dataset;
    matrix score interest favor chinese patience extras;
run;
/*regression*/
proc reg data=dataset;
    model score = interest favor chinese patience extras / lackfit;
run;
quit;

/*stepwise*/
proc reg data=dataset;
	model score = interest favor chinese patience extras / selection=stepwise slentry=0.05 slstay=0.05;
run;
quit;




