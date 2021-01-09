import tempfile
import requests
import pyscipopt as scip
import os

INSTANCES_DIR = tempfile.gettempdir() + "/geco/miplib/instances/"
MIPLIB_INSTANCE_URL = "https://miplib.zib.de/WebData/instances/"

def load_instance(instance_name):
    if not instance_cached(instance_name):
        _download_instance(instance_name)
    problem_path = INSTANCES_DIR + instance_name
    model = scip.Model()
    model.readProblem(problem_path)
    return model


def _download_instance(instance_name):
    if not os.path.exists(INSTANCES_DIR):
        os.makedirs(INSTANCES_DIR)
    path = _instance_path(instance_name)
    content = requests.get(MIPLIB_INSTANCE_URL + instance_name).content
    with open(path, "wb") as f:
        f.write(content)


def instance_cached(instance_name):
    return os.path.exists(_instance_path(instance_name))


def _instance_path(instance_name):
    return INSTANCES_DIR + instance_name

