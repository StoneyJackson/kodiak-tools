import sys
import click
from pathlib import Path
from kodiak.unpack import UnpackCommand
from kodiak.pack import PackCommand


if not (sys.version_info.major == 3 and sys.version_info.minor >= 6):
    sys.exit("Requires Python 3.6+")


@click.group()
def main():
    pass


@main.command()
@click.argument(
    'archive_file',
    type=click.Path(
        exists=True,
        dir_okay=False,
        readable=True,
        allow_dash=False,
        resolve_path=True
    )
)
@click.argument(
    'directory',
    type=click.Path(
        exists=False,
        file_okay=False,
        writable=True,
        readable=True,
        allow_dash=False,
        resolve_path=True
    )
)
@click.option(
    '--duplicates',
    type=click.Choice(['number-newer', 'newest-only', 'oldest-only', 'number-older']),
    default='number-newer',
    help='How to handle duplicate submissions.'
)
def unpack(archive_file, directory, duplicates):
    '''Unpack ARCHIVE_FILE into DIRECTORY.

    OVERVIEW

    A student directory is created for each student in DIRECTORY.
    Student directories have the form <LASTNAME>_<FIRSTNAME>.
    Each student's submissions are placed into their student directory.

    DUPLICATES

    Submission files are renamed to the name the student gave the file before uploading to Kodiak.
    If a student resubmits the same file (or another file with the same name) there will be
    duplicates that must be handled. By default kodiak will append (k) to the k_th duplicate file
    in order from oldest to newest in submission time. For example, if a student submits
    hw2.txt five times, the first submission is hw2.txt, the next is hw2 (1).txt, ..., the most
    recent is hw2 (4).txt. You can control how kodiak handles duplicates by passing one of the
    following values using the --duplicates option:

        number-newer\t(default) Number duplicates from oldest to newest.

        number-older\tNumber duplicates from newest to oldest.

        oldest-only\tKeep only the oldest.

        newest-only\tKeep only the newest.
    '''
    archiveFile = Path(archive_file)
    projectDirectory = Path(directory)
    UnpackCommand(archiveFile, projectDirectory, duplicates).unpack()


@main.command()
@click.argument(
    'DIRECTORY',
    type=click.Path(
        exists=True,
        file_okay=False,
        writable=True,
        readable=True,
        allow_dash=False,
        resolve_path=True
    )
)
def pack(directory):
    '''Pack graded DIRECTORY into archive.'''
    PackCommand(Path(directory)).pack()


if __name__ == '__main__':
    main()
