libname regress "D:\SAS\regression_analysis\workspace";
options nodate nonumber FORMCHAR="|----|+|---+=|-/\<>*";

data dataset;
	set regress.group_project_data; 
run;

%macro regress(label);
	proc reg data=dataset plots=none;
		model score = &label;
	run;
	quit;
%mend;

%regress(grade); 
%regress(gender);
%regress(interest);
%regress(favor);
%regress(chinese);
%regress(patience);
%regress(extras);
%regress(study_hours);
%regress(work_hours);
%regress(club_hours);
%regress(sleep_hours);
%regress(commute_hours);
