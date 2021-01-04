import functools
import json
import multiprocessing
import tempfile

import tqdm

import geco.aux.scip as aux_scip
from geco.generator import *
from geco.mips.facility_location import *


def solve_capfac2(num_instances, j=1):
    n, m, r = 25, 20, 5
    capfac = functools.partial(cornuejols_instance, n, m, r)
    generator = generate_n(capfac, num_instances)
    instances = []
    for i, m in generator:
        name = f"c-{i}.lp"
        m.writeProblem(name)
        instances.append(name)

    with multiprocessing.Pool(processes=j) as p:
        ds = []
        for d in tqdm.tqdm(p.imap_unordered(solve, instances), total=len(instances)):
            print(d)
            ds += d
        return ds


if __name__ == "__main__":
    with open("out.json", 'w') as out_file:
        ds = solve_capfac2(10, 4)
        json.dump(ds, out_file)
