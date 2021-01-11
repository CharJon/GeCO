import pyscipopt as scip
from geco.mips.miplib.loader import *
import pytest


def test_load_instance():
    instance = load_instance("30n20b8.mps.gz")
    assert isinstance(instance, scip.Model)


@pytest.mark.skip(reason="Resolving this requires loading the csv dynamically")
def test_load_instances():
    instances = [i for i in load_instances({"Status  Sta.": "hard"})]
    assert len(instances) == 142
    for i in instances:
        assert isinstance(i, scip.Model)


@pytest.mark.skip
def test_easy_instances():
    instances_csv = "TODO: add this"
    instances = [i for i in hard_instances(instances_csv)]
    assert len(instances) == 142
    for i in instances:
        assert isinstance(i, scip.Model)


@pytest.mark.skip
def test_hard_instances():
    instances_csv = "TODO: add this"
    instances = [i for i in easy_instances(instances_csv)]
    assert len(instances) == 677
    for i in instances:
        assert isinstance(i, scip.Model)


@pytest.mark.skip
def test_open_instances():
    instances_csv = "TODO: add this"
    instances = [i for i in open_instances(instances_csv)]
    assert len(instances) == 246
    for i in instances:
        assert isinstance(i, scip.Model)
