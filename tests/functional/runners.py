# from kodiak.__main__ import pack
from kodiak.__main__ import unpack
from click.testing import CliRunner  # type: ignore  # noqa: F401
import traceback


def run_kodiak_unpack(temp_path, archive_file, target_dir, duplicates=None):
    args = []
    if duplicates:
        args.append('--duplicates='+duplicates)
    args.extend([archive_file, str(temp_path / target_dir)])
    result = CliRunner().invoke(unpack, args)
    checkCliRunnerErrors(result)


# def run_kodiak_pack(temp_path, target_dir):
#     result = CliRunner().invoke(pack, [str(temp_path / target_dir)])
#     checkCliRunnerErrors(result)


def checkCliRunnerErrors(result):
    print(result.output)
    if result.exit_code != 0:
        if result.exception:
            traceback.print_tb(result.exception.__traceback__)
            print(result.exception)
        assert False
