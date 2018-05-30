import pickle
from kodiak.submission import SubmissionFile
import shutil


class PackCommand:
    def __init__(self, projectDirectory):
        self.projectDirectory = projectDirectory.resolve()
        self.unpackMap = None
        self.definePaths()

    def definePaths(self):
        self.pathTo = {
            'project': self.projectDirectory,
            'internal': self.projectDirectory / '.kodiak',
            'archive': self.projectDirectory / '.kodiak' / 'archive',
            'extracted archive': self.projectDirectory / '.kodiak' / 'archive-extracted',
            'extracted pack': self.projectDirectory / '.kodiak' / 'pack-extracted',
        }

    def pack(self):
        self.loadUnpackMap()
        self.makePackDirectory()
        self.copyOriginalSubmissionsToPackDirectory()
        self.copyUnpackedSubmissionsToPackDirectory()
        self.archivePack()

    def loadUnpackMap(self):
        self.unpackMap = pickle.load((self.pathTo['internal'] / 'unpackMap.dict').open('rb'))

    def makePackDirectory(self):
        self.pathTo['extracted pack'].mkdir()

    def copyOriginalSubmissionsToPackDirectory(self):
        packPath = self.pathTo['extracted pack']
        for f in self.getStudentSubmissionFiles():
            shutil.copy2(str(f.path), str(packPath / f.path.name))

    def copyUnpackedSubmissionsToPackDirectory(self):
        for originalName, unpackedName in self.unpackMap.items():
            print(originalName, '======>', unpackedName)
            pack_path = self.pathTo['extracted pack']
            orig_path = self.pathTo['extracted archive']
            proj_path = self.pathTo['project']
            originalFilePath = orig_path / originalName
            originalSubmission = SubmissionFile(originalFilePath)
            student = originalSubmission.getStudentNameFromSubmissionFile()
            unpacked = proj_path / student / unpackedName
            if unpacked.is_dir():
                target = pack_path / (pack_path/originalName).stem
                shutil.make_archive(target, 'zip', unpacked)
            else:
                target = str(pack_path / originalName)
                shutil.copy2(unpacked, target)

    def getStudentSubmissionFiles(self):
        for f in self.pathTo['extracted archive'].iterdir():
            if f.name not in ['index.html', '.', '..']:
                yield SubmissionFile(f)

    def archivePack(self):
        originalArchive = next(self.pathTo['archive'].iterdir())

        source = self.pathTo['extracted pack']
        target = self.pathTo['project'] / originalArchive.stem

        shutil.make_archive(target, 'zip', source)
