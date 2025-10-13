from __future__ import annotations

from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

setup(
    name="hcloud",
    version="2.9.0",  # x-releaser-pleaser-version
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
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    python_requires=">=3.10",
    install_requires=[
        "python-dateutil>=2.7.5",
        "requests>=2.20",
    ],
    extras_require={
        "docs": [
            "sphinx>=8,<8.3",
            "sphinx-rtd-theme>=3,<3.1",
            "myst-parser>=4,<4.1",
            "watchdog>=6,<6.1",
        ],
        "test": [
            "coverage>=7.10,<7.11",
            "pylint>=4,<4.1",
            "pytest>=8,<8.5",
            "pytest-cov>=7,<7.1",
            "mypy>=1.18,<1.19",
            "types-python-dateutil",
            "types-requests",
        ],
    },
    include_package_data=True,
    packages=find_packages(exclude=["examples", "tests*", "docs"]),
    zip_safe=False,
)
