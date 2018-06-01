import traceback

import click.testing  # type: ignore

import kodiak.cli


def run_kodiak_init(temp_path, archive_file, target_dir, duplicates=None):
    args = []
    if duplicates:
        args.append('--duplicates='+duplicates)
    args.extend([str(temp_path / target_dir), archive_file])
    result = click.testing.CliRunner().invoke(
        kodiak.cli.init,
        args
    )
    checkCliRunnerErrors(result)


def run_kodiak_archive(temp_path, target_dir):
    project_root = temp_path / target_dir
    result = click.testing.CliRunner().invoke(
        kodiak.cli.archive,
        [f'--project-root={project_root}']
    )
    checkCliRunnerErrors(result)


def checkCliRunnerErrors(result):
    print(result.output)
    if result.exit_code != 0:
        if result.exception:
            traceback.print_tb(result.exception.__traceback__)
            print(result.exception)
        assert False
