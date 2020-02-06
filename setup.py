import setuptools
from TIDE import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TIDE",
    version=__version__,
    author="Jingxin Fu",
    author_email="jingxinfu.tj@gmail.com",
    description="A computational method to predict immunotherapy response.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jingxinfu/TIDEpy",
    packages=setuptools.find_packages(),
    scripts=['bin/TIDE'],
    package_data={'TIDEpy': ["data/*.pkl"],},
    include_package_data=True,
    install_requires=['pandas','numpy'],
    python_requires='>=2.7, <4',
    keywords= ['Immunotherapy', 'ICB Prediction','Biomarkers',
          'Bioinformatics', 'Computational Biology'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ]
)
