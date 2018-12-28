#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    changelog = changelog_file.read()

requirements = []

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

version = {}
with open("hcloud/version.py") as fp:
    exec(fp.read(), version)

setup(
    author="Hetzner Cloud GmbH",
    author_email='support-cloud@hetzner.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Official Hetzner Cloud python library",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + changelog,
    include_package_data=True,
    keywords='hcloud',
    name='hcloud',
    packages=find_packages(exclude=["examples", "tests"]),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/hetznercloud/hcloud-python',
    version=version['VERSION'],
    zip_safe=False,
)
