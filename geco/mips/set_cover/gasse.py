import numpy as np
import scipy
from networkx.utils import np_random_state
import pyscipopt as scip

from geco.mips.set_cover.generic import set_cover


@np_random_state(-1)
def gasse_instance(nrows, ncols, density, max_coef=100, seed=0):
    """
    Generates instance for set cover generation as described in [1].

    Parameters
    ----------
    nrows : int
        Desired number of rows
    ncols : int
        Desired number of columns
    density: float between 0 (excluded) and 1 (included)
        Desired density of the constraint matrix
    max_coef: int
        Maximum objective coefficient (>=1)
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the generated instance

    References
    ----------
    .. [1] E.Balas and A.Ho, Set covering algorithms using cutting planes, heuristics,
    and subgradient optimization: A computational study, Mathematical
    Programming, 12 (1980), 37-60.
    """
    return set_cover(
        *gasse_params(nrows, ncols, density, max_coef, seed), name="Gasse Set Cover"
    )


@np_random_state(-1)
def gasse_params(nrows, ncols, density, max_coef=100, seed=0):
    """
    Generates instance params for set cover generation as described in [1],
    based on the code from [2].

    Parameters
    ----------
    nrows : int
        Desired number of rows
    ncols : int
        Desired number of columns
    density: float between 0 (excluded) and 1 (included)
        Desired density of the constraint matrix
    max_coef: int
        Maximum objective coefficient (>=1)
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    costs: list[int]
        Element costs in objective function
    sets: list[set]
        Definition of element requirement for each set

    References
    ----------
    .. [1] E.Balas and A.Ho, Set covering algorithms using cutting planes, heuristics,
    and subgradient optimization: A computational study, Mathematical
    Programming, 12 (1980), 37-60.
    .. [2] https://github.com/ds4dm/learn2branch/blob/master/01_generate_instances.py
    """
    nnzrs = int(nrows * ncols * density)

    assert nnzrs >= nrows  # at least 1 col per row
    assert nnzrs >= 2 * ncols  # at least 2 rows per col

    # compute number of rows per column
    indices = seed.choice(ncols, size=nnzrs)  # random column indexes
    indices[: 2 * ncols] = np.repeat(
        np.arange(ncols), 2
    )  # force at leats 2 rows per col
    _, col_nrows = np.unique(indices, return_counts=True)

    # for each column, sample random rows
    indices[:nrows] = seed.permutation(nrows)  # force at least 1 column per row
    i = 0
    indptr = [0]
    for n in col_nrows:

        # empty column, fill with random rows
        if i >= nrows:
            indices[i : i + n] = seed.choice(nrows, size=n, replace=False)

        # partially filled column, complete with random rows among remaining ones
        elif i + n > nrows:
            remaining_rows = np.setdiff1d(
                np.arange(nrows), indices[i:nrows], assume_unique=True
            )
            indices[nrows : i + n] = seed.choice(
                remaining_rows, size=i + n - nrows, replace=False
            )

        i += n
        indptr.append(i)

    # objective coefficients
    c = seed.randint(max_coef, size=ncols) + 1

    # sparse CSC to sparse CSR matrix
    A = scipy.sparse.csc_matrix(
        (np.ones(len(indices), dtype=int), indices, indptr), shape=(nrows, ncols)
    ).tocsr()
    indices = A.indices
    indptr = A.indptr

    costs = list(c)
    sets = [list(indices[indptr[i] : indptr[i + 1]]) for i in range(nrows)]
    return costs, sets
