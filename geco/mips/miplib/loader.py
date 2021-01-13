import tempfile
from urllib.request import urlretrieve
import pyscipopt as scip
import pandas as pd

MIPLIB_INSTANCE_URL = "https://miplib.zib.de/WebData/instances/"
cached_instances = {}


def load_instances(filters=None, instances_csv=None):
    if filters is None:
        filters = {}
    if instances_csv:
        df = pd.read_csv(instances_csv, header=0)
    else:
        raise NotImplemented("Dynamic loading of instances csv is not implemented yet.")

    for key, value in filters.items():
        df = df[df[key] == value]

    for instance in df["Instance  Ins."]:
        full_instance_name = instance + ".mps.gz"
        yield load_instance(full_instance_name)


def load_instance(instance_name):
    if not _instance_cached(instance_name):
        _download_instance(instance_name)
    problem_path = cached_instances[instance_name]
    model = scip.Model()
    model.readProblem(problem_path)
    return model


def _download_instance(instance_name):
    path = tempfile.NamedTemporaryFile(suffix=".mps.gz").name
    urlretrieve(MIPLIB_INSTANCE_URL + instance_name, path)
    cached_instances[instance_name] = path


def _instance_cached(instance_name):
    return instance_name in cached_instances


def easy_instances(instances_csv):
    return load_instances(filters={"Status  Sta.": "easy"}, instances_csv=instances_csv)


def hard_instances(instances_csv):
    return load_instances(filters={"Status  Sta.": "hard"}, instances_csv=instances_csv)


def open_instances(instances_csv):
    return load_instances(filters={"Status  Sta.": "open"}, instances_csv=instances_csv)
