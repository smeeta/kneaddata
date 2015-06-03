import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='knead-datalib',
    version='0.0.1',
    description='',
    packages=['knead_datalib'],
    zip_safe=False,
    install_requires=[
        'biopython'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha"
    ],
    scripts=[os.path.join(here, "knead_data.py")],
    entry_points = {
        "distutils.commands": [
            "trimmomatic = knead_datalib.util:DownloadTrimmomaticCommand"
        ]
    }
)

