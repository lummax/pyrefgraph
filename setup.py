# coding=utf-8
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reference_graph",
    version="0.0.1",
    author="lummax",
    description="Trace python object usages as a reference graph.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lummax/pyrefgraph",
    packages=["reference_graph"],
    install_requires=["typing", "pathlib"],
    tests_require=["pytest"],
    extras_require={
        "dev": [
            "pytest",
            "black; python_version >= '3.6'",
            "mypy; python_version >= '3.6'",
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ),
    entry_points={"console_scripts": ["pyrefgraph=reference_graph.config:main"]},
)
