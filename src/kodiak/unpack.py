import shutil
import pathlib
from kodiak.submission import SubmissionFile


class UnpackCommand:
    def __init__(self, archiveFile: pathlib.Path, projectDirectory: pathlib.Path, keep_all: bool) -> None:
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
        for submissionFile in self.getStudentSubmissionFiles():
            submissionFile.fixMtime()

    def createStudentDirectories(self):
        for name in self.getStudentNames():
            studentDirectory = self.pathTo['project'] / name
            mkdir(studentDirectory)

    def getStudentNames(self):
        files = self.getStudentSubmissionFiles()
        names = [self.getStudentNameFromSubmissionFile(f) for f in files]
        return set(names)

    def getStudentNameFromSubmissionFile(self, f: SubmissionFile):
        return f'{f.student_last_name}_{f.student_first_name}'

    def getStudentSubmissionFiles(self):
        for f in self.pathTo['extracted archive'].iterdir():
            if f.name not in ['index.html', '.', '..']:
                yield SubmissionFile(f)

    def importStudentSubmissions(self):
        for file in self.getSubmissionsOrderedOldestToYoungest():
            name = self.getStudentNameFromSubmissionFile(file)
            student = self.pathTo['project'] / name
            unpackedFile = student / file.submitted_filename
            if self.isArchive(file):
                target = unpackedFile.with_name(unpackedFile.stem)
                unpack_archive(file.path, target, self.collisionHandler)
            else:
                copy(file.path, unpackedFile, self.collisionHandler)

    def getSubmissionsOrderedOldestToYoungest(self):
        submissions = list(self.getStudentSubmissionFiles())
        return sorted(submissions, key=lambda s: s.datetime)

    def isArchive(self, file):
        return file.suffix in get_supported_archive_extensions()


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
