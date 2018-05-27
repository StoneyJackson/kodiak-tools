from kodiak import kodiak


NAME = "13394-80551 - Charlie Brown - Mar 29, 2018 1205 PM - CBrown - Homework 6.zip"  # noqa: E501


def test_file_name_with_separator_in_file_name():
    parts = kodiak.parse_submission_file_name(NAME)
    assert parts.file_name == "CBrown - Homework 6.zip"


def test_submission_id():
    parts = kodiak.parse_submission_file_name(NAME)
    assert parts.submission_id == "13394-80551"


def test_first_name():
    parts = kodiak.parse_submission_file_name(NAME)
    assert parts.first_name == "Charlie"


def test_last_name():
    parts = kodiak.parse_submission_file_name(NAME)
    assert parts.last_name == "Brown"


def test_submission_date_time():
    from datetime import datetime
    parts = kodiak.parse_submission_file_name(NAME)
    assert parts.date_time == datetime.strptime("Mar 29, 2018 1205 PM", '%b %d, %Y %I%M %p')
