libname regress "D:\SAS\regression_analysis\workspace";

data dataset_job; 
	infile "D:\SAS\regression_analysis\data\CH09PR10.txt";
	input y x1 x2 x3 x4;
    label y="score" x1="test 1" x2="test 2" x3="test 3" x4="test 4";
run;

/*save dataset*/
data regress.dataset_job; 
	set dataset_job; 
run;
