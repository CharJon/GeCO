from geco.mips.miplib.loader import *


def test_load_instance():
    instance = load_instance('30n20b8.mps.gz')
    assert isinstance(instance, scip.Model)

