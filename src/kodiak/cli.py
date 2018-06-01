import pathlib
import sys

import click

import kodiak.core


if not (sys.version_info.major == 3 and sys.version_info.minor >= 6):
    sys.exit("Requires Python 3.6+")


@click.group()
@click.version_option(kodiak.__VERSION__)
def main() -> None:
    pass


@main.command()
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
@click.argument(
    'archive',
    type=click.Path(
        exists=True,
        dir_okay=False,
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
def init(directory: str, archive: str, duplicates: str) -> None:
    '''Create project in DIRECTORY from ARCHIVE.

OVERVIEW

DIRECTORY is created if it doesn't exist and blessed as a kodiak project (DIRECOTRY/.kodiak).  ARCHIVE is copied into DIRECOTORY/originalArchive and extracted to DIRECTORY/originalSubmissions.  Submission filenames are
demangled and organized into student folders under DIRECTORY/submissions.  If a stdunent the same named file more than once, these duplicates are handeled according to a duplicates strategy.  See section on DUPLICATES STRATEGIES for details.

DUPLICATES STRATEGIES

Use the "--duplicates=STRATEGY" option to specify one of the
strategies listed below.

number-older (default)

    Append (k) to each duplicate file older than the newest file in increasing order of age.  For example,if "foo.txt" was submitted 3 times, using this strategy, the newest will be named "foo.txt", the next oldest "foo (1).txt", and the oldest "foo (2).txt".  This is the default assuming most instructors want easy access to the most recently submitted copy, while still having access to older copies "just in case".

number-newer

    Append (k) to each duplicate file newer than the oldest file in decreasing order of age.  For example, if "foo.txt" was submitted 3 times, using this strategy, the oldest will be "foo.txt", the next newest will be "foo (1).txt", and the newest will be "foo (2).txt".  This strategy more closely mimics how modern filesystems will number files.  The newer files get the decoration.

oldest-only

    Keep only the oldest copy.  The newer copies will remain in the original archive, and will appear in the final graded archive.  But they will not appear in the working submissions directory.

newest-only

    Keep only the newest copy.  The older copies will remain in the original archive, and will appear in the final graded archive.  But they will not appear in the working submissions directory.
    '''
    archiveFile = pathlib.Path(archive)
    projectDirectory = pathlib.Path(directory)

    importer = {
        'number-newer': kodiak.core.IMPORT_NUMBERING_NEWER,
        'number-older': kodiak.core.IMPORT_NUMBERING_OLDER,
        'oldest-only': kodiak.core.IMPORT_OLDEST_ONLY,
        'newest-only': kodiak.core.IMPORT_NEWEST_ONLY
    }[duplicates]

    if projectDirectory.exists():
        if '.kodiak' in [f.name for f in projectDirectory.iterdir()]:
            raise Exception(f'"{projectDirectory} is already a Kodiak project."')

    click.echo(f'''
Creating kodiak project in {projectDirectory}
Importing {archiveFile}

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

    kodiak.core.Project(projectDirectory).runInitCommand(archiveFile, importer)
    print('Done.')


@main.command()
@click.option(
    '--project-root',
    type=click.Path(
        exists=True,
        file_okay=False,
        writable=True,
        readable=True,
        allow_dash=False,
        resolve_path=True
    ),
    help='Root of project to pack.',
    default='.',
)
def archive(project_root: str) -> None:
    '''Build an archive for Kodiak.

Archive graded and ungraded submissions into a file suitable for upload to Kodiak.
The archive file will be placed in [project_root]/gradedArchive. The files in the archive
will be placed in [project_root]/gradedSubmissions so you may inspect what you are about to
upload.
    '''
    kodiak.core.Project(pathlib.Path(project_root)).runArchiveCommand()


@main.command()
def formats() -> None:
    '''List supported archive formats.

Might include these on your syllabus.
    '''

    click.echo('''
kodiak-tools supports the archive formats listed below. Let your students know.
    ''')

    for format in kodiak.core.get_supported_archive_extensions():
        click.echo(format)

    click.echo('''
If kodiak-tools encounters a submission of a format it doesn't know, it treats it like a normal file and will drop it in [project-root]/submissions.  You may manually extract this file.  When you are done, archive it again using the same format the student used, and delete the extracted contents.  Now `kodiak archive` will include it in the archive for uploading to Kodiak.
    ''')


if __name__ == '__main__':
    main()
