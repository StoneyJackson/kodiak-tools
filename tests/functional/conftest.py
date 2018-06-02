import pathlib
import shutil
import typing

import pytest  # type: ignore


@pytest.fixture
def temp_path() -> typing.Generator[pathlib.Path, None, None]:
    t = pathlib.Path(__file__).parent / 'temp'
    t.mkdir(exist_ok=True)
    yield t
    shutil.rmtree(t)


@pytest.fixture
def archive_file(temp_path: pathlib.Path) -> str:
    archive_path = generate_homework_archive(
        temp_path,
        'Homework 4 Download May 25, 2018 1118 AM',
        [
            ('11690-66708 - Charlie Brown - Feb 9, 2017 614 PM - CharlieB_HW4', 'archive', ''),
            ('11824-66708 - Lucy Pelt - Feb 9, 2017 1004 PM - LPelt_HW4.pdf', 'file', 'oldest'),
            ('11824-66708 - Lucy Pelt - Feb 9, 2017 1007 PM - LPelt_HW4.pdf', 'file', 'middle'),
            ('11824-66708 - Lucy Pelt - Feb 9, 2017 1017 PM - LPelt_HW4.pdf', 'file', 'newest'),
            ('index.html', 'file', 'index')
        ]
    )
    return str(archive_path)


def generate_homework_archive(
    temp_path: pathlib.Path,
    target_name_str: str,
    submission_descs: typing.List[typing.Tuple[str, str, str]]
) -> pathlib.Path:
    target_path = temp_path / target_name_str
    for name, type, content in submission_descs:
        if type == 'file':
            mkfile(target_path/name).write_text(content)
        if type == 'archive':
            mk_archive_submission(temp_path, target_path/name)
    archive = mkarchive(target_path, target_path)
    rmtree(target_path)
    return archive


def mk_archive_submission(
        temp_path: pathlib.Path,
        target_path: pathlib.Path
) -> pathlib.Path:
    cb_path = mkdir(temp_path/'cb')
    mkfile(cb_path/'x')
    mkfile(cb_path/'y')
    z_path = mkdir(cb_path/'z')
    mkfile(z_path/'q')
    mkarchive(target_path, cb_path)
    rmtree(cb_path)
    return target_path


def mkdir(path: pathlib.Path) -> pathlib.Path:
    path.mkdir()
    return path


def mkfile(path: pathlib.Path) -> pathlib.Path:
    path.touch()
    return path


def mkarchive(dest_path: pathlib.Path, src_path: pathlib.Path) -> pathlib.Path:
    shutil.make_archive(str(dest_path), 'zip', str(src_path))
    return dest_path.with_suffix('.zip')


def rmtree(path: pathlib.Path) -> None:
    shutil.rmtree(path)
