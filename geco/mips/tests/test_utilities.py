from geco.mips.utilities.generic import *
from geco.mips.set_cover.yang import yang_instance


def test_shuffle():
    model = yang_instance(300)
    shuffled = shuffle(model, seed=1)
    model.hideOutput()
    shuffled.hideOutput()
    model.optimize()
    shuffled.optimize()
    assert model.getNNodes() != shuffled.getNNodes()
