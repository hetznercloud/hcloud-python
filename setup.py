from __future__ import annotations

from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

version = {}
with open("hcloud/__version__.py", encoding="utf-8") as fp:
    exec(fp.read(), version)

setup(
    name="hcloud",
    version=version["VERSION"],
    keywords="hcloud hetzner cloud",
    description="Official Hetzner Cloud python library",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Hetzner Cloud GmbH",
    author_email="support-cloud@hetzner.com",
    url="https://github.com/hetznercloud/hcloud-python",
    project_urls={
        "Bug Tracker": "https://github.com/hetznercloud/hcloud-python/issues",
        "Documentation": "https://hcloud-python.readthedocs.io/en/stable/",
        "Changelog": "https://github.com/hetznercloud/hcloud-python/blob/main/CHANGELOG.md",
        "Source Code": "https://github.com/hetznercloud/hcloud-python",
    },
    license="MIT license",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "python-dateutil>=2.7.5",
        "requests>=2.20",
    ],
    extras_require={
        "docs": [
            "sphinx>=7.2.2,<7.3",
            "sphinx-rtd-theme>=1.3.0,<1.4",
            "myst-parser>=2.0.0,<2.1",
            "watchdog>=3.0.0,<3.1",
        ],
        "test": [
            "coverage>=7.3,<7.4",
            "pylint>=2.17.4,<2.18",
            "pytest>=7.4,<7.5",
            "mypy>=1.5,<1.6",
            "types-python-dateutil",
            "types-requests",
        ],
    },
    include_package_data=True,
    packages=find_packages(exclude=["examples", "tests*", "docs"]),
    zip_safe=False,
)
