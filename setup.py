from __future__ import with_statement
import os.path
import sys

import ez_setup
ez_setup.use_setuptools()

from setuptools import find_packages, setup


PACKAGE = 'efcorps'
ROOTDIR = os.path.dirname(os.path.abspath(__file__))


def get_long_description():
    """Retrieve long distribution description from README.txt, if available."""
    try:
        return open('README.txt').read()
    except IOError:
        return None


def _is_install():
    return len(sys.argv) >= 2 and sys.argv[1] == 'install'


def get_py_modules():
    """Modules to list.

    Don't include `ez_setup` on install.

    """
    if _is_install():
        return []
    return ['ez_setup']


def get_requirements(name):
    with open(os.path.join(ROOTDIR, 'requirements', name + '.txt')) as fh:
        return fh.read().splitlines()


setup(
    name=PACKAGE.title(),
    description="Shared models for various Edgeflip repos",
    long_description=get_long_description(),
    version='0.1',
    py_modules=get_py_modules(),
    packages=find_packages('.'),
    install_requires=get_requirements('base'),
    maintainer="Edgeflip Developers",
    maintainer_email="devs@edgeflip.com",
    url="http://github.com/edgeflip/efcorps",
    license='BSD',
    classifiers=(
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ),
)
