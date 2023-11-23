** Logistic regression;


libname cat "D:\Courses_2023_1121\Regression Analysis\Data";

options nodate nonumber FORMCHAR="|----|+|---+=|-/\<>*";


data ebchf;
	infile "D:\Courses_2023_1121\Regression Analysis\Data\ebchf.dat";
	input	id age male sbp dbp pefr mile stair praf prchd prvlv antih fsmk csmk dm chf chfme;
	run;
/*
pefr = peak expiratory flow rate
mile = ability to walk a half mile
stair = ability to climb stairs
praf = prior to atrial fibrillation
prchd = prior diagnosis of coronary heart disease
prvlv = prior diagnosis of valvular heart disease
antih = current use of antihypertensive medications
fsmk = former smoker
csml = current smoker
dm = diagnosed or treated diabetes mellitus
chf = hospitalized for CHF or died due to CHF by the end of study
chfme = time to CHF death or the end of study (years)
*/

proc format;
	value yesnoft 1="yes"
				  0="no";
	 run;


**univariate analysis;
proc freq	data=ebchf order=data;
	 tables (mile
	  		stair
			praf
			prchd
			prvlv
			antih
			fsmk
			csmk
			dm)
			*chf / nopercent chisq;
	 *format chf yesnoft.;
	 run;




proc logistic data=ebchf;
	 model	chf(event="1") = age;
	 run;

proc logistic data=ebchf descending;
	 model	chf = sbp;
	 run;

proc logistic data=ebchf descending;
	 model	chf = dbp;
	 run;

proc logistic data=ebchf descending;
	 model	chf = pefr;
	 run;

proc logistic data=ebchf descending;
	 model	chf = mile;
	 run;

proc logistic data=ebchf;
	 model	chf = stair;
	 run;

proc logistic data=ebchf;
	 model	chf = praf;
	 run;

proc logistic data=ebchf;
	 model	chf = prchd;
	 run;

proc logistic data=ebchf;
	 model	chf = prvlv;
	 run;

proc logistic data=ebchf;
	 model	chf = antih;
	 run;

proc logistic data=ebchf;
	 model	chf = fsmk;
	 run;

proc logistic data=ebchf;
	 model	chf = csmk;
	 run;

proc logistic data=ebchf ;
	 class dm(ref="0");
	 model	chf = dm / CL;
	 run;


proc logistic data=ebchf descending;
	 model	chf = dm;
	 run;



**selection;
proc logistic data=ebchf descending;
	 model	chf = pefr age male 
			      sbp dbp
				  mile stair praf prchd prvlv antih fsmk 
				  csmk dm
		    / selection=forward include=3;
	 run;

proc logistic data=ebchf descending;
	 model	chf = age male sbp dbp pefr 
				  mile stair praf prchd prvlv antih fsmk 
				  csmk dm
		    / selection=stepwise slentry=0.2 slstay=0.2;
	 run;


proc logistic data=ebchf descending;
	 model	chf = age male sbp dbp pefr 
				  mile stair praf prchd prvlv antih fsmk 
				  csmk dm
		    / selection=backward;
	 run;


proc logistic data=ebchf descending;
	 model	chf = pefr age male sbp;
	 run;
