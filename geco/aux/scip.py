import tempfile

import pyscipopt as scip

MAX_SEED = 2147483648
MAX_PRIORITY = 536870911


def branching_parameter(m: scip.Model, cuts_at_root=True):
    """
    Sets parameter to try to isolate impact of branching heuristic.
    See [1].
    ---------
    [1]: Measuring the impact of branching rules for mixed-integer programming
    """
    # cuts at root
    if not cuts_at_root:
        m.setIntParam('separating/maxroundsroot', 0)
    # cuts after root
    m.setIntParam('separating/maxrounds', 0)
    # presolving
    m.setIntParam('presolving/maxrounds', 0)
    m.setIntParam('presolving/maxrestarts', 0)
    # conflict analysis (more cuts)
    m.setBoolParam('conflict/enable', False)
    # primal heuristics
    m.setHeuristics(scip.SCIP_PARAMSETTING.OFF)


def add_optimal_solution(m: scip.Model, time_limit=None):
    with tempfile.NamedTemporaryFile(suffix=".lp", dir="/dev/shm") as pf:
        m.writeProblem(pf.name)
        model_copy = scip.Model()
        model_copy.hideOutput()
        model_copy.readProblem(pf.name)
        if time_limit:
            model_copy.setParam("limits/time", time_limit)
        model_copy.optimize()

        if model_copy.getStatus() == "optimal":
            with tempfile.NamedTemporaryFile(suffix=".sol", dir="/dev/shm") as sf:
                model_copy.writeBestSol(sf.name)
                m.readSol(sf.name)
            return True
    return False


def set_vanillafullstrongbranching(m: scip.Model, idempotent=True):
    m.setParam("branching/vanillafullstrong/priority", MAX_PRIORITY)
    m.setBoolParam('branching/vanillafullstrong/integralcands', False)
    m.setBoolParam('branching/forceallchildren', True)
    m.setBoolParam('branching/divingpscost', False)
    m.setBoolParam('branching/vanillafullstrong/idempotent', idempotent)


def stats(m: scip.Model):
    d = {
        "solving_time": m.getSolvingTime(),
        "num_nodes": m.getNNodes(),
        "status": m.getStatus(),
        "primal_bound": m.getObjVal(),
        "dual_bound": m.getDualbound(),
        "root_dual_bound": m.getDualboundRoot(),
        "_primal_bound_": m.getPrimalbound(),
        # "primal_root": None
    }
    return d
