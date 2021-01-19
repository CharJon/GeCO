import tempfile

from geco.mips.set_cover.yang import yang_instance
from geco.mips.utilities.generic import *


def test_shuffle():
    model = yang_instance(300)
    shuffled = shuffle(model, seed=1)
    model.hideOutput()
    shuffled.hideOutput()
    model.optimize()
    shuffled.optimize()
    assert model.getNNodes() != shuffled.getNNodes()


def test_saving_shuffled_instance():
    model = yang_instance(300)
    shuffled_model = shuffle(model, seed=1)

    original_file = tempfile.NamedTemporaryFile(suffix=".mps")
    shuffled_file = tempfile.NamedTemporaryFile(suffix=".mps")

    model.writeProblem(original_file.name)
    shuffled_model.writeProblem(shuffled_file.name)

    with open(original_file.name, 'r') as of, open(shuffled_file.name, 'r') as sf:
        for line1, line2 in zip(of, sf):
            if line1 != line2:
                print(line1)
                print(line2)
                assert True
                return
    original_file.close()
    shuffled_file.close()
    assert False
