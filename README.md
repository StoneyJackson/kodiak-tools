# Kodiak Tools

Kodiak Tools provides a CLI to help instructors manage assignment archives for grading.

## 1. A Quick Example

Download assignment archive from Kodiak. Then create a kodiak project as follows.

```
$ kodiak init h4 ~/Downloads/Homework\ 4\ Download\ May\ 25\,\ 2018\ 1118\ AM.zip
```

To grade, edit the files under the submissions subfolder of the project.

```
$ cd h4
$ tree submissions/
submissions/
├── Brown_Charlie
│   └── CharlieB_HW4
│       ├── bar.txt
│       ├── foo.txt
│       └── subdir
│           └── baz.txt
└── Pelt_Lucy
    ├── LPelt_HW4\ (1).txt
    ├── LPelt_HW4\ (2).txt
    └── LPelt_HW4.txt
```

When you're done grading, create an archive to upload to Kodiak.

```
$ kodiak archive
$ ls gradedArchive/
Homework 4 Download May 25, 2018 1118 AM.zip
```

Upload the archive in gradedArchive to Kodiak.

## 2. Requirements

Requires Python 3.6 or higher to run.

## 3. Download and Install

1. [Download latest stable release](https://github.com/StoneyJackson/kodiak-tools/releases).

2. Rename it to kodiak, or kodiak.pyz.

    ```
    mv kodiak-tools-[VERSION].pyz kodiak
    ```

3. Make sure it is executable.

    ```
    chmod +x kodiak
    ```

4. Move it to a directory that is in your system's path.

    ```
    mv kodaik ~/bin
    ```

5. Start using kodiak. Start with help.

    ```
    kodiak --help
    kodiak [COMMAND] --help
    ```


## 4. Getting Started as a Developer

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

To develop on this project, you'll need the following software installed and available from the
command-line:

1. Python 3.6+
2. pipenv
3. GNU make
4. [hub](https://github.com/github/hub)

### Installing the Development Environment

1. Fork this repository and clone your fork.


2. In the root of your clone, create a virtual environment for the project using Python 3.6 or higher.

    ```
    pipenv --python 3.6
    ```

3. Install all dependencies for development.

    ```
    pipenv install --dev
    ```

4. Install the kodiak command into your virtual environment. `-e` will install using
symlinks into src so that changes you make in src will be immediately reflected in the install.

    ```
    pipenv install -e .
    ```

5. Now enable the shell and give your development install of kodiak a test drive.

    ```
    pipenv shell
    kodiak --help
    ```

### Running the tests

Run all tests (including style and type checking) as follows.

```
make test
```

### Making a release

This requires `hub` to be installed. Basically this will bumpversions

```
make release
```

## 5. Built With

* [bumpversion](https://github.com/peritus/bumpversion)
* [click](http://click.pocoo.org/5/) - Framework for building command-line applications
* [coverage](https://coverage.readthedocs.io/en/coverage-4.5.1/) - Test coverage reports
* [hub](https://github.com/github/hub)
* [flake8](http://flake8.pycqa.org/en/latest/) - Automated style tests
* [GNU make](https://www.gnu.org/software/make/) - Developer task automation
* [mypy](http://mypy-lang.org/) - Static type checking
* [pytest-mypy](https://github.com/dbader/pytest-mypy) - pytest mypy plugin
* [pipenv](https://docs.pipenv.org/) - Virtual environment and dependency manager
* [pytest](https://docs.pytest.org/en/latest/) - Unit test framework
* [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) - pytest coverage plugin
* [tox](https://tox.readthedocs.io/en/latest/)
* [zipapp](https://docs.python.org/3/library/zipapp.html) - Packaging into standalone, executable zips

## 6. Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## 7. Versioning

We use [RomVer](http://blog.legacyteam.info/2015/12/romver-romantic-versioning/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## 8. Authors

* [Stoney Jackson](https://github.com/StoneyJackson)

See also the list of [contributors](https://github.com/StoneyJackson/kodiak-tools/contributors) who participated in this project.

## 9. License

This project is licensed under the GPLv3 - see the [LICENSE](LICENSE) file for details

## 10. Acknowledgments

* Hat tip to all the awesome development tools!
