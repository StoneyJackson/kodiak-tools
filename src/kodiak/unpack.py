import shutil
import pathlib
from kodiak.submission import SubmissionFile


class UnpackCommand:
    def __init__(self, archiveFile: pathlib.Path, projectDirectory: pathlib.Path, duplicates: str) -> None:
        self.archiveFile = archiveFile.resolve()
        self.projectDirectory = projectDirectory.resolve()
        self.duplicates_option = duplicates
        self.definePaths()

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
        shutil.unpack_archive(str(archive), str(target))

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
        project_path = self.pathTo['project']
        if self.duplicates_option == 'newest-only':
            self.importNewestStudentSubmissions(project_path)
        elif self.duplicates_option == 'oldest-only':
            self.importOldestStudentSubmissions(project_path)
        elif self.duplicates_option == 'number-older':
            self.importStudentSubmissionsNumberingOlder(project_path)
        elif self.duplicates_option == 'number-newer':
            self.importStudentSubmissionsNumberingNewer(project_path)

    def importOldestStudentSubmissions(self, target_path):
        self.importSubmissionsSkippingDuplicates(self.getSubmissionsOldestToYoungest(), target_path)

    def importNewestStudentSubmissions(self, target_path):
        self.importSubmissionsSkippingDuplicates(self.getSubmissionsYoungestToOldest(), target_path)

    def importSubmissionsSkippingDuplicates(self, submissions, target_path):
        for file in submissions:
            p = file.getUnpackedFilePath(target_path)
            if p.exists():
                continue
            else:
                file.unpackTo(p)

    def importStudentSubmissionsNumberingNewer(self, target_path):
        self.importSubmissionsNumberingDuplicates(self.getSubmissionsOldestToYoungest(), target_path)

    def importStudentSubmissionsNumberingOlder(self, target_path):
        self.importSubmissionsNumberingDuplicates(self.getSubmissionsYoungestToOldest(), target_path)

    def importSubmissionsNumberingDuplicates(self, submissions, target_path):
        for file in submissions:
            p = file.getUnpackedFilePath(target_path)
            p = append_number_to_make_unique(p)
            file.unpackTo(p)

    def getSubmissionsOldestToYoungest(self):
        submissions = list(self.getStudentSubmissionFiles())
        submissions = sorted(submissions, key=lambda s: s.datetime)
        return submissions

    def getSubmissionsYoungestToOldest(self):
        return reversed(self.getSubmissionsOldestToYoungest())


def mkdir(d):
    d.mkdir(parents=True)


def copy(s, d):
    if d.exists() and d.is_dir():
        d = d / s.name
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
