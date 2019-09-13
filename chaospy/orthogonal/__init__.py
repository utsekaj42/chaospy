r"""
One of the basic assumption in polynomial chaos expansion is that a collection
of polynomials that are mutually orthogonal on a weighted Hilbert space. The
relation is typically written mathematically as:

.. math::
    \left\langle \Phi_n, \Phi_m \right\rangle = 0 \qquad n \neq m

In practice this relation is instead expressed by the equivalent notation using
expected values:

.. math::
    \mathbb E[\Phi_n \Phi_m] = 0 \qquad n \neq m

This relationship can in the case of ``chaospy`` be expressed as follows::

    >>> polynomials = numpoly.monomial(numpoly.symbols("q0,"), start=0, stop=3)
    >>> print(polynomials)
    [1 q0 q0**2 q0**3]
    >>> distribution = chaospy.Normal(0, 1)
    >>> print(chaospy.E(polynomials[0]*polynomials[1], distribution))
    0.0

Note that here the expected value operator implicitly assumes a probability
space to take expected value over, which in the case of the software have to be
defined explicitly.

For a more convenient way to check all pairs at the same time, it is possible
to use the ``chaospy.outer`` function::

    >>> print(chaospy.E(numpoly.outer(polynomials, polynomials), distribution))
    [[ 1.  0.  1.  0.]
     [ 0.  1.  0.  3.]
     [ 1.  0.  3.  0.]
     [ 0.  3.  0. 15.]]

For the case of ``chaospy.prange`` (which creates simple monomials), not all
pairs are orthogonal, as the outer matrix is not diagonal. The methods for
creating orthogonal polynomials are listed bellow.
"""
from .three_terms_recursion import orth_ttr
from .lagrange import lagrange_polynomial
from .gram_schmidt import orth_gs
from .cholesky import orth_chol
