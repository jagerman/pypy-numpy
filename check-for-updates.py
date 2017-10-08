#!/usr/bin/python3

import json
import requests
import os.path
import shutil
from subprocess import run
from config import pypy, repo

try:
    from packaging.version import parse
except ImportError:
    from pip._vendor.packaging.version import parse

def version(package_name):
    url = "https://pypi.python.org/pypi/{}/json".format(package_name)
    req = requests.get(url)
    data = req.json()
    version = parse('0')
    found = False
    if req.status_code == requests.codes.ok:
        if 'releases' in data:
            releases = data['releases']
            for release in data['releases']:
                ver = parse(release)
                if not ver.is_prerelease:
                    version = max(version, ver)
                    found = True

    if not found:
        raise RuntimeError("Could not find latest stable version of {}".format(package_name))
    return str(version)

vnp, vsp = version("numpy"), version("scipy")

for pypy_v, pypy_wheel_suffix in pypy.items():
    np_whl = 'numpy-' + vnp + pypy_wheel_suffix
    sp_whl = 'scipy-' + vsp + pypy_wheel_suffix
    if not os.path.isfile(repo + '/numpy/' + np_whl) or not os.path.isfile(repo + '/scipy/' + sp_whl):
        print("Numpy and/or scipy wheels outdated or do not exist; building new wheels")
        print("Found current versions: numpy-{}, scipy-{}".format(vnp, vsp))
        run([repo + "/../build-numpy-pypy.sh", pypy_v], check=True)
        if not os.path.isfile(repo + '/../' + np_whl) or not os.path.isfile(repo + '/../' + sp_whl):
            raise RuntimeError("Build succeeded, but expected wheels not found!")
        shutil.move(repo + "/../" + np_whl, repo + "/numpy/" + np_whl)
        shutil.move(repo + "/../" + sp_whl, repo + "/scipy/" + sp_whl)
        print("Generated new " + np_whl + " and " + sp_whl + " pypy wheels")
