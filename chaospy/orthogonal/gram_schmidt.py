"""
Perhaps the simplest method for creating orthogonal polynomials is
Gram-Schmidt's method. It consist of using projections to iteratively make new
terms in an expansion orthogonal to the previous ones.
"""
import logging

import numpy
import numpoly
import chaospy


def orth_gs(order, dist, normed=False, sort="G", cross_truncation=1., **kws):
    """
    Gram-Schmidt process for generating orthogonal polynomials.

    Args:
        order (int, Poly):
            The upper polynomial order. Alternative a custom polynomial basis
            can be used.
        dist (Dist):
            Weighting distribution(s) defining orthogonality.
        normed (bool):
            If True orthonormal polynomials will be used instead of monic.
        sort (str):
            Ordering argument passed to numpoly.basis. If custom basis is used,
            argument is ignored.
        cross_truncation (float):
            Use hyperbolic cross truncation scheme to reduce the number of
            terms in expansion.

    Returns:
        (Poly):
            The orthogonal polynomial expansion.

    Examples:
        >>> Z = chaospy.J(chaospy.Normal(), chaospy.Normal())
        >>> print(chaospy.orth_gs(2, Z).round(4))
        [1.0 q1 q0 -1.0+q1**2 q0*q1 -1.0+q0**2]
    """
    logger = logging.getLogger(__name__)
    dim = len(dist)

    if isinstance(order, int):
        if order == 0:
            return numpoly.polynomial(1)
        basis = numpoly.monomial(
            numpoly.symbols("q:%d" % dim), start=0, stop=order,
            ordering=sort, cross_truncation=cross_truncation)
    else:
        basis = order

    basis = list(basis)

    polynomials = [basis[0]]

    if normed:
        for idx in range(1, len(basis)):

            # orthogonalize polynomial:
            for idy in range(idx):
                orth = chaospy.descriptives.E(
                    basis[idx]*polynomials[idy], dist, **kws)
                basis[idx] = basis[idx] - polynomials[idy]*orth

            # normalize:
            norms = chaospy.descriptives.E(polynomials[-1]**2, dist, **kws)
            if norms <= 0:
                logger.warning("Warning: Polynomial cutoff at term %d", idx)
                break
            basis[idx] = basis[idx] / numpy.sqrt(norms)

            polynomials.append(basis[idx])

    else:

        norms = [1.]
        for idx in range(1, len(basis)):

            # orthogonalize polynomial:
            for idy in range(idx):
                orth = chaospy.descriptives.E(
                    basis[idx]*polynomials[idy], dist, **kws)
                basis[idx] = basis[idx] - polynomials[idy] * orth / norms[idy]

            norms.append(
                chaospy.descriptives.E(polynomials[-1]**2, dist, **kws))
            if norms[-1] <= 0:
                logger.warning("Warning: Polynomial cutoff at term %d", idx)
                break

            polynomials.append(basis[idx])

    return numpoly.polynomial(polynomials)
