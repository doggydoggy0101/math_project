libname regress "D:\SAS\regression_analysis\workspace";
options nodate nonumber FORMCHAR="|----|+|---+=|-/\<>*";

/*load dataset*/
data dataset;
	set regress.group_project_data; 
	patience_interest = patience*interest;
	patience_favor = patience*favor;
	patience_extras = patience*extras;
	patiencet_study_hours = patience*study_hours;
	patience_sleep_hours = patience*sleep_hours;
run;

proc reg data=dataset plots=none;
	/*	patience*1*/
	model score = patience interest grade gender favor chinese extras
	study_hours work_hours club_hours sleep_hours commute_hours
	/ include=1 selection=stepwise slentry=0.1 slstay=0.15;
	/*	patience*2*/
	model score = patience interest grade favor chinese extras study_hours sleep_hours
	patience_interest patience_favor patience_extras patiencet_study_hours patience_sleep_hours
	/  include=1 selection=stepwise slentry=0.1 slstay=0.15;
	/*	patience2*/
	model score = patience interest grade favor chinese extras study_hours sleep_hours
	patience_interest patience_favor patience_extras patiencet_study_hours patience_sleep_hours
	/  selection=stepwise slentry=0.1 slstay=0.15;
run;
quit;

proc reg data=dataset plots=none;
	/* patience*1*/
	model score = patience interest grade favor chinese extras sleep_hours
	/ include=7 selection=adjrsq aic bic press cp;
	/*	patience*2*/
	model score = patience interest favor chinese extras sleep_hours patience_favor patience_extras
	/ include=8 selection=adjrsq aic bic press cp;
	/*	patience2*/
	model score = interest grade favor extras 
	/include=4 selection=adjrsq aic bic press cp;
run;
quit;




