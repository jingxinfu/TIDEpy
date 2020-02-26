#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author            : Jingxin Fu <jingxinfu.tj@gmail.com>
# Date              : 26/02/2020
# Last Modified Date: 26/02/2020
# Last Modified By  : Jingxin Fu <jingxinfu.tj@gmail.com>
import setuptools
from tidepy import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tidepy",
    version=__version__,
    author="Jingxin Fu",
    author_email="jingxinfu.tj@gmail.com",
    description="A computational method to predict immunotherapy response.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://jingxinfu.github.io/TIDEpy",
    packages=setuptools.find_packages(),
    scripts=['bin/tidepy'],
    package_data={'tidepy': ["data/*.pkl"],},
    include_package_data=True,
    install_requires=['pandas','numpy'],
    python_requires='>=3.4, <4',
    keywords= ['Immunotherapy', 'ICB Prediction','Biomarkers',
          'Bioinformatics', 'Computational Biology'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ]
)
