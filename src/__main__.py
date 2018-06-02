'''
This __main__.py is here to satisfy zipapp, which requires a __main__.py
at the top level.
'''
from kodiak import cli


def main() -> None:
    cli.main()


if __name__ == '__main__':
    main()
