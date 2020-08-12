import os

from itanalyses.data.parameters.info import Info


class DataIndex:
    def __init__(self, folder=None, index_file=None):
        if index_file:
            self.info = Info(index_file=index_file)
            self.files = self.info.files.copy()
        elif folder:
            self.files = self.file_names(folder)
            self.info = Info(setting_files=self.files)
        else:
            self.files = list()
            self.info = Info()

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

    def add(self, folder=None):
        new_files = list(set(self.file_names(folder)) - set(self.files))
        self.files += new_files
        self.info.load_data(files=new_files)

    def remove(self, files=None):
        pass

    def save(self, index_file='index.idx'):
        self.info.save_data(file_path=index_file)
