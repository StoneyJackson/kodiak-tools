import datetime
import os
import pathlib
import pickle
import shutil
import time
import typing


class Project:
    def __init__(self: 'Project', root: pathlib.Path) -> None:
        self.root = root


    def runInitCommand(
        self: 'Project', archive: pathlib.Path, importer: 'SubmissionImporter'
    ) -> None:
        self.definePaths()
        self.initializeProjectDirectory()
        self.setOriginalArchiveFile(archive)
        self.copyArchiveIn(archive)
        self.extractArchive()
        self.loadSubmissionFiles()
        self.adjustTimeStampsOnSubmissionFilesToMatchNames()
        self.makeStudentDirectories()
        importer.importIntoProject(self)
        self.writeSourceTargetMapping()


    def definePaths(self: 'Project') -> None:
        self.kodiakDir =                self.root / '.kodiak'
        self.sourceTargetMappingFile =  self.root / '.kodiak' / 'sourceTargetMapping'
        self.originalArchiveDir =       self.root / 'originalArchive'
        self.originalSubmissionsDir =   self.root / 'originalSubmissions'
        self.submissionsDir =           self.root / 'submissions'
        self.gradedSubmissionsDir =     self.root / 'gradedSubmissions'
        self.gradedArchiveDir =         self.root / 'gradedArchive'

        self.originalArchiveFile: typing.Union[pathlib.Path, None] =  None
        self.originalSubmissionFiles: typing.List['SubmissionFile'] = []
        self.gradedSubmissionFiles: typing.List['SubmissionFile'] = []
        self.studentDirs: typing.List[pathlib.Path] = []
        self.sourceTargetMapping: typing.List[typing.Tuple[pathlib.Path, pathlib.Path]] = []


    def initializeProjectDirectory(self: 'Project') -> None:
        pathsToCreate = [
            self.kodiakDir,
            self.originalArchiveDir,
            self.originalSubmissionsDir,
            self.submissionsDir,
            self.gradedSubmissionsDir,
            self.gradedArchiveDir,
        ]
        for path in pathsToCreate:
            path.mkdir(parents=True, exist_ok=True)


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
            path = self.submissionsDir / f.getStudentDirectoryName()
            path.mkdir(parents=True, exist_ok=True)
            self.studentDirs.append(path)


    def writeSourceTargetMapping(self: 'Project') -> None:
        pickle.dump(self.sourceTargetMapping, self.sourceTargetMappingFile.open('wb'))


    def getSubmissionFilesOldestToNewest(self: 'Project') -> typing.List['SubmissionFile']:
        return sorted(self.originalSubmissionFiles, key=getDatetimeFromSubmissionFile)


    def getSubmissionFilesNewestToOldest(self: 'Project') -> typing.Iterator['SubmissionFile']:
        return reversed(self.getSubmissionFilesOldestToNewest())


    def runArchiveCommand(self: 'Project') -> None:
        self.resolveRoot()
        self.definePaths()
        self.loadState()
        self.copyOriginalSubmissionsToGradedSubmissions()
        self.copySubmissionsToGradedSubmissions()
        self.archiveGradedSubmissions()


    def resolveRoot(self: 'Project') -> None:
        d = self.root
        d = d.resolve()
        while '.kodiak' not in [f.name for f in d.iterdir()] and d != d.parent:
            d = d.parent
        if '.kodiak' not in [f.name for f in d.iterdir()]:
            raise Exception(f'"{d}" is not a Kodiak project.')
        self.root = d


    def loadState(self: 'Project') -> None:
        self.originalArchiveFile = next(self.originalArchiveDir.iterdir())
        self.originalSubmissionFiles.extend(
            SubmissionFile(self, f)
            for f in self.originalSubmissionsDir.iterdir() if f.name != 'index.html'
        )
        self.studentDirs.extend(self.submissionsDir.iterdir())
        self.sourceTargetMapping = pickle.load(self.sourceTargetMappingFile.open('rb'))


    def copyOriginalSubmissionsToGradedSubmissions(self: 'Project') -> None:
        for f in self.originalSubmissionsDir.iterdir():
            shutil.copy2(f, self.gradedSubmissionsDir)


    def copySubmissionsToGradedSubmissions(self: 'Project') -> None:
        sources = {}
        for source, target in self.sourceTargetMapping:
            sources[target] = source

        for studentDir in self.submissionsDir.iterdir():
            for file in studentDir.iterdir():
                original = sources[file]
                if SubmissionFile(self, original).isArchive():
                    shutil.make_archive(
                        base_name=str(self.gradedSubmissionsDir / original.stem),
                        format=original.suffix[1:],
                        root_dir=str(file),
                    )
                else:
                    shutil.copy2(
                        str(file),
                        str(self.gradedSubmissionsDir / original.name)
                    )


    def archiveGradedSubmissions(self: 'Project') -> None:
        oaf = typing.cast(pathlib.Path, self.originalArchiveFile)
        shutil.make_archive(
            base_name=str(self.gradedArchiveDir/oaf.stem),
            format='zip',
            root_dir=str(self.gradedSubmissionsDir)
        )


