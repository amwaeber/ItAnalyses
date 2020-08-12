import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.Qt import Qt

from itanalyses.data.dataindex import DataIndex
from itanalyses.utility.config import paths
from itanalyses.utility.widgets import TreeWidgetItem, ItemSignal


class IndexWidget(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(IndexWidget, self).__init__(parent)

        self.index_path = paths['last_index']
        self.data_index = DataIndex()
        self.selected = list()

        self.setWindowTitle('Experiment Index')

        vbox_total = QtWidgets.QVBoxLayout()

        self.toolbar = QtWidgets.QToolBar("Index")
        create_button = QtWidgets.QAction(QtGui.QIcon(os.path.join(paths['icons'], 'open_index.png')), 'Create Index', self)
        create_button.triggered.connect(self.create_index)
        self.toolbar.addAction(create_button)
        open_button = QtWidgets.QAction(QtGui.QIcon(os.path.join(paths['icons'], 'create_index.png')), 'Open Index', self)
        open_button.triggered.connect(self.open_index)
        self.toolbar.addAction(open_button)
        refresh_button = QtWidgets.QAction(QtGui.QIcon(os.path.join(paths['icons'], 'refresh.png')), 'Refresh', self)
        refresh_button.triggered.connect(self.refresh_index)
        self.toolbar.addAction(refresh_button)
        save_button = QtWidgets.QAction(QtGui.QIcon(os.path.join(paths['icons'], 'save.png')), 'Save Index', self)
        save_button.triggered.connect(self.save_index)
        self.toolbar.addAction(save_button)
        vbox_total.addWidget(self.toolbar)

        self.experiment_tree = QtWidgets.QTreeWidget()
        self.experiment_tree.setRootIsDecorated(False)
        self.experiment_tree.setSortingEnabled(True)
        self.experiment_tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        header_labels = [''] + list(self.data_index.info.info.keys())[1:]
        self.experiment_tree.setHeaderLabels(header_labels)
        self.experiment_tree.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        vbox_total.addWidget(self.experiment_tree)

        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        vbox_total.addWidget(self.buttonBox)

        self.setLayout(vbox_total)
        self.showMaximized()

    def create_index(self):
        path = str(QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Index', self.index_path))
        if path:
            self.index_path = path
            self.data_index = DataIndex(folder=self.index_path)
            self.update_index_tree()

    def open_index(self):  # TODO: Implement loading from saved index
        index = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Select Directory', self.index_path,
                                                          "Index files (*.idx)")[0])
        if index:
            self.index_path = os.path.dirname(index)
            self.data_index = DataIndex(index_file=index)
            self.update_index_tree()

    def refresh_index(self):
        self.data_index = DataIndex(folder=self.data_index.folder)
        self.update_index_tree()

    def save_index(self):
        save_path = str(QtWidgets.QFileDialog.getSaveFileName(self, 'Save as...', self.index_path,
                                                              "Index files (*.idx)")[0])
        self.data_index.save(save_path)

    def update_index_tree(self):
        self.experiment_tree.clear()
        for i, file in enumerate(self.data_index.files):
            tree_item = TreeWidgetItem(ItemSignal(), self.experiment_tree,
                                       [None] + ['%s' % _ for _ in self.data_index.info.info.loc[i].values.tolist()[1:]])
            tree_item.setToolTip(1, os.path.dirname(file))
            tree_item.setCheckState(0, Qt.Unchecked)
            tree_item.signal.itemChecked.connect(self.tree_checkbox_changed)

    @QtCore.pyqtSlot(object, int)
    def tree_checkbox_changed(self, item, column):
        experiment = str(item.toolTip(1))
        if int(item.checkState(column)) == 0:
            self.selected.remove(experiment)
        else:
            self.selected.append(experiment)
