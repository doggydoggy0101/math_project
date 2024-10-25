# adapted from pymanopt source code
# https://github.com/pymanopt/pymanopt/blob/master/src/pymanopt/optimizers/line_search.py

class BackTrackingLineSearch:

    def __init__(self, contraction_factor=0.5, optimism=2, sufficient_decrease=1e-4, max_iteration=25, initial_step_size=1):

        self.contraction = contraction_factor
        self.optimism = optimism
        self.suff_decrease = sufficient_decrease
        self.max_iter = max_iteration
        self.init_step = initial_step_size

        self._oldf0 = None

    def search(self, objective, retraction, norm, x, desc_dir, f0, df0):

        norm_dir = norm(desc_dir)

        if self._oldf0 is not None:
            alpha = 2*(f0 - self._oldf0)/df0
            alpha *= self.optimism
        else:
            alpha = self.init_step/norm_dir

        for i in range(self.max_iter):
            
            alpha *= self.contraction
            new_x = retraction(alpha*desc_dir, x)
            new_f = objective(new_x)

            if new_f < f0 + self.suff_decrease*alpha*df0:
                break

        if new_f > f0:
            alpha = 0
            new_x = x

        step_size = alpha*norm_dir
        self._oldf0 = f0

        return new_x, step_size


class AdaptiveLineSearch:

    def __init__(self, contraction_factor=0.5, sufficient_decrease=0.5, max_iteration=10, initial_step_size=1,):

        self.contraction = contraction_factor
        self.suff_decrease = sufficient_decrease
        self.max_iter = max_iteration
        self.init_step = initial_step_size

        self._oldalpha = None

    def search(self, objective, retraction, norm, x, desc_dir, f0, df0):

        norm_dir = norm(desc_dir)

        if self._oldalpha is not None:
            alpha = self._oldalpha
        else:
            alpha = self.init_step/norm_dir

        for i in range(self.max_iter):
            
            alpha *= self.contraction
            new_x = retraction(alpha*desc_dir, x)
            new_f = objective(new_x)

            if new_f < f0 + self.suff_decrease*alpha*df0:
                break

        if new_f > f0:
            alpha = 0
            new_x = x

        step_size = alpha*norm_dir

        if i == 1:
            self._oldalpha = alpha
        else:
            self._oldalpha = 2*alpha

        return new_x, step_size