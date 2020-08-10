import os

from itanalyses.data.parameters.info import Info


class DataIndex:
    def __init__(self, folder=None):
        self.folder = folder
        self.files = self.file_names(self.folder)
        self.info = Info(setting_files=self.files)

    def file_names(self, path):
        files = list()
        if os.path.isfile(path):
            return []
        # add dir to pathlist if it contains info files
        if len([f for f in os.listdir(path) if os.path.basename(f) == 'IV_Curve_0.dat']) > 0:
            files.append(os.path.normpath(os.path.join(path, 'IV_Curve_0.dat')))
        for d in os.listdir(path):
            new_path = os.path.join(path, d)
            if os.path.isdir(new_path):
                files += self.file_names(new_path)
        return files
