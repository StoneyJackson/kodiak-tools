import setuptools  # type: ignore
import sys


if not (sys.version_info.major == 3 and sys.version_info.minor >= 6):
    sys.exit("Sorry, requires Python 3.6+.")


with open("README.md", "r") as fh:
    long_description = fh.read()


with open("VERSION", "r") as fh:
    version = fh.read()


setuptools.setup(
    name='Kodiak Tools',
    version=version,
    license='GPLv3',
    long_description=long_description,
    packages=setuptools.find_packages('src'),
    package_dir={
        '': 'src',
    },
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'kodiak = kodiak.cli:main',
        ]
    },
)
