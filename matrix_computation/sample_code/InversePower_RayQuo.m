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

function [sigma_new, ev, iter] = InversePower_RayQuo(sigma, mtx_A, iter_max, tol)

% --------------
% initialization
% --------------

n           = size(mtx_A,1);
mtx_A_shift = mtx_A - sigma * speye(n);

s = RandStream('mt19937ar','Seed',0);
RandStream.setGlobalStream(s);
          
ev    = randn(n,1);
for ii = 1:10
    ev = mtx_A_shift \ ev;
    ev = ev / norm(ev);
end
ev         = ev / norm(ev);
iter       = 0;
sigma_old  = ev' * mtx_A * ev;

rsdl       = norm( mtx_A * ev - sigma_old * ev );
% -------------
% the main loop
% -------------

while (rsdl > tol && iter < iter_max)
    
    % --- solve the linear system
    
    mtx_A_shift = mtx_A - sigma_old * speye(n);
    ev_tmp      = mtx_A_shift \ ev;
    
    % --- compute the approximate eigenpair
    
    ev_tmp     = ev_tmp / norm(ev_tmp);    
    sigma_new  = ev_tmp' * mtx_A * ev_tmp;
    % --- compute error
    
    err_ew     = abs(sigma_new - sigma_old)/abs(sigma_new);
    err_ev     = norm(ev_tmp-ev)/norm(ev);
    rsdl       = norm( mtx_A * ev_tmp - sigma_new * ev_tmp );
    
    % --- update eigenpair
    
    ev         = ev_tmp;
    sigma_old  = sigma_new;
    iter       = iter + 1;
    
    % --- output intermediate results
    
    % format='ew = %22.14e, ew_rel_chng = %10.4e, ev_rel_chng(%6.0f) = %10.4e \n';
    % fprintf(format, real(sigma_new), err_ew, iter, err_ev)
    % fprintf('residual = %12.4e \n',rsdl)
    
end

