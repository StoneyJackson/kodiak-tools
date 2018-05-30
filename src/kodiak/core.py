import pathlib
import shutil
from typing import Dict, Callable, List, Iterable, Union, Tuple
from abc import ABC, abstractmethod
from datetime import datetime
import pickle
import os
import time


class Project:
    def __init__(self: 'Project', root: pathlib.Path) -> None:
        self.root =                     root
        self.private =                  root / '.kodiak'
        self.sourceTargetMappingFile =  root / '.kodiak' / 'sourceTargetMapping'
        self.temp =                     root / '.kodiak' / 'temp'
        self.originalArchiveDir =       root / 'originalArchive'
        self.originalSubmissionsDir =   root / 'originalSubmissions'
        self.submissions =              root / 'submissions'
        self.gradedSubmissions =        root / 'gradedSubmissions'
        self.gradedArchive =            root / 'gradedArchive'

        self.originalArchiveFile: Union[pathlib.Path, None] =  None
        self.originalSubmissionFiles: List['SubmissionFile'] = []
        self.gradedSubmissionFiles: List['SubmissionFile'] = []
        self.studentDirectories: List[pathlib.Path] = []
        self.sourceTargetMapping: List[Tuple[pathlib.Path, pathlib.Path]] = []


    def importArchive(
        self: 'Project', archive: pathlib.Path, importer: 'SubmissionImporter'
    ) -> None:
        self.initializeProjectDirectory()
        self.setOriginalArchiveFile(archive)
        self.copyArchiveIn(archive)
        self.extractArchive()
        self.loadSubmissionFiles()
        self.adjustTimeStampsOnSubmissionFilesToMatchNames()
        self.makeStudentDirectories()
        importer.importIntoProject(self)
        self.writeSourceTargetMapping()

    def initializeProjectDirectory(self: 'Project') -> None:
        pathsToCreate = [
            self.root,
            self.private,
            self.temp,
            self.originalArchiveDir,
            self.originalSubmissionsDir,
            self.submissions,
            self.gradedSubmissions,
            self.gradedArchive,
        ]
        for path in pathsToCreate:
            path.mkdir(parents=True)


    def setOriginalArchiveFile(self: 'Project', external_archive: pathlib.Path) -> None:
        self.originalArchiveFile = self.originalArchiveDir / external_archive.name


    def copyArchiveIn(self: 'Project', archive: pathlib.Path) -> None:
        shutil.copy2(archive, self.originalArchiveDir)


    def extractArchive(self: 'Project') -> None:
        shutil.unpack_archive(
            filename=str(self.originalArchiveFile),
            extract_dir=self.originalSubmissionsDir,
            format='zip'
        )


    def loadSubmissionFiles(self: 'Project') -> None:
        for f in self.originalSubmissionsDir.iterdir():
            if f.name != 'index.html':
                self.originalSubmissionFiles.append(SubmissionFile(self, f))


    def adjustTimeStampsOnSubmissionFilesToMatchNames(self: 'Project') -> None:
        for f in self.originalSubmissionFiles:
            f.adjustTimeStampsToMatchName()

    def makeStudentDirectories(self: 'Project') -> None:
        for f in self.originalSubmissionFiles:
            path = self.submissions / f.getStudentNameFromSubmissionFile()
            path.mkdir(parents=True, exist_ok=True)
            self.studentDirectories.append(path)


    def writeSourceTargetMapping(self: 'Project') -> None:
        pickle.dump(self.sourceTargetMapping, self.sourceTargetMappingFile.open('wb'))


    def getSubmissionFilesOldestToNewest(self: 'Project'):
        return sorted(self.originalSubmissionFiles, key=lambda s: s.datetime)


    def getSubmissionFilesNewestToOldest(self: 'Project'):
        return reversed(self.getSubmissionFilesOldestToNewest())


