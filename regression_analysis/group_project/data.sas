libname regress "D:\SAS\regression_analysis\workspace";

proc import datafile = "D:\SAS\regression_analysis\group_project\data\math_score.csv"
	out = group_project_data dbms = CSV;
run;

/*save dataset*/
data regress.group_project_data; 
	set group_project_data; 
run;
