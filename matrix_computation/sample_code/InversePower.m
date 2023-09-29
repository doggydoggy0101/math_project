%==========================================================================
%> @brief Inverse power method with fixed shift
%>
%> Description:
%> Inverse power method with fixed shift for solving standard eigenvalue
%> problems.
%>
%> Reference:
%> N/A
%>
%> History:
%> 2011/01/29 First version
%>
%> Authors:
%> N/A
%>
%> @param mtx_A    coefficient matrix A of the problem Ax=lambda x
%> @param iter_max mximum iteration number
%> @param tol      error tolerance of eigenvalue and eigenvector
%>
%> @retval lambda computed eigenvalue
%> @retval ev     computed eigenvector
%> @retval iter   iteration number taken
%==========================================================================

function [lambda, ev, iter] = InversePower(sigma, mtx_A, iter_max, tol)

% --------------
% initialization
% --------------

n           = size(mtx_A,1);
mtx_A_shift = mtx_A - sigma * speye(n); 

s = RandStream('mt19937ar','Seed',0);
RandStream.setGlobalStream(s);

ev    = randn(n,1);
for ii = 1:5
    ev = mtx_A_shift \ ev;
    ev = ev / norm(ev);
end
[val,idx]  = max(abs(ev));
lambda_old = ev(idx);
ev         = ev / lambda_old;
iter       = 0;
err        = tol+1;

% -------------
% the main loop
% -------------

while (err > tol && iter < iter_max)
    
    % --- solve the linear system
    
    ev_tmp     = mtx_A_shift \ ev;
    
    % --- compute the approximate eigenpair
    
    lambda     = ev_tmp(idx);
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

% --- restore the eigenvalue

lambda = 1 / lambda + sigma;
