#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.rst") as changelog_file:
    changelog = changelog_file.read()

requirements = ["future>=0.17.1,<1", "python-dateutil>=2.7.5,<3", "requests>=2.20,<3"]

extras_require = {"docs": ["Sphinx==1.8.1", "sphinx-rtd-theme==0.4.2"]}

version = {}
with open("hcloud/__version__.py") as fp:
    exec(fp.read(), version)

setup(
    author="Hetzner Cloud GmbH",
    author_email="support-cloud@hetzner.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires="!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <3.11",
    description="Official Hetzner Cloud python library",
    install_requires=requirements,
    extras_require=extras_require,
    license="MIT license",
    long_description=readme + "\n\n" + changelog,
    include_package_data=True,
    keywords="hcloud hetzner cloud",
    name="hcloud",
    packages=find_packages(exclude=["examples", "tests*", "docs"]),
    test_suite="tests",
    url="https://github.com/hetznercloud/hcloud-python",
    version=version["VERSION"],
    zip_safe=False,
)
