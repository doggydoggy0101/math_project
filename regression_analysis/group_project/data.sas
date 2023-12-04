libname regress "D:\SAS\regression_analysis\workspace";

proc import datafile = "D:\SAS\regression_analysis\group_project\data\math_score_train.csv"
	out = group_project_data dbms = CSV;
run;

proc import datafile = "D:\SAS\regression_analysis\group_project\data\math_score_train2.csv"
	out = group_project_data_interact dbms = CSV;
run;

/*save dataset*/
data regress.group_project_data; 
	set group_project_data; 
run;

data regress.group_project_data_interact; 
	set group_project_data_interact; 
run;
