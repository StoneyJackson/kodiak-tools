import sys
import click
from pathlib import Path
from kodiak.unpack import UnpackCommand


if not (sys.version_info.major == 3 and sys.version_info.minor >= 6):
    sys.exit("Requires Python 3.6+")


@click.group()
def main():
    pass


@main.command()
@click.argument('archive_file')
@click.argument('directory')
@click.option('--keep-all', is_flag=True, help='''By default, keeps only the most recent submission
of each file with the same name per student. This option will keep all copies by appending an
integer to the end of the name of each duplicate file (e.g., "file (1).pdf").''')
def unpack(archive_file, directory, keep_all):
    archiveFile = Path(archive_file)
    projectDirectory = Path(directory)
    UnpackCommand(archiveFile, projectDirectory, keep_all).unpack()


if __name__ == '__main__':
    main()
