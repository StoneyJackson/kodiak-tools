import pathlib
from datetime import datetime
import time
import os


class SubmissionFile:
    def __init__(self, path: pathlib.Path) -> None:
        self.path = path
        self.suffix = path.suffix
        self.parseIntoAttributes(path.name)
        self.datetime = makeDatetime(self.datetime_str)
        self.datetime_total_seconds = calculateTotalSeconds(self.datetime)

    def parseIntoAttributes(self, name: str) -> None:
        parts = name.split(' - ', maxsplit=3)
        first, last = parts[1].split(' ')
        self.student_submission_id = parts[0]
        self.student_first_name = first
        self.student_last_name = last
        self.datetime_str = parts[2]
        self.submitted_filename = parts[3]

    def fixMtime(self) -> None:
        s = self.datetime_total_seconds
        os.utime(str(self.path), (s, s))


def makeDatetime(s: str) -> datetime:
    # Kodiak runs together hours and minutes. Split them up so that
    # we can use strptime to parse and create a datetime object.
    minutes = s[-5:-3]
    hours = s[-7:-5]
    s = s[:-7] + hours + ' ' + minutes + s[-3:]
    return datetime.strptime(s, '%b %d, %Y %I %M %p')


def calculateTotalSeconds(dt: datetime) -> float:
    return (dt - datetime(1970, 1, 1)).total_seconds() + time.timezone
