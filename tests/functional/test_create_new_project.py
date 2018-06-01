import pathlib
import typing
from tests.functional import runners


def test_no_opts(temp_path: pathlib.Path, archive_file: pathlib.Path) -> None:
    runners.run_kodiak_init(temp_path, archive_file, 'h4', duplicates=None)
    h4 = temp_path / 'h4'
    subs = h4/'submissions'
    assert listdir(subs) == ['Brown_Charlie', 'Pelt_Lucy']
    assert listdir(subs/'Brown_Charlie'/'CharlieB_HW4') == ['x', 'y', 'z']
    assert listdir(subs/'Brown_Charlie'/'CharlieB_HW4'/'z') == ['q']
    assert listdir(subs/'Pelt_Lucy') == ['LPelt_HW4 (1).pdf', 'LPelt_HW4 (2).pdf', 'LPelt_HW4.pdf']
    assert (h4/'.kodiak'/'sourceTargetMapping').exists()
    lucy_path = temp_path / 'h4' / 'submissions' / 'Pelt_Lucy'
    lpelt_hw4_pdf = lucy_path / 'LPelt_HW4.pdf'
    lpelt_hw4_pdf_2 = lucy_path / 'LPelt_HW4 (2).pdf'
    assert lpelt_hw4_pdf.read_text() == 'newest'
    assert lpelt_hw4_pdf_2.read_text() == 'oldest'


def test_duplicates_number_newest(temp_path: pathlib.Path, archive_file: pathlib.Path) -> None:
    runners.run_kodiak_init(temp_path, archive_file, 'h4', duplicates='number-newer')
    lucy_path = temp_path / 'h4' / 'submissions' / 'Pelt_Lucy'
    lpelt_hw4_pdf = lucy_path / 'LPelt_HW4.pdf'
    lpelt_hw4_pdf_2 = lucy_path / 'LPelt_HW4 (2).pdf'
    assert lpelt_hw4_pdf.read_text() == 'oldest'
    assert lpelt_hw4_pdf_2.read_text() == 'newest'


def test_duplicates_number_older(temp_path: pathlib.Path, archive_file: pathlib.Path) -> None:
    runners.run_kodiak_init(temp_path, archive_file, 'h4', duplicates='number-older')
    lucy_path = temp_path / 'h4' / 'submissions' / 'Pelt_Lucy'
    lpelt_hw4_pdf = lucy_path / 'LPelt_HW4.pdf'
    lpelt_hw4_pdf_2 = lucy_path / 'LPelt_HW4 (2).pdf'
    assert lpelt_hw4_pdf.read_text() == 'newest'
    assert lpelt_hw4_pdf_2.read_text() == 'oldest'


def test_duplicates_keep_newest_only(temp_path: pathlib.Path, archive_file: pathlib.Path) -> None:
    runners.run_kodiak_init(temp_path, archive_file, 'h4', duplicates='newest-only')
    lucyDir = temp_path / 'h4' / 'submissions' / 'Pelt_Lucy'
    assert len(listdir(lucyDir)) == 1
    assert (lucyDir / 'LPelt_HW4.pdf').read_text() == 'newest'


def test_duplicates_keep_oldest_only(temp_path: pathlib.Path, archive_file: pathlib.Path) -> None:
    runners.run_kodiak_init(temp_path, archive_file, 'h4', duplicates='oldest-only')
    lucyDir = temp_path / 'h4' / 'submissions' / 'Pelt_Lucy'
    assert len(listdir(lucyDir)) == 1
    assert (lucyDir / 'LPelt_HW4.pdf').read_text() == 'oldest'


def listdir(path: pathlib.Path) -> typing.List[str]:
    return sorted([f.name for f in path.iterdir()])
