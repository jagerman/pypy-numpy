#!/usr/bin/python3

import json
import requests
import os.path
import shutil
from subprocess import run
from config import pypy, pypy_wheel_suffix, repo

def version(package_name):
    url = "https://pypi.python.org/pypi/{}/json".format(package_name)
    data = requests.get(url).json()
    return data["info"]["version"]

vnp, vsp = version("numpy"), version("scipy")
np_whl = 'numpy-' + vnp + pypy_wheel_suffix
sp_whl = 'scipy-' + vsp + pypy_wheel_suffix
if not os.path.isfile(repo + '/numpy/' + np_whl) or not os.path.isfile(repo + '/scipy/' + sp_whl):
    print("Numpy and/or scipy wheels outdated or do not exist; building new wheels")
    run([repo + "/../build-numpy-pypy.sh", pypy], check=True)
    if not os.path.isfile(repo + '/../' + np_whl) or not os.path.isfile(repo + '/../' + sp_whl):
        raise RuntimeError("Build succeeded, but expected wheels not found!")
    shutil.move(repo + "/../" + np_whl, repo + "/numpy/" + np_whl)
    shutil.move(repo + "/../" + sp_whl, repo + "/scipy/" + sp_whl)
    print("Generated new " + np_whl + " and " + sp_whl + " pypy wheels")

