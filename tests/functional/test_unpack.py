from kodiak.__main__ import unpack
from click.testing import CliRunner  # type: ignore  # noqa: F401


def test_unpack_no_opts(temp_path, archive_file):
    run_kodiak_unpack(temp_path, archive_file, 'h4', duplicates=None)
    h4 = temp_path / 'h4'
    assert listdir(h4) == ['.kodiak', 'Brown_Charlie', 'Pelt_Lucy']
    assert listdir(h4 / 'Brown_Charlie' / 'CharlieB_HW4') == ['x', 'y', 'z']
    assert listdir(h4 / 'Brown_Charlie' / 'CharlieB_HW4' / 'z') == ['q']
    assert listdir(h4 / 'Pelt_Lucy') == ['LPelt_HW4 (1).pdf', 'LPelt_HW4 (2).pdf', 'LPelt_HW4.pdf']


def test_unpack_duplicates_number_newest(temp_path, archive_file):
    run_kodiak_unpack(temp_path, archive_file, 'h4', duplicates='number-newer')
    lucy_path = temp_path / 'h4' / 'Pelt_Lucy'
    lpelt_hw4_pdf = lucy_path / 'LPelt_HW4.pdf'
    lpelt_hw4_pdf_2 = lucy_path / 'LPelt_HW4 (2).pdf'
    assert lpelt_hw4_pdf.read_text() == 'oldest'
    assert lpelt_hw4_pdf_2.read_text() == 'newest'


def test_unpack_duplicates_number_older(temp_path, archive_file):
    run_kodiak_unpack(temp_path, archive_file, 'h4', duplicates='number-older')
    lucy_path = temp_path / 'h4' / 'Pelt_Lucy'
    lpelt_hw4_pdf = lucy_path / 'LPelt_HW4.pdf'
    lpelt_hw4_pdf_2 = lucy_path / 'LPelt_HW4 (2).pdf'
    assert lpelt_hw4_pdf.read_text() == 'newest'
    assert lpelt_hw4_pdf_2.read_text() == 'oldest'


def test_unpack_duplicates_keep_newest_only(temp_path, archive_file):
    run_kodiak_unpack(temp_path, archive_file, 'h4', duplicates='newest-only')
    h4 = temp_path / 'h4'
    assert len(listdir(h4 / 'Pelt_Lucy')) == 1
    assert (h4 / 'Pelt_Lucy' / 'LPelt_HW4.pdf').read_text() == 'newest'


def test_unpack_duplicates_keep_oldest_only(temp_path, archive_file):
    run_kodiak_unpack(temp_path, archive_file, 'h4', duplicates='oldest-only')
    h4 = temp_path / 'h4'
    assert len(listdir(h4 / 'Pelt_Lucy')) == 1
    assert (h4 / 'Pelt_Lucy' / 'LPelt_HW4.pdf').read_text() == 'oldest'


def run_kodiak_unpack(temp_path, archive_file, target_dir, duplicates=None):
    args = []
    if duplicates:
        args.append('--duplicates='+duplicates)
    args.extend([archive_file, str(temp_path / target_dir)])
    result = CliRunner().invoke(unpack, args)
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
