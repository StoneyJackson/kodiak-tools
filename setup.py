import sys
from setuptools import setup, find_packages  # type: ignore


if not (sys.version_info.major == 3 and sys.version_info.minor >= 6):
    sys.exit("Sorry, requires Python 3.6+.")


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='Kodiak Tools',
    version='0.1.0.dev0',
    license='GPLv3',
    long_description=long_description,
    packages=find_packages('src'),
    package_dir={
        '': 'src',
    },
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'kodiak = kodiak.kodiak:main',
        ]
    },
)
