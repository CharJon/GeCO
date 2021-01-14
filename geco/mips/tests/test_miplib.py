import pyscipopt as scip
from geco.mips.miplib.base import *
import os


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
