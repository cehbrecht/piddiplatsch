#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.md") as history_file:
    history = history_file.read()

requirements = ["Click>=7.0", "pika>=1.3.1"]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Carsten Ehbrecht",
    author_email="ehbrecht@dkrz.de",
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="Demo project for a PID consumer.",
    entry_points={
        "console_scripts": [
            "piddiplatsch=piddiplatsch.cli:main",
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="piddiplatsch",
    name="piddiplatsch",
    packages=find_packages(include=["piddiplatsch", "piddiplatsch.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/cehbrecht/piddiplatsch",
    version="0.1.0",
    zip_safe=False,
)
