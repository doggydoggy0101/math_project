libname regress "D:\SAS\regression_analysis\workspace";
options nodate nonumber FORMCHAR="|----|+|---+=|-/\<>*";

/*load dataset*/
data dataset;
	set regress.group_project_data; 
	interest_grade = interest*grade;
	interest_gender = interest*gender;
	interest_favor = interest*favor;
	interest_chinese = interest*chinese;
	interest_patience = interest*patience;
	interest_extras = interest*extras;
	interest_study_hours = interest*study_hours;
	interest_work_hours = interest*work_hours;
	interest_sleep_hours = interest*sleep_hours;
	interest_commute_hours = interest*commute_hours;
run;

proc reg data=dataset plots=none;
	/*	interest*1*/
	model score = interest grade gender favor chinese patience extras
	study_hours work_hours club_hours sleep_hours commute_hours
	/ include=1 selection=stepwise slentry=0.1 slstay=0.15;
	/*	interest*2*/
	model score = interest grade gender favor chinese patience extras study_hours work_hours sleep_hours commute_hours
	interest_grade interest_gender interest_favor interest_chinese interest_patience interest_extras 
	interest_study_hours interest_work_hours interest_sleep_hours interest_commute_hours
	/  include=1 selection=stepwise slentry=0.1 slstay=0.15;
	/*	interest2*/
	model score = interest grade gender favor chinese patience extras study_hours work_hours sleep_hours commute_hours
	interest_grade interest_gender interest_favor interest_chinese interest_patience interest_extras 
	interest_study_hours interest_work_hours interest_sleep_hours interest_commute_hours
	/  selection=stepwise slentry=0.1 slstay=0.15;
run;
quit;

proc reg data=dataset plots=none;
	/*	interest*1*/
	model score = interest grade favor extras
	/include=4 selection=adjrsq aic bic press cp;
	/*	interest*2*/
	model score = interest grade favor extras interest_favor interest_extras 
	/include=6 selection=adjrsq aic bic press cp;
	/*	interest2*/
	model score = grade favor extras interest_favor interest_extras 
	/include=5 selection=adjrsq aic bic press cp;
run;
quit;




