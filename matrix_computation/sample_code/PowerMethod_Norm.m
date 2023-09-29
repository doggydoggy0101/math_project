function [lambda, ev, iter] = PowerMethod_Norm(mtx_A, iter_max, tol)

% --------------
% initialization
% --------------

n          = size(mtx_A,1);

s = RandStream('mt19937ar','Seed',0);
RandStream.setGlobalStream(s);
          
ev         = randn(n,1);
lambda_old = norm(ev);
ev         = ev / lambda_old;
iter       = 0;
err        = tol+1;

% -------------
% the main loop
% -------------

while (err > tol && iter < iter_max)
    
    % --- compute the approximate eigenpair
    
    ev_tmp     = mtx_A * ev;
    lambda     = norm(ev_tmp);
    ev_tmp     = ev_tmp / lambda;
    
    % --- compute error
    
    err_ew     = abs(lambda - lambda_old)/abs(lambda);
    err_ev     = norm(ev_tmp-ev)/norm(ev);
    err        = max( err_ew, err_ev );
    
    % --- update eigenpair
    
    ev         = ev_tmp;
    lambda_old = lambda;
    iter       = iter + 1;
    
    % --- output intermediate results
    
    % format='ew=%21.14e, ew_rel_chng=%10.4e, ev_rel_chng(%6.0f)=%10.4e \n';
    % fprintf(format, real(lambda), err_ew, iter, err_ev)
end