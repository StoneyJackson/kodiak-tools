import pathlib  # type: ignore
import pytest  # type: ignore
import shutil
from kodiak.__main__ import pack
from kodiak.__main__ import unpack

from click.testing import CliRunner  # type: ignore  # noqa: F401


TEMP_PATH = pathlib.Path(__file__).parent / 'temp'


def setup_function(function):
    TEMP_PATH.mkdir(exist_ok=True)


def teardown_function(function):
    shutil.rmtree(TEMP_PATH)


@pytest.fixture
def archive_file():
    archive_path = generate_homework_archive(
        'Homework 4 Download May 25, 2018 1118 AM', [
            ('11690-66708 - Charlie Brown - Feb 9, 2017 614 PM - CharlieB_HW4', 'archive', ''),
            ('11824-66708 - Lucy Pelt - Feb 9, 2017 1004 PM - LPelt_HW4.pdf', 'file', 'oldest'),
            ('11824-66708 - Lucy Pelt - Feb 9, 2017 1007 PM - LPelt_HW4.pdf', 'file', 'middle'),
            ('11824-66708 - Lucy Pelt - Feb 9, 2017 1017 PM - LPelt_HW4.pdf', 'file', 'newest'),
        ]
    )
    return str(archive_path)


def generate_homework_archive(target_path, submission_descs):
    target_path = TEMP_PATH / target_path
    for name, type, content in submission_descs:
        if type == 'file':
            mkfile(target_path/name).write_text(content)
        if type == 'archive':
            mk_archive_submission(target_path/name)
    archive = mkarchive(target_path, target_path)
    rmtree(target_path)
    return archive


def mk_archive_submission(target_path):
    cb_path = mkdir(TEMP_PATH/'cb')
    mkfile(cb_path/'x')
    mkfile(cb_path/'y')
    z_path = mkdir(cb_path/'z')
    mkfile(z_path/'q')
    mkarchive(target_path, cb_path)
    rmtree(cb_path)
    return target_path


def mk_file_submission(target_path):
    return mkfile(target_path)


def mkdir(path):
    path.mkdir()
    return path


def mkfile(path):
    path.touch()
    return path


def mkarchive(dest_path, src_path):
    shutil.make_archive(str(dest_path), 'zip', str(src_path))
    return dest_path.with_suffix('.zip')


def rmtree(path):
    shutil.rmtree(path)


def run_kodiak_unpack(archive_file, target_dir, duplicates=None):
    args = []
    if duplicates:
        args.append('--duplicates='+duplicates)
    args.extend([archive_file, str(TEMP_PATH / target_dir)])
    result = CliRunner().invoke(unpack, args)
    checkCliRunnerErrors(result)


def run_kodiak_pack(target_dir):
    result = CliRunner().invoke(pack, [str(TEMP_PATH / target_dir)])
    checkCliRunnerErrors(result)


def checkCliRunnerErrors(result):
    print(result.output)
    if result.exit_code != 0:
        if result.exception:
            import traceback
            traceback.print_tb(result.exception.__traceback__)
            print(result.exception)
        assert False


def listdir(path):
    return sorted([f.name for f in path.iterdir()])


def test_pack_from_oldest_only(archive_file):
    run_kodiak_unpack(archive_file, 'h4', duplicates='oldest-only')

    pelt = TEMP_PATH / 'h4' / 'Pelt_Lucy' / 'LPelt_HW4.pdf'
    pelt.write_text('feedback')

    run_kodiak_pack('h4')

    new_archive = (TEMP_PATH / 'h4' / 'Homework 4 Download May 25, 2018 1118 AM.zip')
    h4_1 = TEMP_PATH / 'h4_1'
    shutil.unpack_archive(str(new_archive), str(h4_1))
    pelt = h4_1 / '11824-66708 - Lucy Pelt - Feb 9, 2017 1004 PM - LPelt_HW4.pdf'
    assert pelt.read_text() == 'feedback'
