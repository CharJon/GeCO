import tempfile

import pyscipopt as scip

MAX_SEED = 2147483648
MAX_PRIORITY = 536870911


def stats(m: scip.Model):
    d = {
        "solving_time": m.getSolvingTime(),
        "num_nodes": m.getNNodes(),
        "status": m.getStatus(),
        "primal_bound_": m.getPrimalbound(),
        "dual_bound": m.getDualbound(),
        "root_dual_bound": m.getDualboundRoot(),
        "obj_val": m.getObjVal(),
        # "primal_root": None
        "num_leaves": m.getNLeaves()
    }
    return d


class DualBoundEventHandler(scip.Eventhdlr):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.history = []

    def extract_metrics(self):
        self.history.append({
            "time": self.model.getSolvingTime(),
            "total_nodes": self.model.getNTotalNodes(),
            "dual_bound": self.model.getDualbound(),
            "lp_iterations": self.model.getNLPIterations()
        })

    def eventinit(self):
        self.model.catchEvent(scip.SCIP_EVENTTYPE.LPEVENT, self)

    def eventexit(self):
        self.model.dropEvent(scip.SCIP_EVENTTYPE.LPEVENT, self)

    def eventexec(self, event):
        self.extract_metrics()

    def eventinitsol(self):
        self.extract_metrics()

    def eventexitsol(self):
        self.extract_metrics()


class PrimalBoundEventHandler(scip.Eventhdlr):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.history = []

    def extract_metrics(self):
        self.history.append({
            "time": self.model.getSolvingTime(),
            "total_nodes": self.model.getNTotalNodes(),
            "primal_bound": self.model.getPrimalBound(),
            "lp_iterations": self.model.getNLPIterations()
        })

    def eventinit(self):
        self.model.catchEvent(scip.SCIP_EVENTTYPE.BESTSOLFOUND, self)

    def eventexit(self):
        self.model.dropEvent(scip.SCIP_EVENTTYPE.BESTSOLFOUND, self)

    def eventexec(self, event):
        self.extract_metrics()

    def eventinitsol(self):
        self.extract_metrics()

    def eventexitsol(self):
        self.extract_metrics()


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


def solve_problem_default(file, time_limit=None):
    m = scip.Model()
    m.readProblem(file)
    m.hideOutput()
    if time_limit:
        m.setParam("limits/time", time_limit)
    m.optimize()
    if m.getStatus() == "optimal":
        with open(f"/tmp/{file.split('/')[-1]}", 'w') as sf:
            m.writeBestSol(sf.name)
            return sf.name


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
        "primal_bound_": m.getPrimalbound(),
        "dual_bound": m.getDualbound(),
        "root_dual_bound": m.getDualboundRoot(),
        "obj_val": m.getObjVal()
        # "primal_root": None
    }
    return d


def solve_one_vanillafullstrong(problem_file, solution_file, node_limit=None):
    model = scip.Model()
    model.hideOutput()
    model.readProblem(problem_file)
    model.readSol(solution_file)
    set_vanillafullstrongbranching(model)
    branching_parameter(model)
    if node_limit:
        model.setParam('limits/totalnodes', node_limit)
    model.optimize()
    return {"branching": "vanillafullstrong", "settings": "isolate_branching", **stats(model)}


def solve_one_default(problem_file, solution_file, node_limit=None):
    model = scip.Model()
    model.hideOutput()
    model.readProblem(problem_file)
    model.readSol(solution_file)
    branching_parameter(model)
    if node_limit:
        model.setParam('limits/totalnodes', node_limit)
    model.optimize()
    return {"branching": "default", "settings": "isolate_branching", **stats(model)}


def solve_one_full_default(problem_file, solution_file, node_limit=None):
    model = scip.Model()
    model.hideOutput()
    model.readProblem(problem_file)
    branching_parameter(model)
    if node_limit:
        model.setParam('limits/totalnodes', node_limit)
    model.optimize()
    return {"branching": "default", "settings": "default", **stats(model)}


def solve(instance, solver):
    problem = scip.Model()
    problem.readProblem(instance)
    with tempfile.NamedTemporaryFile('w', prefix='/dev/shm/', suffix='.lp') as ntf:
        problem.writeProblem(ntf.name)
        # solve problem and solution
        optimal_solution = solve_problem_default(ntf.name)

        d = []
        for s in solver:
            d.append(s(ntf.name, optimal_solution))
        return d
