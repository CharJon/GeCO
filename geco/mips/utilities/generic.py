import pyscipopt as scip
import tempfile


def shuffle(model, seed, cons=True, vars=True):
    """
    Shuffles a MIP instance's rows & columns

    Parameters
    ----------
    model: scip.Model
        A pyscipopt model of the to be shuffled instance
    seed: int
        Used in shuffling (must be bigger than 0)
    cons: bool
        Whether the columns should be shuffled
    vars: bool
        Whether the rows should be shuffled

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the shuffled instance
    """
    # The following line of code does not correctly set the name! Leave commented until it's clear why.
    # shuffled = scip.Model(sourceModel=model, problemName=model.getProbName(), origcopy=True)
    assert seed > 0
    temp = tempfile.NamedTemporaryFile(suffix='.lp')
    model.writeProblem(temp.name)
    shuffled = scip.Model()
    shuffled.setParam("randomization/permutationseed", seed)
    shuffled.setParam("randomization/permuteconss", cons)
    shuffled.setParam("randomization/permutevars", vars)
    shuffled.readProblem(temp.name)
    shuffled.setProbName(model.getProbName())
    temp.close()
    return shuffled
