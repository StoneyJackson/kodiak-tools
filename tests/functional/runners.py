import traceback
import pathlib
import typing

from click.testing import CliRunner, Result  # type: ignore

import kodiak.cli


def run_kodiak_init(
        temp_path: pathlib.Path,
        archive_file: pathlib.Path,
        target_dir: str,
        duplicates: typing.Optional[str]=None
) -> None:
    args = []
    if duplicates is not None:
        args.append('--duplicates='+duplicates)
    args.extend([str(temp_path / target_dir), str(archive_file)])
    result = CliRunner().invoke(
        kodiak.cli.init,
        args
    )
    checkCliRunnerErrors(result)


def run_kodiak_archive(temp_path: pathlib.Path, target_dir: str) -> None:
    project_root = temp_path / target_dir
    result = CliRunner().invoke(
        kodiak.cli.archive,
        [f'--project-root={project_root}']
    )
    checkCliRunnerErrors(result)


def checkCliRunnerErrors(result: Result) -> None:  # type: ignore
    print(result.output)
    if result.exit_code != 0:
        if result.exception:
            traceback.print_tb(result.exception.__traceback__)
            print(result.exception)
        assert False
