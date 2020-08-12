import os

from itanalyses.data.parameters.info import Info


class DataIndex:
    def __init__(self, folder=None, index_file=None):
        if index_file:
            self.folder = os.path.dirname(index_file)
            self.info = Info(index_file=index_file)
            self.files = self.info.files
        else:
            self.folder = folder if folder is not None else '.'
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

    def save(self, index_file='index.idx'):
        self.info.save_data(file_path=index_file)
