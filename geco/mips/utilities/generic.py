import pyscipopt as scip


def shuffle(model, seed, cons=True, vars=True):
    """
    Shuffles a MIP instance's rows & columns

    Parameters
    ----------
    model: scip.Model
        A pyscipopt model of the to be shuffled instance
    seed: int
        Used in shuffling
    cons: bool
        Whether the columns should be shuffled
    vars: bool
        Whether the rows should be shuffled

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the shuffled instance
    """
    shuffled = scip.Model(sourceModel=model)
    shuffled.setProbName(model.getProbName())
    shuffled.setParam("randomization/permutationseed", seed)
    shuffled.setParam("randomization/permuteconss", cons)
    shuffled.setParam("randomization/permutevars", vars)
    return shuffled
