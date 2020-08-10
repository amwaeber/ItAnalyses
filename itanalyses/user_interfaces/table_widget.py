from PyQt5 import QtWidgets

from itanalyses.user_interfaces.main_widget import MainWidget


class TableWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(TableWidget, self).__init__(parent)

        self.layout = QtWidgets.QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QtWidgets.QTabWidget()

        self.tab_analysis = MainWidget(self)
        self.tabs.addTab(self.tab_analysis, "Analysis")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
