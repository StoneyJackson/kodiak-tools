from click.testing import CliRunner  # type: ignore  # noqa: F401
import pytest  # type: ignore  # noqa: F401
import os
import shutil

from kodiak.__main__ import unpack


FUNCTIONAL_TEST_DIR = os.path.dirname(__file__)
TEMP_DIR = os.path.join(FUNCTIONAL_TEST_DIR, 'temp')
FIXTURES_DIR = os.path.join(FUNCTIONAL_TEST_DIR, 'fixtures')


def setup_function(function):
    os.makedirs(TEMP_DIR, exist_ok=True)


def teardown_function(function):
    shutil.rmtree(TEMP_DIR)


@pytest.fixture
def archive_file():
    root = 'Homework 4 Download May 25, 2018 1118 AM'
    mkdir(root)
    mkdir(root, 'HW4')
    mkfile(root, 'HW4', 'x')
    mkfile(root, 'HW4', 'y')
    mkdir(root, 'HW4', 'z')
    mkfile(root, 'HW4', 'z', 'q')
    archive(
        [root, 'HW4'],
        [root, '11690-66708 - Charlie Brown - Feb 9, 2017 614 PM - CharlieB_HW4']
    )
    rmdir(root, 'HW4')
    mkfile(root, '11824-66708 - Lucy Pelt - Feb 9, 2017 1004 PM - LPelt_HW4.pdf', contents='oldest')
    mkfile(root, '11824-66708 - Lucy Pelt - Feb 9, 2017 1007 PM - LPelt_HW4.pdf', contents='middle')
    mkfile(root, '11824-66708 - Lucy Pelt - Feb 9, 2017 1017 PM - LPelt_HW4.pdf', contents='newest')
    archive([root], [root])
    return intemp(root + '.zip')


def test_unpack_no_opts(archive_file):
    result = CliRunner().invoke(unpack, [archive_file, intemp('h4')])
    print(result.output)
    checkCliRunnerErrors(result)

    assert listdir('h4') == ['.kodiak', 'Brown_Charlie', 'Pelt_Lucy']
    assert listdir('h4', 'Brown_Charlie', 'CharlieB_HW4') == ['x', 'y', 'z']
    assert listdir('h4', 'Brown_Charlie', 'CharlieB_HW4', 'z') == ['q']
    assert listdir('h4', 'Pelt_Lucy') == ['LPelt_HW4 (1).pdf', 'LPelt_HW4 (2).pdf', 'LPelt_HW4.pdf']


def test_unpack_duplicates_number_newest(archive_file):
    result = CliRunner().invoke(unpack, ['--duplicates=number-newer', archive_file, intemp('h4')])
    print(result.output)
    checkCliRunnerErrors(result)

    with open(intemp('h4', 'Pelt_Lucy', 'LPelt_HW4.pdf')) as f:
        assert f.read() == 'oldest'

    with open(intemp('h4', 'Pelt_Lucy', 'LPelt_HW4 (2).pdf')) as f:
        assert f.read() == 'newest'


def test_unpack_duplicates_number_older(archive_file):
    result = CliRunner().invoke(unpack, ['--duplicates=number-older', archive_file, intemp('h4')])
    print(result.output)
    checkCliRunnerErrors(result)

    with open(intemp('h4', 'Pelt_Lucy', 'LPelt_HW4.pdf')) as f:
        assert f.read() == 'newest'

    with open(intemp('h4', 'Pelt_Lucy', 'LPelt_HW4 (2).pdf')) as f:
        assert f.read() == 'oldest'


def test_unpack_duplicates_keep_newest_only(archive_file):
    result = CliRunner().invoke(unpack, ['--duplicates=newest-only', archive_file, intemp('h4')])
    print(result.output)
    checkCliRunnerErrors(result)

    assert len(listdir('h4', 'Pelt_Lucy')) == 1

    result_mtime = os.stat(intemp('h4', 'Pelt_Lucy', 'LPelt_HW4.pdf')).st_mtime

    import datetime
    result_str = datetime.datetime.fromtimestamp(
        result_mtime
    ).strftime('%b %-d, %Y %I%M')
    assert result_str == 'Feb 9, 2017 1017'


def test_unpack_duplicates_keep_oldest_only(archive_file):
    result = CliRunner().invoke(unpack, ['--duplicates=oldest-only', archive_file, intemp('h4')])
    print(result.output)
    checkCliRunnerErrors(result)

    assert len(listdir('h4', 'Pelt_Lucy')) == 1

    result_mtime = os.stat(intemp('h4', 'Pelt_Lucy', 'LPelt_HW4.pdf')).st_mtime

    import datetime
    result_str = datetime.datetime.fromtimestamp(
        result_mtime
    ).strftime('%b %-d, %Y %I%M')
    assert result_str == 'Feb 9, 2017 1004'


def checkCliRunnerErrors(result):
    if result.exit_code != 0:
        if result.exception:
            import traceback
            traceback.print_tb(result.exception.__traceback__)
            print(result.exception)
        assert False


def mkdir(*args):
    os.mkdir(intemp(*args))


def mkfile(*args, contents=''):
    with open(intemp(*args), 'w') as f:
        f.write(contents)


def intemp(*args):
    return join(TEMP_DIR, *args)


def join(*args):
    return os.sep.join(args)


def archive(src_dir, target_sans_extension):
    shutil.make_archive(intemp(*target_sans_extension), 'zip', intemp(*src_dir))


def rmdir(*args):
    shutil.rmtree(intemp(*args))


def listdir(*args):
    return sorted(os.listdir(intemp(*args)))
