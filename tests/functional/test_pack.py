from kodiak.__main__ import pack
from kodiak.__main__ import unpack
from click.testing import CliRunner  # type: ignore  # noqa: F401
import shutil


def run_kodiak_unpack(temp_path, archive_file, target_dir, duplicates=None):
    args = []
    if duplicates:
        args.append('--duplicates='+duplicates)
    args.extend([archive_file, str(temp_path / target_dir)])
    result = CliRunner().invoke(unpack, args)
    checkCliRunnerErrors(result)


def run_kodiak_pack(temp_path, target_dir):
    result = CliRunner().invoke(pack, [str(temp_path / target_dir)])
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


def test_pack_from_oldest_only(temp_path, archive_file):
    run_kodiak_unpack(temp_path, archive_file, 'h4', duplicates='oldest-only')

    pelt = temp_path / 'h4' / 'Pelt_Lucy' / 'LPelt_HW4.pdf'
    pelt.write_text('feedback')

    run_kodiak_pack(temp_path, 'h4')

    new_archive = (temp_path / 'h4' / 'Homework 4 Download May 25, 2018 1118 AM.zip')
    h4_1 = temp_path / 'h4_1'
    shutil.unpack_archive(str(new_archive), str(h4_1))
    pelt = h4_1 / '11824-66708 - Lucy Pelt - Feb 9, 2017 1004 PM - LPelt_HW4.pdf'
    assert pelt.read_text() == 'feedback'
