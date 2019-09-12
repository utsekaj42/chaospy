"""Total Sobol sensitivity index."""
import numpy

from ..conditional import E_cond
from ..variance import Var


def Sens_t(poly, dist, **kws):
    """
    Variance-based decomposition
    AKA Sobol' indices

    Total effect sensitivity index

    Args:
        poly (numpoly.ndpoly):
            Polynomial to find first order Sobol indices on.
        dist (chaospy.Dist):
            The distributions of the input used in ``poly``.

    Returns:
        (numpy.ndarray) :
            First order sensitivity indices for each parameters in ``poly``,
            with shape ``(len(dist),) + poly.shape``.

    Examples:
        >>> x, y = numpoly.symbols("x y")
        >>> poly = numpoly.polynomial([1, x, y, 10*x*y])
        >>> dist = chaospy.Iid(chaospy.Uniform(0, 1), 2)
        >>> indices = chaospy.Sens_t(poly, dist)
        >>> print(indices)
        [[0.         1.         0.         0.57142857]
         [0.         0.         1.         0.57142857]]
    """
    dim = len(dist)
    zero = [1]*dim
    out = numpy.zeros((dim,) + poly.shape, dtype=float)
    V = Var(poly, dist, **kws)
    for i in range(dim):
        zero[i] = 0
        out[i] = ((V-Var(E_cond(poly, zero, dist, **kws), dist, **kws)) /
                  (V+(V == 0))**(V!=0))
        zero[i] = 1
    return out
