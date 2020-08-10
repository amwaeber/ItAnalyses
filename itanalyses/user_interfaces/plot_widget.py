from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.Qt import Qt


class PlotWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)

        self.plot_group_box = QtWidgets.QGroupBox('Graphs')
        vbox_plot = QtWidgets.QVBoxLayout()
        self.plot_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.plot_canvas.figure.tight_layout(pad=0.3)
        vbox_plot.addWidget(self.plot_canvas)
        self.plot_group_box.setLayout(vbox_plot)
