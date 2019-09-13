"""Power normal or Box-Cox distribution."""
import numpy
from scipy import special

from ..baseclass import Dist
from ..operators.addition import Add
from .deprecate import deprecation_warning


class power_normal(Dist):
    """Power normal or Box-Cox distribution."""

    def __init__(self, c):
        Dist.__init__(self, c=c)

    def _pdf(self, x, c):
        norm = (2*numpy.pi)**-.5*numpy.exp(-x**2/2.)
        return c*norm*special.ndtr(-x)**(c-1.)

    def _cdf(self, x, c):
        return 1.-special.ndtr(-x)**c

    def _ppf(self, q, c):
        return -special.ndtri(pow(1-q, 1./c))

    def _bnd(self, x, c):
        return self._ppf(1e-10, c), self._ppf(1-1e-10, c)


class PowerNormal(Add):
    """
    Power normal or Box-Cox distribution.

    Args:
        shape (float, Dist) : Shape parameter
        mu (float, Dist) : Mean of the normal distribution
        scale (float, Dist) : Standard deviation of the normal distribution

    Examples:
        >>> distribution = chaospy.PowerNormal(2, 2, 2)
        >>> print(distribution)
        PowerNormal(mu=2, scale=2, shape=2)
        >>> q = numpy.linspace(0,1,6)[1:-1]
        >>> print(numpy.around(distribution.inv(q), 4))
        [-0.5008  0.4919  1.3233  2.2654]
        >>> print(numpy.around(distribution.fwd(distribution.inv(q)), 4))
        [0.2 0.4 0.6 0.8]
        >>> print(numpy.around(distribution.pdf(distribution.inv(q)), 4))
        [0.1633 0.2325 0.2383 0.1768]
        >>> print(numpy.around(distribution.sample(4), 4))
        [ 1.5523 -1.122   3.5244  0.8368]
        >>> print(numpy.around(distribution.mom(1), 4))
        0.8716
        >>> print(numpy.around(distribution.ttr([1, 2, 3]), 4))
        [[0.6455 0.4421 0.2628]
         [2.7268 5.5707 8.4597]]
    """

    def __init__(self, shape=1, mu=0, scale=1):
        self._repr = {"shape": shape, "mu": mu, "scale": scale}
        Add.__init__(self, left=power_normal(shape)*scale, right=mu)


Powernorm = deprecation_warning(PowerNormal, "Powernorm")