class SubmissionImporter:
    def __init__(
        self: 'SubmissionImporter',
        getSubmissionFiles: Callable[[Project], Iterable['SubmissionFile']],
        shouldImport: Callable[['SubmissionFile'], bool]
    ) -> None:
        self.getSubmissionFiles = getSubmissionFiles
        self.shouldImport = shouldImport

    def importIntoProject(self: 'SubmissionImporter', project: Project) -> None:
        for file in self.getSubmissionFiles(project):
            if self.shouldImport(file):
                source, target = file.importIntoProject()
                project.sourceTargetMapping.append( (source, target) )


def getSubmissionFilesOldestToNewest(project: Project) -> Iterable['SubmissionFile']:
    return project.getSubmissionFilesOldestToNewest()


def getSubmissionFilesNewestToOldest(project: Project) -> Iterable['SubmissionFile']:
    return project.getSubmissionFilesNewestToOldest()


def processIfDoesNotExist(file: 'SubmissionFile') -> bool:
    return not file.getUnpackedFilePath().exists()


def processUnconditionally(file: 'SubmissionFile') -> bool:
    return True


IMPORT_NEWEST_ONLY = SubmissionImporter(
    getSubmissionFilesNewestToOldest, processIfDoesNotExist
)
IMPORT_OLDEST_ONLY = SubmissionImporter(
    getSubmissionFilesOldestToNewest, processIfDoesNotExist
)
IMPORT_NUMBERING_NEWER = SubmissionImporter(
    getSubmissionFilesOldestToNewest, processUnconditionally
)
IMPORT_NUMBERING_OLDER = SubmissionImporter(
    getSubmissionFilesNewestToOldest, processUnconditionally
)


class SubmissionFile:
    def __init__(self: 'SubmissionFile', project: Project, path: pathlib.Path) -> None:
        self.project = project
        self.path = path
        self.suffix = path.suffix
        self.parseIntoAttributes(path.name)
        self.datetime = makeDatetime(self.datetime_str)
        self.datetime_total_seconds = calculateTotalSeconds(self.datetime)

    def parseIntoAttributes(self: 'SubmissionFile', name: str) -> None:
        parts = name.split(' - ', maxsplit=3)
        first, last = parts[1].split(' ')
        self.student_submission_id = parts[0]
        self.student_first_name = first
        self.student_last_name = last
        self.datetime_str = parts[2]
        self.submitted_filename = parts[3]

    def adjustTimeStampsToMatchName(self: 'SubmissionFile') -> None:
        s = self.datetime_total_seconds
        os.utime(str(self.path), (s, s))

    def getUnpackedFilePath(self: 'SubmissionFile'):
        target_parent_path = self.project.submissions
        name = self.getStudentNameFromSubmissionFile()
        path = target_parent_path / name / self.submitted_filename
        if self.isArchive():
            path = path.with_name(path.stem)
        return path

    def getStudentNameFromSubmissionFile(self: 'SubmissionFile'):
        return f'{self.student_last_name}_{self.student_first_name}'

    def isArchive(self: 'SubmissionFile'):
        return self.path.suffix in get_supported_archive_extensions()

    def unpackTo(self: 'SubmissionFile', target):
        if self.isArchive():
            self.unpackArchiveTo(target)
        else:
            self.unpackFileTo(target)

    def unpackArchiveTo(self: 'SubmissionFile', target):
        shutil.unpack_archive(str(self.path), str(target))

    def unpackFileTo(self: 'SubmissionFile', target):
        shutil.copy2(str(self.path), str(target))

    def importIntoProject(self: 'SubmissionFile'):
        target = append_number_to_make_unique(self.getUnpackedFilePath())
        self.unpackTo(target)
        return (self.path, target)


def makeDatetime(s: str) -> datetime:
    # Kodiak runs together hours and minutes. Split them up so that
    # we can use strptime to parse and create a datetime object.
    minutes = s[-5:-3]
    hours = s[-7:-5]
    s = s[:-7] + hours + ' ' + minutes + s[-3:]
    return datetime.strptime(s, '%b %d, %Y %I %M %p')


def calculateTotalSeconds(dt: datetime) -> float:
    return (dt - datetime(1970, 1, 1)).total_seconds() + time.timezone


def get_supported_archive_extensions():
    return [extension for disc in shutil.get_unpack_formats() for extension in disc[1]]


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
