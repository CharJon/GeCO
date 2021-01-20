import tempfile
from urllib.request import urlretrieve, urlopen
from urllib.error import URLError
import pyscipopt as scip
import os


class Loader:
    INSTANCES_URLS = [
        "https://miplib.zib.de/WebData/instances/",  # 2017 instances
        "http://miplib2010.zib.de/download/",  # 2010 instances
        "http://miplib2010.zib.de/miplib2003/download/",  # 2003 instance
    ]

    def __init__(self, persistent_directory=None):
        """
        Initializes the MIPLIB loader object

        Parameters
        ----------
        persistent_directory: str or None
            Path for directory to use for persistent files,
            If set to None, resorts to default case of using temporary files
            that get deleted after program execution
        """
        self.instances_cache = {}
        self.dir = persistent_directory
        if persistent_directory:
            self._load_instances_cache()

    def load_instance(self, instance_name):
        if not self._instance_cached(instance_name):
            self._download_instance(instance_name)
        problem_path = self._instance_path(instance_name)
        model = scip.Model()
        model.readProblem(problem_path)
        return model

    def _instance_path(self, instance_name):
        return self.instances_cache[instance_name]

    def _generate_path_for_instance(self, instance_name):
        if self.dir:
            return self.dir + instance_name
        else:
            extention = instance_name[instance_name.index(".") :]
            return tempfile.NamedTemporaryFile(suffix=extention).name

    def _download_instance(self, instance_name):
        path = self._generate_path_for_instance(instance_name)
        for url in self.INSTANCES_URLS:
            download_url = url + instance_name
            try:
                response = urlopen(download_url)
            except URLError:
                continue
            if self._successful_response(response):
                urlretrieve(download_url, path)
                self.instances_cache[instance_name] = path
                break
        else:
            raise ValueError(
                "Was not able to find the instance in any of the MIPLIB files"
            )

    @staticmethod
    def _successful_response(response):
        return response.status == 200 and "not_found" not in response.url

    def _instance_cached(self, instance_name):
        return instance_name in self.instances_cache

    def _load_instances_cache(self):
        for path in os.listdir(self.dir):
            if path.endswith(".mps.gz"):
                instance_name = path.split("/")[-1]
                self.instances_cache[instance_name] = self.dir + path

    def __del__(self):
        if self.dir is None:
            for path in self.instances_cache.values():
                os.unlink(path)
