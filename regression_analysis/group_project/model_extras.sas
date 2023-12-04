libname regress "D:\SAS\regression_analysis\workspace";
options nodate nonumber FORMCHAR="|----|+|---+=|-/\<>*";

/*load dataset*/
data dataset;
	set regress.group_project_data; 
	extras_gender = extras*gender;
	extras_interest = extras*interest;
	extras_favor = extras*favor;
	extras_chinese = extras*chinese;
	extras_patience = extras*patience;
	extras_study_hours = extras*study_hours;
	extras_work_hours = extras*work_hours;
	extras_sleep_hours = extras*sleep_hours;
	extras_commute_hours = extras*commute_hours;
run;

proc reg data=dataset plots=none;
	/*	extras*1*/
	model score = extras interest grade gender favor chinese patience 
	study_hours work_hours club_hours sleep_hours commute_hours
	/ include=1 selection=stepwise slentry=0.1 slstay=0.15;
	/*	extras*2*/
	model score = extras interest gender favor chinese patience study_hours work_hours sleep_hours commute_hours
	extras_gender extras_interest extras_favor extras_chinese extras_patience 
	extras_study_hours extras_work_hours extras_sleep_hours extras_commute_hours
	/  include=1 selection=stepwise slentry=0.1 slstay=0.15;
	/*	extras2*/
	model score = extras interest gender favor chinese patience study_hours work_hours sleep_hours commute_hours
	extras_gender extras_interest extras_favor extras_chinese extras_patience 
	extras_study_hours extras_work_hours extras_sleep_hours extras_commute_hours
	/  selection=stepwise slentry=0.1 slstay=0.15;
run;
quit;

proc reg data=dataset plots=none;
	/*	extras*1*/
	model score = extras interest grade favor
	/include=4 selection=adjrsq aic bic press cp;
	/*	extras*2*/
	model score = extras interest favor extras_interest extras_favor
	/include=5 selection=adjrsq aic bic press cp;
	/*	extras2*/
	model score = interest favor extras_interest extras_favor
	/include=4 selection=adjrsq aic bic press cp;
run;
quit;




