"""Arc-Tangent."""
import numpy

from ..baseclass import Dist
from .. import evaluation, approximation


class Arctan(Dist):
    """
    Arc-Tangent.

    Args:
        dist (Dist): Distribution to perform transformation on.

    Example:
        >>> distribution = chaospy.Arctan(chaospy.Uniform(-0.5, 0.5))
        >>> print(distribution)
        Arctan(Uniform(lower=-0.5, upper=0.5))
        >>> q = numpy.linspace(0, 1, 6)[1:-1]
        >>> print(numpy.around(distribution.inv(q), 4))
        [-0.2915 -0.0997  0.0997  0.2915]
        >>> print(numpy.around(distribution.fwd(distribution.inv(q)), 4))
        [0.2 0.4 0.6 0.8]
        >>> print(numpy.around(distribution.pdf(distribution.inv(q)), 4))
        [1.09 1.01 1.01 1.09]
        >>> print(numpy.around(distribution.sample(4), 4))
        [ 0.1524 -0.3675  0.4231 -0.0178]
        >>> print(numpy.around(distribution.mom(2), 4))
        0.076
    """

    def __init__(self, dist):
        assert isinstance(dist, Dist)
        Dist.__init__(self, dist=dist)

    def _pdf(self, x, dist, cache):
        return evaluation.evaluate_density(
            dist, numpy.tan(x), cache=cache)*(1+numpy.tan(x)**2)

    def _cdf(self, x, dist, cache):
        return evaluation.evaluate_forward(dist, numpy.tan(x), cache=cache)

    def _ppf(self, q, dist, cache):
        return numpy.arctan(evaluation.evaluate_inverse(dist, q, cache=cache))

    def _bnd(self, x, dist, cache):
        return numpy.arctan(evaluation.evaluate_bound(
            dist, numpy.tan(x), cache=cache))

    def _mom(self, x, dist, cache):
        return approximation.approximate_moment(self, x)

    def __len__(self):
        return len(self.prm["dist"])

    def __str__(self):
        return self.__class__.__name__ + "(" + str(self.prm["dist"]) + ")"

    def _fwd_cache(self, cache):
        dist = evaluation.get_forward_cache(self.prm["dist"], cache)
        if not isinstance(dist, Dist):
            return numpy.arctan(dist)
        return self

    def _inv_cache(self, cache):
        dist = evaluation.get_forward_cache(self.prm["dist"], cache)
        if not isinstance(dist, Dist):
            return numpy.tan(dist)
        return self
