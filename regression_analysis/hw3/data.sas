libname regress "D:\SAS\regression_analysis\workspace";

data dataset_brand; 
	infile "D:\SAS\regression_analysis\data\CH06PR05.txt";
	input y x_1 x_2;
    label y="brand" x_1="moisture" x_2="sweetness";
	run;

/*save dataset*/
data regress.dataset_brand; 
	set dataset_brand; 
	run;
