libname regress "C:\Users\doggy\regression_analysis\workspace";
options nodate nonumber FORMCHAR="|----|+|---+=|-/\<>*"

/data step;
/*load dataset*/
data dataset;
	set regress.dataset_gpa; 
	xx = act*act;
	yy = gpa*gpa;
	run;

/*data analysis*/
proc means data=dataset n nmiss mean std min max median maxdec=3;
	var act gpa xx yy;
	run;

/*scatter plot*/
proc sgplot data=dataset;
	 xaxis label = "ACT test score";
	 yaxis label = "GPA";
	 scatter x=act y=gpa / markerattrs=(size=6 symbol=Circle color=steel);
	 run;

/*regression model*/
proc reg data=dataset;
	 model gpa = act;
	 output out=outut p=p_ lcl=lcl_ ucl=ucl_ rstudent = r ;
	 run;
quit;
