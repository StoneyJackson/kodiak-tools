import shutil
from tests.functional.runners import run_kodiak_unpack, run_kodiak_pack


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
