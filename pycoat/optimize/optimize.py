# coding: utf-8

import sys
from collections import deque
from itertools import product


def brute(f, vectors, args=(), start_from=None,
          max_iter=None, max_best=100, full_output=0,
          callback=None):
    """Minimize a function over a given range by brute force.

    Parameters
    ----------
    f : callable ``f(x,*args)``
        Merit function to be minimize.
    vectors : sequence
        Each element is a sequence of possible values of the function args.
    args : tuple, optional
        Extra arguments passed to `f`.
    max_iter : int, optional
        Maximum number of iteration to perform.
    max_best : int, optional
        Maximum number of the best parameters to return.
    full_output : bool, optional
        If set to `True`, return x0, point and Jbest
        in addition to x0.
    callback : callable, optional
        An optional function to call after each iteration.
        Called as ``callback(point,J,params)``, where
        `point` is the current coordinates over the grid,
        `J` is the current function value and
        `params` is the current parameter vector.

    Returns
    -------
    x0 : ndarray
        Value of arguments to `func`, giving minimum over the grid.
    last_point : tuple
        Last point.
    Jbest : ndarray
        Array of tuple with information about `max_best` last results.
    """
    if start_from:
        if len(start_from) != len(vectors):
            raise ValueError("start_from and vectors parameters"
                             "must have the same length.")

    N = len(vectors)
    # (y, params, point)
    Jbest = deque([(sys.maxsize, None, None)], maxlen=max_best)

    if start_from:
        loops = [range(x, len(v)) for x, v in zip(start_from, vectors)]
    else:
        loops = [range(len(v)) for v in vectors]
    point = None
    for i, point in enumerate(product(*loops), 1):
        params = [v[coord] for coord, v in zip(point, vectors)]
        y = f(params, *args)
        J = (y, params, point)
        if J[0] <= Jbest[-1][0]:
            Jbest.append(J)
        if callable(callback):
            callback(i, J)
        if i == max_iter:
            break

    y0, x0, _ = Jbest[-1]
    Jbest = list(filter(lambda x: x[0] != sys.maxsize, Jbest))

    if full_output:
        return dict(x0=x0, last_point=point, Jbest=Jbest)
    else:
        return x0
