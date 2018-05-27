# Kodiak Tools

Kodiak Tools provides a CLI to help instructors manage assignment archives for grading.

Requires Python 3.6+.

## Getting Started

### Installing

1. Download current stable release from [URL]
2. Rename file to kodiak.
3. Make kodiak exectuable and move it into a folder that's in your system's path.

### Running

```
kodiak --help
```

## Developing

### Installing development environment

1. Install GNU make
2. `git clone [URL]`
3. `cd kodiak-tools`
4. `pipenv --3.6`
5. `pipenv install`
6. `pipenv install --dev`

### Testing

`make clean ; make test`
