import kodiak

def test_file_name_with_separator_in_file_name():
    name = "13394-80551 - Eric Gillotti - Mar 29, 2018 1205 PM - EGillotti - Homework 6.zip"
    parts = kodiak.parse_submission_file_name(name)
    assert parts.file_name == "EGillotti - Homework 6.zip"

def test_submission_id():
    name = "13394-80551 - Eric Gillotti - Mar 29, 2018 1205 PM - EGillotti - Homework 6.zip"
    parts = kodiak.parse_submission_file_name(name)
    assert parts.submission_id == "13394-80551"

def test_first_name():
    name = "13394-80551 - Eric Gillotti - Mar 29, 2018 1205 PM - EGillotti - Homework 6.zip"
    parts = kodiak.parse_submission_file_name(name)
    assert parts.first_name == "Eric"

def test_last_name():
    name = "13394-80551 - Eric Gillotti - Mar 29, 2018 1205 PM - EGillotti - Homework 6.zip"
    parts = kodiak.parse_submission_file_name(name)
    assert parts.last_name == "Gillotti"

def test_submission_date_time():
    name = "13394-80551 - Eric Gillotti - Mar 29, 2018 1205 PM - EGillotti - Homework 6.zip"
    parts = kodiak.parse_submission_file_name(name)
    assert parts.date_time == "Mar 29, 2018 1205 PM"
