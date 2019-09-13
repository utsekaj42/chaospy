"""Binomial probability distribution."""
import numpy
from scipy import special

from ..baseclass import Dist


class Binomial(Dist):
    """
    Binomial probability distribution.

    Point density:
        comb(N, x) p^x (1-p)^{N-x}      x in {0, 1, ..., N}

    Examples:
        >>> distribution = chaospy.Binomial(5, 0.5)
        >>> print(distribution)
        Binomial(prob=0.5, size=5)
        >>> q = numpy.linspace(0, 1, 8)
        >>> print(numpy.around(distribution.inv(q), 4))
        [0. 1. 2. 2. 3. 3. 4. 5.]
        >>> print(numpy.around(distribution.fwd(distribution.inv(q)), 4))
        [0.0312 0.1875 0.5    0.5    0.8125 0.8125 0.9688 1.    ]
        >>> print(numpy.around(distribution.pdf(distribution.inv(q)), 4))
        [0.0312 0.1562 0.3125 0.3125 0.3125 0.3125 0.1562 0.0312]
        >>> print(numpy.around(distribution.sample(10), 4))
        [3. 1. 4. 2. 4. 2. 1. 2. 2. 4.]
        >>> print(numpy.around(distribution.mom([1, 2, 3]), 4))
        [ 2.5  7.5 25. ]
        >>> print(numpy.around(distribution.ttr([1, 2, 3]), 4))
        [[2.5  2.5  2.5 ]
         [1.25 2.   2.25]]
    """

    def __init__(self, size, prob):
        Dist.__init__(self, size=size, prob=prob)

    def _cdf(self, x_data, size, prob):
        return special.bdtr(numpy.floor(x_data), numpy.floor(size), prob)

    def _ppf(self, q_data, size, prob):
        return numpy.ceil(special.bdtrik(q_data, numpy.floor(size), prob))

    def _pdf(self, x_data, size, prob):
        return special.comb(size, x_data)*prob**x_data*(1-prob)**(size-x_data)

    def _bnd(self, x_data, size, prob):
        return 0, numpy.floor(size)+1

    def _mom(self, k_data, size, prob):
        x_data = numpy.arange(int(size)+1, dtype=int)
        return numpy.sum(x_data**k_data*self._pdf(
            x_data, size=numpy.floor(size), prob=prob))

    def _ttr(self, k_data, size, prob):
        """Krawtchouk rule"""
        from chaospy.quadrature import discretized_stieltjes
        abscissas = numpy.arange(0, numpy.floor(size)+1)
        weights = self._pdf(abscissas, size, prob)
        (alpha, beta), _, _ = discretized_stieltjes(k_data, [abscissas], weights)
        return alpha[0, -1], beta[0, -1]
