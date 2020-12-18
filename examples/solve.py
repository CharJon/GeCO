import functools
import json
import multiprocessing

import tqdm

import geco.aux.scip as aux_scip
from geco.generator import *
from geco.mips.facility_location import *


def solve_one(problem_file):
    model = scip.Model()
    model.readProblem(problem_file)
    model.hideOutput()
    solution_added = aux_scip.add_optimal_solution(model, 60)
    if not solution_added:
        return {"status": "solution_addition_timeout"}
    aux_scip.set_vanillafullstrongbranching(model)
    aux_scip.branching_parameter(model)
    model.setParam('limits/totalnodes', 2000)
    model.optimize()
    return aux_scip.stats(model)


def solve_capfac(num_instances, j=1):
    n, m, r = 50, 20, 5
    capfac = functools.partial(cornuejols_instance, n, m, r)
    generator = generate_n(capfac, num_instances)
    instances = []
    for i, m in generator:
        name = f"c-{i}.lp"
        m.writeProblem(name)
        instances.append(name)

    with multiprocessing.Pool(processes=j) as p:
        ds = []
        for d in tqdm.tqdm(p.imap_unordered(solve_one, instances), total=len(instances)):
            print(d)
            ds.append(d)
        return ds


if __name__ == "__main__":
    with open("out.json", 'w') as out_file:
        ds = solve_capfac(10, 4)
        json.dump(ds, out_file)
