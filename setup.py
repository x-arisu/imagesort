# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="imagesort",
    version="1.0.0",
    description="A pip package",
    license="GNU GPL v3",
    author="ArisuTheWired",
    packages=['imagesort'],
    install_requires=[],
    long_description=long_description,
    entry_points={
        'console_scripts': [
            'imagesort=imagesort:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
    ]
)
