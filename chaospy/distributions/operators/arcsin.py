"""Arc-Sinus."""
import numpy
from ..baseclass import Dist
from .. import evaluation, approximation


class Arcsin(Dist):
    """
    Arc-Sinus.

    Args:
        dist (Dist): Distribution to perform transformation on.

    Example:
        >>> distribution = chaospy.Arcsin(chaospy.Uniform(0, 1))
        >>> print(distribution)
        Arcsin(Uniform(lower=0, upper=1))
        >>> q = numpy.linspace(0,1,6)[1:-1]
        >>> print(numpy.around(distribution.inv(q), 4))
        [0.2014 0.4115 0.6435 0.9273]
        >>> print(numpy.around(distribution.fwd(distribution.inv(q)), 4))
        [0.2 0.4 0.6 0.8]
        >>> print(numpy.around(distribution.pdf(distribution.inv(q)), 4))
        [0.9798 0.9165 0.8    0.6   ]
        >>> print(numpy.around(distribution.sample(4), 4))
        [0.7123 0.1153 1.2541 0.5032]
        >>> print(numpy.around(distribution.mom(1), 4))
        0.5708
        >>> print(numpy.around(distribution.ttr([0, 1, 2]), 4))
        [[0.5708 0.7302 0.7625]
         [1.     0.1416 0.1492]]
    """

    def __init__(self, dist):
        assert isinstance(dist, Dist)
        Dist.__init__(self, dist=dist)

    def _pdf(self, x, dist, cache):
        """Probability density function."""
        return evaluation.evaluate_density(
            dist, numpy.sin(x), cache=cache)*numpy.cos(x)

    def _cdf(self, x, dist, cache):
        return evaluation.evaluate_forward(dist, numpy.sin(x), cache=cache)

    def _ppf(self, q, dist, cache):
        return numpy.arcsin(evaluation.evaluate_inverse(dist, q, cache=cache))

    def _bnd(self, x, dist, cache):
        return numpy.arcsin(evaluation.evaluate_bound(
            dist, numpy.sin(x), cache=cache))

    def _mom(self, x, dist, cache):
        return approximation.approximate_moment(self, x)

    def __len__(self):
        return len(self.prm["dist"])

    def __str__(self):
        return self.__class__.__name__ + "(" + str(self.prm["dist"]) + ")"

    def _fwd_cache(self, cache):
        dist = evaluation.get_forward_cache(self.prm["dist"], cache)
        if not isinstance(dist, Dist):
            return numpy.arcsin(dist)
        return self

    def _inv_cache(self, cache):
        dist = evaluation.get_forward_cache(self.prm["dist"], cache)
        if not isinstance(dist, Dist):
            return numpy.sin(dist)
        return self
