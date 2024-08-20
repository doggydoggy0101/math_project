libname regress "D:\SAS\regression_analysis\workspace";

data dataset_gpa; *120 x 2;
	infile "D:\SAS\regression_analysis\data\CH01PR19.txt";
	input gpa act;
    label gpa = 'GPA'  act = 'ACT';
run;

/*save dataset*/
data regress.dataset_gpa; 
	set dataset_gpa; 
run;
