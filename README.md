# Kodiak Tools

Kodiak Tools provides a CLI to help instructors manage assignment archives for grading.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

To develop on this project, you'll need the following software installed and available from the
command-line:

1. Python 3.6+
2. pipenv
3. GNU make

### Installing

From the command-line, clone this repository.

```
git clone [url]
```

Change into the project directory.

```
cd kodiak-tools
```

Create a virtual environment for the project using Python 3.6 or higher.

```
pipenv --python 3.6
```

Install all dependencies for development.

```
pipenv install --dev
```

Install the kodiak command into your virtual environment. `-e` will install using
symlinks into src so that changes you make in src will be immediately reflected in the install.

```
pipenv install -e .
```

Now enable the shell and give your development install of kodiak a test drive.

```
pipenv shell
kodiak --help
```

## Running the tests

Build and run the unit and functional tests using make as follows.

```
make clean ; make test
```

To run tests manually check out the test rule in the Makefile.

### Static type checking

`make test` uses mypy to perform static type checking.


### Automated style tests

`make test` uses flake8 to check the style of code. Flake8's configuration is available in .flake8.


## Deployment

1. Download a release from [URL]().
2. Rename it to kodiak, or kodiak.pyz.
3. Make sure it is executable.
4. Run it directly or place it in a folder that is in your systems path.

## Built With

* [click](http://click.pocoo.org/5/) - Framework for building command-line applications
* [zipapp](https://docs.python.org/3/library/zipapp.html) - Packaging into standalone, executable zips
* [pytest](https://docs.pytest.org/en/latest/) - Unit test framework
* [coverage](https://coverage.readthedocs.io/en/coverage-4.5.1/) - Test coverage reports
* [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) - pytest coverage plugin
* [flake8](http://flake8.pycqa.org/en/latest/) - Automated style tests
* [pytest-flake8](https://github.com/tholo/pytest-flake8) - pytest flake8 plugin
* [mypy](http://mypy-lang.org/) - Static type checking
* [pytest-mypy](https://github.com/dbader/pytest-mypy) - pytest mypy plugin
* [pipenv](https://docs.pipenv.org/) - Virtual environment and dependency manager
* [GNU make](https://www.gnu.org/software/make/) - Developer task automation

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* [Stoney Jackson](https://github.com/StoneyJackson)

See also the list of [contributors](https://github.com/StoneyJackson/kodiak-tools/contributors) who participated in this project.

## License

This project is licensed under the GPLv3 - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Hat tip to all the awesome development tools!
