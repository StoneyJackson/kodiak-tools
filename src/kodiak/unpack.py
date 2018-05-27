import os
import shutil
import time
from datetime import datetime
from pathlib import Path
from collections import namedtuple


class UnpackCommand:
    def __init__(self, archiveFile: Path, projectDirectory: Path, keep_all: bool) -> None:
        self.archiveFile = archiveFile.resolve()
        self.projectDirectory = projectDirectory.resolve()
        self.setCollisionHandler(keep_all)
        self.definePaths()

    def setCollisionHandler(self, keep_all):
        if keep_all:
            self.collisionHandler = append_number_collision_handler
        else:
            self.collisionHandler = replace_collision_handler

    def definePaths(self):
        self.pathTo = {
            'project': self.projectDirectory,
            'internal': self.projectDirectory / '.kodiak',
            'archive': self.projectDirectory / '.kodiak' / 'archive',
            'extracted archive': self.projectDirectory / '.kodiak' / 'archive-extracted',
        }

    def unpack(self):
        self.createProjectStructure()
        self.importArchive()
        self.extractArchive()
        self.fixMtimesOnSubmissionFiles()
        self.createStudentDirectories()
        self.importStudentSubmissions()

    def createProjectStructure(self):
        print(f"Creating project in {self.pathTo['project']}")
        for p in self.pathTo.values():
            mkdir(p)

    def importArchive(self):
        copy(self.archiveFile, self.pathTo['archive'])

    def extractArchive(self):
        archive = self.getArchive()
        target = self.pathTo['extracted archive']
        unpack_archive(archive, target)

    def getArchive(self):
        return next(self.pathTo['archive'].iterdir())

    def fixMtimesOnSubmissionFiles(self):
        for file in self.getStudentSubmissionFiles():
            parts = parse_submission_file_name(file.name)
            s = parts.date_time_seconds
            os.utime(str(file), (s, s))

    def createStudentDirectories(self):
        for name in self.getStudentNames():
            studentDirectory = self.pathTo['project'] / name
            mkdir(studentDirectory)

    def getStudentNames(self):
        return set([self.getStudentNameFromSubmissionFile(f) for f in self.getStudentSubmissionFiles()])

    def getStudentNameFromSubmissionFile(self, submissionFile: Path):
        n = parse_submission_file_name(submissionFile.name)
        return f'{n.last_name}_{n.first_name}'

    def getStudentSubmissionFiles(self):
        for f in self.pathTo['extracted archive'].iterdir():
            if f.name not in 'index.html . ..'.split():
                yield f

    def importStudentSubmissions(self):
        for file in self.getSubmissionsOrderedOldestToYoungest():
            name = self.getStudentNameFromSubmissionFile(file)
            student = self.pathTo['project'] / name
            unpackedFile = student / self.getFileNameFromSubmissionFile(file)
            if self.isArchive(file):
                unpack_archive(file, unpackedFile.with_name(unpackedFile.stem), self.collisionHandler)
            else:
                copy(file, unpackedFile, self.collisionHandler)

    def getSubmissionsOrderedOldestToYoungest(self):
        submissions = list(self.getStudentSubmissionFiles())
        submissions_parsed = [parse_submission_file_name(str(s)) for s in submissions]
        times = [s.date_time for s in submissions_parsed]
        time_submissions = list(zip(times, submissions))
        time_submissions.sort()     # oldest to youngest
        return [file for time, file in time_submissions]

    def getFileNameFromSubmissionFile(self, submissionFile: Path):
        n = parse_submission_file_name(submissionFile.name)
        return n.file_name

    def isArchive(self, file):
        return file.suffix in get_supported_archive_extensions()


PartsOfSubmissionFileName = namedtuple(
    'PartsOfSubmissionFileName',
    'submission_id first_name last_name date_time date_time_seconds file_name'
)


def parse_submission_file_name(name: str) -> PartsOfSubmissionFileName:
    parts = name.split(' - ', maxsplit=3)
    first, last = parts[1].split(' ')

    # Kodiak runs together hours and minutes. Split them up so that
    # we can use strptime to parse and create a datetime object.
    date_time_str = parts[2]
    minutes = date_time_str[-5:-3]
    hours = date_time_str[-7:-5]
    hours_minutes = hours + ' ' + minutes
    date_time_str = date_time_str[:-7] + hours_minutes + date_time_str[-3:]
    date_time = datetime.strptime(date_time_str, '%b %d, %Y %I %M %p')

    date_time_seconds = (date_time - datetime(1970, 1, 1)).total_seconds() + time.timezone

    return PartsOfSubmissionFileName(
        submission_id=parts[0],
        first_name=first,
        last_name=last,
        date_time=date_time,
        date_time_seconds=date_time_seconds,
        file_name=parts[3]
    )


def get_supported_archive_extensions():
    return [extension for disc in shutil.get_unpack_formats() for extension in disc[1]]


def mkdir(d):
    d.mkdir(parents=True)


def replace_collision_handler(operation, source, destination):
    return destination


def raise_exception_collision_handler(operation, source, destination):
    raise Exception(f'COLISION: cannot {operation} <{source}> because <{destination}> exists.')


def append_number_collision_handler(operation, source, destination):
    return append_number_to_make_unique(destination)


def unpack_archive(s, d, collision_handler=raise_exception_collision_handler):
    if d.exists() and d.is_file():
        d = collision_handler('unpach_archive', s, d)
    shutil.unpack_archive(str(s), str(d))


def copy(s, d, collision_callback=raise_exception_collision_handler):
    if d.exists() and d.is_dir():
        d = d / s.name
    if d.exists() and d.is_file():
        d = collision_callback('copy', s, d)
    shutil.copy2(str(s), str(d))


def append_number_to_make_unique(file):
    i = 1
    if file.exists():
        file = file.with_name(file.stem + f' ({i})' + file.suffix)
        i += 1
    while file.exists():
        k = file.stem.rfind(' ')
        file = file.with_name(file.stem[:k] + f' ({i})' + file.suffix)
        i += 1
    return file
