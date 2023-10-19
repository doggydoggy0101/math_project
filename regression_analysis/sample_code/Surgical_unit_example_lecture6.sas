******************************************************************************
* Regression Analysis - 
* Surgical Unit Example p350
* 10/19/2023
******************************************************************************;

options	nodate nonumber;
libname regress 'D:\Courses_2023_1121\Regression Analysis\Data';

data surgical;
		infile 'D:\Courses_2023_1121\Regression Analysis\Data\CH09TA01.txt'  dlm='09'x;
		input x1 x2 x3 x4 x5 x6 x7 x8 y lny;

		retain case 0;
		case = case + 1;

		label x1='blood clotting score'
				x2='prognostic index'
				x3='enzyme function test score'
				x4='liver function test score'
				x5='age'
				x6='gender'
				x7='alcohol use: moderate'
				x8='alcohol use: heavy'
				y='survival time'
				lny='ln y'
				case='case number';
		run;

/*Stepwise algorithm*/
proc reg data=surgical;
		model	lny = x4 x1-x3 x5-x8  / include=3 selection=stepwise slstay=0.15;
		run;
		quit;

/*Forward algorithm*/
proc reg data=surgical;
		model	lny = x1-x8 / selection=forward slentry=0.05 ;
		run;
		quit;

/*Backward algorithm*/
proc reg data=surgical;
		model	lny = x1-x8 / selection=backward slstay=0.05;
		run;
		quit;


/*Subset included*/
proc reg data=surgical;
		model	lny = x1-x8 / selection=stepwise slentry=0.1 slstay=0.15 include=2;
		run;
		quit;


/*Some criterion*/
proc reg data=surgical;
		model	lny = x1-x8 / SELECTION=ADJRSQ aic bic press cp;
		run;
		quit;
