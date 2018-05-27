from pathlib import Path
from datetime import datetime
import time


class SubmissionFile:
    def __init__(self, path: Path):
        self.path = path
        setattrs(self, parse_submission_filename(path.name))
        self.datetime = makeDatetime(str.datetime_str)
        self.datetime_total_seconds = calculateTotalSeconds(self.datetime)


def parse_submission_filename(name: str) -> Dict[str, str]:
    result = {}
    parts = name.split(' - ', maxsplit=3)
    first, last = parts[1].split(' ')
    result['student_submission_id'] = parts[0]
    result['student_first_name'] = first
    result['student_last_name'] = last
    result['datetime_str'] =  parts[2]
    result['submitted_filename'] = parts[3]
    return result


def setattrs(object, dictionary):
    for k, v in dictionary.items():
        setattr(object, k, v)


def makeDatetime(s: str) -> datetime:
    # Kodiak runs together hours and minutes. Split them up so that
    # we can use strptime to parse and create a datetime object.
    minutes = s[-5:-3]
    hours = s[-7:-5]
    s = s[:-7] + hours + ' ' + minutes + s[-3:]
    return datetime.strptime(s, '%b %d, %Y %I %M %p')


def calculateTotalSeconds(dt: datetime) -> int:
    return (dt - datetime(1970, 1, 1)).total_seconds() + time.timezone
