# import pytest  # type: ignore
#
# from kodiak.submission import SubmissionFile
# from pathlib import Path
#
#
# @pytest.fixture
# def file():
#     name = "13394-80551 - Charlie Brown - Mar 29, 2018 1205 PM - CBrown - Homework 6.zip"
#     return SubmissionFile(Path(name))
#
#
# def test_file_submmited_filename(file):
#     assert file.submitted_filename == "CBrown - Homework 6.zip"
#
#
# def test_student_submission_id(file):
#     assert file.student_submission_id == "13394-80551"
#
#
# def test_student_first_name(file):
#     assert file.student_first_name == "Charlie"
#
#
# def test_last_name(file):
#     assert file.student_last_name == "Brown"
#
#
# def test_datetime(file):
#     assert file.datetime is not None
