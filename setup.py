from __future__ import annotations

from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

setup(
    name="hcloud",
    version="2.1.1",
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
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "python-dateutil>=2.7.5",
        "requests>=2.20",
    ],
    extras_require={
        "docs": [
            "sphinx>=7.4,<7.5",
            "sphinx-rtd-theme>=2,<2.1",
            "myst-parser>=3,<3.1",
            "watchdog>=4,<4.1",
        ],
        "test": [
            "coverage>=7.6,<7.7",
            "pylint>=3,<3.3",
            "pytest>=8,<8.4",
            "pytest-cov>=5,<5.1",
            "mypy>=1.11,<1.12",
            "types-python-dateutil",
            "types-requests",
        ],
    },
    include_package_data=True,
    packages=find_packages(exclude=["examples", "tests*", "docs"]),
    zip_safe=False,
)