class SubmissionImporter:
    def __init__(
        self: 'SubmissionImporter',
        getSubmissionFiles: typing.Callable[[Project], typing.Iterable['SubmissionFile']],
        shouldImport: typing.Callable[['SubmissionFile'], bool]
    ) -> None:
        self.getSubmissionFiles = getSubmissionFiles
        self.shouldImport = shouldImport

    def importIntoProject(self: 'SubmissionImporter', project: Project) -> None:
        for file in self.getSubmissionFiles(project):
            if self.shouldImport(file):
                source, target = file.importIntoProject()
                project.sourceTargetMapping.append( (source, target) )


def getSubmissionFilesOldestToNewest(project: Project) -> typing.Iterable['SubmissionFile']:
    return project.getSubmissionFilesOldestToNewest()


def getSubmissionFilesNewestToOldest(project: Project) -> typing.Iterable['SubmissionFile']:
    return project.getSubmissionFilesNewestToOldest()


def processIfDoesNotExist(file: 'SubmissionFile') -> bool:
    return not file.getPathUnderSubmissionsDir().exists()


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
        self.parse(path.name)
        self.datetime = makeDatetime(self.datetime_str)
        self.datetime_total_seconds = calculateTotalSeconds(self.datetime)

    def parse(self: 'SubmissionFile', name: str) -> None:
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

    def getPathUnderSubmissionsDir(self: 'SubmissionFile') -> pathlib.Path:
        target_parent_path = self.project.submissionsDir
        name = self.getStudentDirectoryName()
        path = target_parent_path / name / self.submitted_filename
        if self.isArchive():
            path = path.with_name(path.stem)
        return path

    def getStudentDirectoryName(self: 'SubmissionFile') -> str:
        return f'{self.student_last_name}_{self.student_first_name}'

    def isArchive(self: 'SubmissionFile') -> bool:
        return self.path.suffix in get_supported_archive_extensions()

    def unpackTo(self: 'SubmissionFile', target: pathlib.Path) -> None:
        if self.isArchive():
            self.unpackArchiveTo(target)
        else:
            self.unpackFileTo(target)

    def unpackArchiveTo(self: 'SubmissionFile', target: pathlib.Path) -> None:
        shutil.unpack_archive(str(self.path), str(target))

    def unpackFileTo(self: 'SubmissionFile', target: pathlib.Path) -> None:
        shutil.copy2(str(self.path), str(target))

    def importIntoProject(self: 'SubmissionFile') -> typing.Tuple[pathlib.Path, pathlib.Path]:
        target = append_number_to_make_unique(self.getPathUnderSubmissionsDir())
        self.unpackTo(target)
        return (self.path, target)


def getDatetimeFromSubmissionFile(file: SubmissionFile) -> datetime.datetime:
    return file.datetime


def makeDatetime(s: str) -> datetime.datetime:
    # Kodiak runs together hours and minutes. Split them up so that
    # we can use strptime to parse and create a datetime.datetime object.
    minutes = s[-5:-3]
    hours = s[-7:-5]
    s = s[:-7] + hours + ' ' + minutes + s[-3:]
    return datetime.datetime.strptime(s, '%b %d, %Y %I %M %p')


def calculateTotalSeconds(dt: datetime.datetime) -> float:
    return (dt - datetime.datetime(1970, 1, 1)).total_seconds() + time.timezone


def get_supported_archive_extensions() -> typing.List[str]:
    return [extension for disc in shutil.get_unpack_formats() for extension in disc[1]]


def append_number_to_make_unique(file: pathlib.Path) -> pathlib.Path:
    i = 1
    if file.exists():
        file = file.with_name(file.stem + f' ({i})' + file.suffix)
        i += 1
    while file.exists():
        k = file.stem.rfind(' ')
        file = file.with_name(file.stem[:k] + f' ({i})' + file.suffix)
        i += 1
    return file
