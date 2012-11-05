#!/usr/bin/env python
""" Setup file for pgpass package """

from distutils.core import setup
import os
from os.path import abspath, dirname, join


readme = open(join(dirname(abspath(__file__)),'README.rst')).read()



def is_package(path):
    return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, '__init__.py'))
    )


def find_packages(path, base=""):
    """ Find all packages in path """
    packages = {}
    for item in os.listdir(path):
        dir = os.path.join(path, item)
        if is_package(dir):
            if base:
                module_name = "%(base)s.%(item)s" % vars()
            else:
                module_name = item
            packages[module_name] = dir
            packages.update(find_packages(dir, module_name))
    return packages

setup(name='pgpass',
      version='0.0.2',
      description='utils for work with ~/.pgpass PostgreSQL',
      long_description=readme,
      author='cancerhermit',
      author_email='cancerhermit@gmail.com',
      url='http://github.com/cancerhermit/py-pgpass/',
      install_requires=[''],
      packages = find_packages(".").keys(),
      classifiers=(
          'Environment :: Console',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Programming Language :: Python',
        ),
      license="GPL"
     )