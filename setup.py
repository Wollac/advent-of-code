from setuptools import setup, find_packages

from aoc import __version__

setup(
    name='advent-of-code',
    version=__version__,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/Wollac/advent-of-code',
    author='Wolfgang Welz',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment :: Puzzle Games",
    ],
    install_requires=[
        "advent-of-code-data >= 0.8",
        "networkx",
        "numpy >= 1.19",
        "regex",
        "scipy",
    ],
    extras_require={
        'dev': [
            'pytest',
        ]
    },
    packages=find_packages(),
    python_requires='>=3.8',
    entry_points={
        "adventofcode.user": ["wollac = aoc:plugin"],
    },
)
