import tempfile

from geco.mips.set_cover.yang import yang_instance
from geco.mips.utilities.generic import *


def test_saving_shuffled_instance():
    model = yang_instance(300)
    shuffled_model = shuffle(model, seed=1)

    original_file = tempfile.NamedTemporaryFile(suffix=".mps")
    shuffled_file = tempfile.NamedTemporaryFile(suffix=".mps")

    model.writeProblem(original_file.name)
    shuffled_model.writeProblem(shuffled_file.name)

    with open(original_file.name, "r") as of, open(shuffled_file.name, "r") as sf:
        for line1, line2 in zip(of, sf):
            if line1 != line2:
                assert True
                break
        else:
            assert False


def test_expand_parameters():
    def add(x, y):
        return x + y

    assert list(expand_parameters(add, x=[1, 2], y=[3, 4])) == [4, 5, 5, 6]
