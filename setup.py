# Licensed under the Apache License, Version 2.0 (the "License");
# Inspired from https://github.com/google/gemma_pytorch/blob/main/setup.py

import io
import os
from typing import List

import setuptools

ROOT_DIR = os.path.dirname(__file__)


def get_path(*filepath) -> str:
    return os.path.join(ROOT_DIR, *filepath)


def read_readme() -> str:
    """Read the README file."""
    return io.open(get_path("README.md"), "r", encoding="utf-8").read()


def get_requirements() -> List[str]:
    """Get Python package dependencies from requirements.txt."""
    with open(get_path("requirements.txt")) as f:
        requirements = f.read().strip().split("\n")
    return requirements


setuptools.setup(
    name="sales_prediction",
    version="0.1",
    author="All Dataers Group 4",
    license="Apache 2.0",
    url="https://github.com/AllDataers/SalesPredictionGroupe4",
    description=("Groupe 4 Sales Prediction"),
    author_email="alldataers@gmail.com",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Scientific/Engineering :: Machine Learning",
    ],
    packages=setuptools.find_packages(
        where="src",
        exclude=(
            "data",
            "docs",
            "Notebooks",
            "tests",
            "tmp",
            "src/config",
            "src/visualisation",
            "src/models",
        ),
    ),
    python_requires=">=3.8",
    install_requires=get_requirements(),
)
