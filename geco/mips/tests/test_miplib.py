import pandas as pd
import pytest

from geco.mips.miplib.base import *


def test_load_miplib_list():
    df = pd.read_csv("data/lists/branching_rules_revisited.csv", comment="#")
    loader = Loader()
    miplib_only_df = df[df["miplib"] == 1]
    for i in miplib_only_df["instance"]:
        loader.load_instance(f"{i}.mps.gz")
        path = loader.instances_cache[f"{i}.mps.gz"]
        assert os.path.exists(path)


def test_load_instance():
    instance = Loader().load_instance("30n20b8.mps.gz")
    assert isinstance(instance, scip.Model)


def test_deletion_of_temp_files():
    loader = Loader()
    instance_name = "30n20b8.mps.gz"
    loader.load_instance(instance_name)
    path = loader.instances_cache[instance_name]
    del loader
    assert not os.path.exists(path)


def test_persistent_directory():
    loader = Loader(persistent_directory="./")
    instance_name = "30n20b8.mps.gz"
    loader.load_instance(instance_name)
    del loader
    new_loader = Loader(persistent_directory="./")
    path = new_loader.instances_cache[instance_name]
    assert (
        instance_name in new_loader.instances_cache
    )  # instance path loaded correctly into cache
    assert os.path.exists(path)  # instance path exists
    os.unlink(instance_name)  # cleanup local directory


def test_miplib_sources_with_solution():
    _check_instance("30n20b8.mps.gz", with_solution=True)  # from miplib 2017
    _check_instance("neos-941262.mps.gz", with_solution=True)  # from miplib 2010
    _check_instance("vpm2.mps.gz", with_solution=True)  # from miplib 2003


def test_instance_not_found_error():
    with pytest.raises(ValueError):
        Loader().load_instance("i_am_not_an_instance.mps.gz")


def test_solution_not_found_error():
    with pytest.raises(ValueError):
        Loader().load_instance(
            "bharat.mps.gz", with_solution=True
        )  # one of miplib 2017 open instances with no known solution


def _check_instance(instance_name, with_solution=False):
    instance = Loader().load_instance(instance_name, with_solution=with_solution)
    assert isinstance(instance, scip.Model)
    if with_solution:
        sols = instance.getSols()
        assert len(sols) == 1
