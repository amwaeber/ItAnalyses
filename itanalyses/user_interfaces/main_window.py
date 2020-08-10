import ctypes
import os
from PyQt5 import QtWidgets, QtGui

from itanalyses.user_interfaces.main_widget import MainWidget
from itanalyses.utility import config
from itanalyses.utility.version import __version__


# noinspection PyAttributeOutsideInit
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # # changing the background color to white
        # self.setStyleSheet("background-color: white;")

        myappid = 'ItAnalyses'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        config.read_config()
        self.init_ui()

    def init_ui(self):
        self.setWindowIcon(QtGui.QIcon(os.path.join(config.paths['icons'], 'analysis.png')))
        self.setWindowTitle("%s %s" % (config.global_confs['progname'], __version__))

        self.main_widget = MainWidget(self)  # create multiple document interface widget
        self.setCentralWidget(self.main_widget)
        self.showMaximized()

    def closeEvent(self, *args, **kwargs):
        super(QtWidgets.QMainWindow, self).closeEvent(*args, **kwargs)

        # Save newly created experiment analyses
        for experiment in self.main_widget.experiment_dict.values():
            experiment.save_pickle()

        # Update config ini with current paths
        config.write_config(plot_path=str(self.main_widget.plot_directory),
                            analysis_path=str(self.main_widget.analysis_directory),
                            export_path=str(self.main_widget.export_directory))
