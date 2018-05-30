import sys
import click
import pathlib
from kodiak import core


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
    default='number-older',
    help='How to handle duplicate submissions.'
)
def unpack(archive_file, directory, duplicates):
    '''Unpack ARCHIVE_FILE into DIRECTORY.

OVERVIEW

A student directory is created for each student in DIRECTORY.
Student directories have the form <LASTNAME>_<FIRSTNAME>.
Student submissions are renamed to the name students gave them
before uploading their files to Kodiak. This can create collisions
when unpacking if the same student submits two files with the same
name (i.e., resubmits the same file). See the section on DUPLICATES
STRATEGIES to learn the different strategies offered to handle
duplicates.

DUPLICATES STRATEGIES

Unpack offers four strategies for handling duplicate submissions.
Use the "--duplicates=STRATEGY" option to specify the strategy
unpack should use.

number-older

    (default) Append (k) to each duplicate file older than the newest file in increasing order of age.  For example,if "foo.txt" was submitted 3 times, using this strategy, the newest will be named "foo.txt", the next oldest "foo (1).txt", and the oldest "foo (2).txt".  This is the default assuming most instructors want easy access to the most recently submitted copy, while still having access to older copies "just in case".

number-newer

    Append (k) to each duplicate file newer than the oldest file in decreasing order of age.  For example, if "foo.txt" was submitted 3 times, using this strategy, the oldest will be "foo.txt", the next newest will be "foo (1).txt", and the newest will be "foo (2).txt".  This strategy more closely mimics how modern filesystems will number files.  The newer files get the decoration.

oldest-only

    Keep only the oldest copy.  The newer copies will remain in the original archive, and will appear in the final graded archive.  But they will not appear in the working submissions directory.

newest-only

    Keep only the newest copy.  The older copies will remain in the original archive, and will appear in the final graded archive.  But they will not appear in the working submissions directory.
    '''
    archiveFile = pathlib.Path(archive_file)
    projectDirectory = pathlib.Path(directory)

    importer = {
        'number-newer': core.IMPORT_NUMBERING_NEWER,
        'number-older': core.IMPORT_NUMBERING_OLDER,
        'oldest-only': core.IMPORT_OLDEST_ONLY,
        'newest-only': core.IMPORT_NEWEST_ONLY
    }[duplicates]


    click.echo(f'Importing {archiveFile}')
    click.echo(f'     into {projectDirectory}')
    click.echo(f'''
Using the "{duplicates}" strategy to resolve duplicate
submissions by the same student. For more information

    kodiak unpack --help

If you want a different strategy, delete the project
and run kodiak again specifying your desired strategy. E.g.,

    rm -rf "{projectDirectory}"
    kodiak unpack --duplicates=STRATEGY \\
        "{archiveFile}" \\
        "{projectDirectory}"
''')

    core.Project(projectDirectory).importArchive(archiveFile, importer)
    print('Done.')


# @main.command()
# @click.argument(
#     'DIRECTORY',
#     type=click.Path(
#         exists=True,
#         file_okay=False,
#         writable=True,
#         readable=True,
#         allow_dash=False,
#         resolve_path=True
#     )
# )
# def pack(directory):
#     '''Pack graded DIRECTORY into archive.'''
#     PackCommand(Path(directory)).pack()


if __name__ == '__main__':
    main()
