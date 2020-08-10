import os
from PyQt5 import QtWidgets, QtGui

from itanalyses.user_interfaces.table_widget import TableWidget
from itanalyses.utility import config
from itanalyses.utility.version import __version__


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        config.read_config()
        self.init_ui()

    def init_ui(self):
        self.setWindowIcon(QtGui.QIcon(os.path.join(config.paths['icons'], 'coffee.png')))
        self.setWindowTitle("%s %s" % (config.global_confs['progname'], __version__))

        self.table_widget = TableWidget(self)  # create multiple document interface widget
        self.setCentralWidget(self.table_widget)
        self.showMaximized()

    def closeEvent(self, *args, **kwargs):
        super(QtWidgets.QMainWindow, self).closeEvent(*args, **kwargs)

        # Save newly created experiment analyses
        for experiment in self.table_widget.tab_analysis.experiment_dict.values():
            experiment.save_pickle()

        # Update config ini with current paths
        config.write_config(plot_path=str(self.table_widget.tab_analysis.plot_directory),
                            analysis_path=str(self.table_widget.tab_analysis.analysis_directory),
                            export_path=str(self.table_widget.tab_analysis.export_directory))
