[![Build Status](https://travis-ci.org/CharJon/GeCO.svg?branch=main)](https://travis-ci.org/CharJon/GeCO) [![codecov](https://codecov.io/gh/CharJon/GeCO/branch/main/graph/badge.svg?token=IRS3LOkoFZ)](https://codecov.io/gh/CharJon/GeCO)

# GeCO

**Generators for Combinatorial Optimization**

This python package offers functionality to easily create instances for combinatorial optimization problems.
By making use of well known open source libraries as networkx for graphs and PySCIPOpt for mathematical programming,
the created instances can be used directly or saved to disk in a variety of different file formats.

## Installation

The code heavily depends on the python interface of SCIP: [PySCIPOpt](https://github.com/scipopt/PySCIPOpt). The easiest
way to install it is using conda

```bash
conda install -c scipopt pyscipopt
```

This just might not result in the most up-to-date version, another way is installing the SCIP solver and the pip package
of `pyscipopt` following [this](https://github.com/scipopt/PySCIPOpt/blob/master/INSTALL.md) guide.

Then, once you have `pyscipopt` installed, you are ready to install the `geco` package.

```bash
pip install geco
```

That's it, now you are ready to generate some instances!

## Example

Assume you want a knapsack instance like in the Yang et
al. [paper](http://www.optimization-online.org/DB_HTML/2020/02/7626.html).

You start by looking through the knapsack package, then searching for a file with the name `FIRSTAUTHOR.py`. 
In this case we find a [`yang.py`](geco/mips/knapsack/yang.py) file in the `mips/knapsack` package.

To generate an instance with 5 items you would run

```python3
from geco import knapsack

knapsack_model = knapsack.yang.yang_instance(n=5, seed=1)
```

This, as all generators inside the `mips` subpackage, returns a `PySCIPOpt` model that makes use of the SCIP mixed
integer programming solver, refer to their docs to learn how to set params, solve the instance and a lot more.

### Randomization

As you might have noticed the generator function has a seed parameter, as a matter of fact this is common through out
all generators that exhibit random behavior, it is used to preserve the random state, in order to get a random instance
each time you can use `seed=None`.

### Multiple instance generation

In case you want to generate more than one instance, we have created some helpful generator functions in
the [`generator.py`](geco/generator.py).

To generate n instances you can use the `generate_n` function, an example to generate 10 Yang knapsack instances would
be

```python3
from geco.generator import generate_n
from geco.mips.knapsack import yang

for model in generate_n(lambda seed: yang.yang_instance(n=5, seed=seed), n=10):
    model.optimize()
```

There is also another function `generate` which is more flexible, assuming you don't know exactly how many instance you
might require, it works the exact same way it just doesn't stop after `n` instances are generated.

### MIPLIB

[MIPLIB](https://miplib.zib.de/) 2017 instances can be loaded into a PySCIPOpt model using the `Loader` class.

```python
from geco.mips.miplib.base import Loader

instance = Loader().load_instance('INSTANCE_NAME.mps.gz')
```

## Implemented Generators

All the following instances are implemented following some of the generation techniques found in the literature, please
refer to the modules corresponding to the generating function for a reference to where it was introduced.

### MIPS

- Capacitated Facility Location
- Scheduling
- Knapsack
- Set Packing
- Set Cover
- Production Planning
- Maximum Independent Set
- Maximum Cut
- Packing
- Graph Coloring

# Contributing
If you want to add some new generator, fix a bug or enhance the repository in some way, please refer to our [guide](CONTRIBUTING.md).
