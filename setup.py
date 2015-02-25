from __future__ import with_statement
import os.path

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup


PACKAGE = 'efcorps'
ROOTDIR = os.path.dirname(os.path.abspath(__file__))


def get_long_description():
    """Retrieve long distribution description from README.txt, if available."""
    try:
        return open('README.txt').read()
    except IOError:
        return None


def get_requirements(name):
    with open(os.path.join(ROOTDIR, 'requirements', name + '.txt')) as fh:
        return fh.read().splitlines()


setup(
    name=PACKAGE,
    description="Shared models for various Edgeflip repos",
    long_description=get_long_description(),
    version='0.1',
    packages=['magnus'],
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
