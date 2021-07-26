#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

# read version.py
import sys, re

try:
    filepath = "ScreenshotMaker/version.py"
    version_file = open(filepath)
    (__version__,) = re.findall('__version__ = "(.*)"', version_file.read())

except Exception as error:
    __version__ = "0.0.1"
    sys.stderr.write("Warning: Could not open '%s' due %s\n" % (filepath, error))

requirements = [
    "numpy==1.19.2",
    "SimpleITK==1.2.4",
    "pytest",
    "coverage",
    "psutil",
    "medcam",
    "black",
]

setup(
    name="ScreenshotMaker",
    version=__version__,
    author="Sarthak Pati",  # alphabetical order
    author_email="software@cbica.upenn.edu",
    python_requires=">=3.6",
    packages=find_packages(),
    scripts=["screenshot_run"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description=("Making screenshots for presentations and manuscripts."),
    install_requires=requirements,
    license="BSD-3-Clause License",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="medical-imaging, screenshot",
    zip_safe=False,
)
