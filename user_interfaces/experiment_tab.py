import numpy as np
import os
from PyQt5 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg

import hardware.keithley as keithley
import hardware.sensor as sensor
from utility import ports
from utility.config import paths


pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class Experiment(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(Experiment, self).__init__(parent)

        self.directory = paths['last_save']
        self.data_iv = np.zeros((5, 1))
        self.block_sensor = False
        self.red_pen = pg.mkPen(color=(255, 0, 0), width=2)
        self.orange_pen = pg.mkPen(color=(255, 140, 0), width=2)
        self.green_pen = pg.mkPen(color=(50, 205, 50), width=2)
        self.blue_pen = pg.mkPen(color=(30, 144, 255), width=2)
        self.black_pen = pg.mkPen(color=(0, 0, 0), width=2)

        vbox_total = QtWidgets.QVBoxLayout()
        hbox_top = QtWidgets.QHBoxLayout()
        self.iv_group_box = QtWidgets.QGroupBox('I-V Curve')
        vbox_iv = QtWidgets.QVBoxLayout()
        self.iv_graph = pg.PlotWidget()
        self.iv_graph.plotItem.getAxis('left').setPen(self.black_pen)
        self.iv_graph.plotItem.getAxis('bottom').setPen(self.black_pen)
        self.iv_graph.setTitle('I-V Curve')
        self.iv_graph.setLabel('left', 'Current (A)')
        self.iv_graph.setLabel('bottom', 'Voltage (V)')
        self.iv_data_line = self.iv_graph.plot(pen=self.blue_pen)
        vbox_iv.addWidget(self.iv_graph)
        self.iv_group_box.setLayout(vbox_iv)
        hbox_top.addWidget(self.iv_group_box, 5)

        vbox_sensor_col = QtWidgets.QVBoxLayout()
        self.sensors_group_box = QtWidgets.QGroupBox('Sensor Readout')
        vbox_sensors = QtWidgets.QVBoxLayout()
        grid_sensors = QtWidgets.QGridLayout()
        self.temperature_label = QtWidgets.QLabel("Temperature (C)", self)
        grid_sensors.addWidget(self.temperature_label, 0, 0)
        self.temperature_edit = QtWidgets.QLineEdit('25', self)
        self.temperature_edit.setFixedWidth(60)
        self.temperature_edit.setDisabled(True)
        grid_sensors.addWidget(self.temperature_edit, 0, 1)
        self.diode1_label = QtWidgets.QLabel("Diode 1 (W/m2)", self)
        grid_sensors.addWidget(self.diode1_label, 1, 0)
        self.diode1_edit = QtWidgets.QLineEdit('0', self)
        self.diode1_edit.setFixedWidth(60)
        self.diode1_edit.setDisabled(True)
        grid_sensors.addWidget(self.diode1_edit, 1, 1)
        self.diode2_label = QtWidgets.QLabel("Diode 2 (W/m2)", self)
        grid_sensors.addWidget(self.diode2_label, 1, 2)
        self.diode2_edit = QtWidgets.QLineEdit('0', self)
        self.diode2_edit.setFixedWidth(60)
        self.diode2_edit.setDisabled(True)
        grid_sensors.addWidget(self.diode2_edit, 1, 3)
        self.diode3_label = QtWidgets.QLabel("Diode 3 (W/m2)", self)
        grid_sensors.addWidget(self.diode3_label, 2, 0)
        self.diode3_edit = QtWidgets.QLineEdit('0', self)
        self.diode3_edit.setFixedWidth(60)
        self.diode3_edit.setDisabled(True)
        grid_sensors.addWidget(self.diode3_edit, 2, 1)
        self.diode4_label = QtWidgets.QLabel("Diode 4 (W/m2)", self)
        grid_sensors.addWidget(self.diode4_label, 2, 2)
        self.diode4_edit = QtWidgets.QLineEdit('0', self)
        self.diode4_edit.setFixedWidth(60)
        self.diode4_edit.setDisabled(True)
        grid_sensors.addWidget(self.diode4_edit, 2, 3)
        vbox_sensors.addLayout(grid_sensors)
        self.sensors_group_box.setLayout(vbox_sensors)
        vbox_sensor_col.addWidget(self.sensors_group_box)

        hbox_sens_plot_setup = QtWidgets.QHBoxLayout()
        self.sens_plot_group_box = QtWidgets.QGroupBox('Sensor Plots')
        hbox_sens_plot = QtWidgets.QHBoxLayout()
        self.sensor_graph = pg.PlotWidget()
        self.sensor_graph.plotItem.getAxis('left').setPen(self.black_pen)
        self.sensor_graph.plotItem.getAxis('bottom').setPen(self.black_pen)
        self.sensor_graph.setTitle('Sensor Readout')
        self.sensor_graph.setLabel('left', '')
        self.sensor_graph.setLabel('bottom', 'Time (s)')
        self.temp_data_line = self.sensor_graph.plot(pen=self.blue_pen)
        self.power_data_line1 = self.sensor_graph.plot(pen=self.blue_pen)
        self.power_data_line2 = self.sensor_graph.plot(pen=self.red_pen)
        self.power_data_line3 = self.sensor_graph.plot(pen=self.green_pen)
        self.power_data_line4 = self.sensor_graph.plot(pen=self.orange_pen)
        hbox_sens_plot.addWidget(self.sensor_graph)
        self.sens_plot_group_box.setLayout(hbox_sens_plot)
        hbox_sens_plot_setup.addWidget(self.sens_plot_group_box)

        vbox_sensor_meas = QtWidgets.QVBoxLayout()
        self.sensor_meas_group_box = QtWidgets.QGroupBox('Sensor Measure')
        grid_sensor_meas = QtWidgets.QGridLayout()
        self.sensor_plot_label = QtWidgets.QLabel("Plot", self)
        grid_sensor_meas.addWidget(self.sensor_plot_label, 0, 0)
        self.sensor_plot_cb = QtWidgets.QComboBox()
        self.sensor_plot_cb.setFixedWidth(120)
        self.sensor_plot_cb.addItem('Continuous')
        self.sensor_plot_cb.addItem('Fixed')
        grid_sensor_meas.addWidget(self.sensor_plot_cb, 0, 1)
        self.sensor_time_label = QtWidgets.QLabel("Time (s)", self)
        grid_sensor_meas.addWidget(self.sensor_time_label, 1, 0)
        self.sensor_time_edit = QtWidgets.QLineEdit('60', self)
        self.sensor_time_edit.setFixedWidth(80)
        grid_sensor_meas.addWidget(self.sensor_time_edit, 1, 1)
        self.sensor_avg_label = QtWidgets.QLabel("# Averages", self)
        grid_sensor_meas.addWidget(self.sensor_avg_label, 2, 0)
        self.sensor_avg_edit = QtWidgets.QLineEdit('1', self)
        self.sensor_avg_edit.setFixedWidth(80)
        grid_sensor_meas.addWidget(self.sensor_avg_edit, 2, 1)
        vbox_sensor_meas.addLayout(grid_sensor_meas)
        vbox_sensor_meas.addStretch(-1)

        hbox_sens_ctrl = QtWidgets.QHBoxLayout()
        temp_icon = QtGui.QIcon()
        temp_icon.addPixmap(QtGui.QPixmap(os.path.join(paths['icons'], 'temp_off.png')),
                            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        temp_icon.addPixmap(QtGui.QPixmap(os.path.join(paths['icons'], 'temp_on.png')),
                            QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.temp_button = QtWidgets.QPushButton(QtGui.QIcon(temp_icon), '')
        self.temp_button.setIconSize(QtCore.QSize(40, 40))
        self.temp_button.setCheckable(True)
        self.temp_button.clicked.connect(self.plot_temp)
        self.temp_button.setToolTip('Plot temperature')
        hbox_sens_ctrl.addWidget(self.temp_button)
        power_icon = QtGui.QIcon()
        power_icon.addPixmap(QtGui.QPixmap(os.path.join(paths['icons'], 'power_off.png')),
                             QtGui.QIcon.Normal, QtGui.QIcon.Off)
        power_icon.addPixmap(QtGui.QPixmap(os.path.join(paths['icons'], 'power_on.png')),
                             QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.power_button = QtWidgets.QPushButton(QtGui.QIcon(power_icon), '')
        self.power_button.setIconSize(QtCore.QSize(40, 40))
        self.power_button.setCheckable(True)
        self.power_button.clicked.connect(self.plot_pow)
        self.power_button.setToolTip('Plot power')
        hbox_sens_ctrl.addWidget(self.power_button)
        hbox_sens_ctrl.addStretch(-1)
        self.sensor_clipboard_button = QtWidgets.QPushButton(
            QtGui.QIcon(os.path.join(paths['icons'], 'clipboard.png')), '')
        # self.sensor_clipboard_button.setIconSize(QtCore.QSize(40, 40))
        self.sensor_clipboard_button.clicked.connect(lambda: self.clipboard('sensor'))
        self.sensor_clipboard_button.setToolTip('Save plot to clipboard')
        hbox_sens_ctrl.addWidget(self.sensor_clipboard_button)
        vbox_sensor_meas.addLayout(hbox_sens_ctrl)
        self.sensor_meas_group_box.setLayout(vbox_sensor_meas)
        hbox_sens_plot_setup.addWidget(self.sensor_meas_group_box)
        vbox_sensor_col.addLayout(hbox_sens_plot_setup)

        self.arduino_group_box = QtWidgets.QGroupBox('Sensor Parameters')
        grid_arduino = QtWidgets.QGridLayout()
        self.baud_label = QtWidgets.QLabel("Baud rate", self)
        grid_arduino.addWidget(self.baud_label, 0, 0)
        self.baud_edit = QtWidgets.QLineEdit('38400', self)
        self.baud_edit.setFixedWidth(60)
        self.baud_edit.setDisabled(True)
        grid_arduino.addWidget(self.baud_edit, 0, 1)
        self.datapoints_label = QtWidgets.QLabel("# Data points", self)
        grid_arduino.addWidget(self.datapoints_label, 0, 2)
        self.datapoints_edit = QtWidgets.QLineEdit('100', self)
        self.datapoints_edit.setFixedWidth(60)
        self.datapoints_edit.setDisabled(True)
        grid_arduino.addWidget(self.datapoints_edit, 0, 3)
        self.databytes_label = QtWidgets.QLabel("Data bytes", self)
        grid_arduino.addWidget(self.databytes_label, 1, 0)
        self.databytes_edit = QtWidgets.QLineEdit('2', self)
        self.databytes_edit.setFixedWidth(60)
        self.databytes_edit.setDisabled(True)
        grid_arduino.addWidget(self.databytes_edit, 1, 1)
        self.timeout_label = QtWidgets.QLabel("Timeout (s)", self)
        grid_arduino.addWidget(self.timeout_label, 1, 2)
        self.timeout_edit = QtWidgets.QLineEdit('30', self)
        self.timeout_edit.setFixedWidth(60)
        self.timeout_edit.setDisabled(True)
        grid_arduino.addWidget(self.timeout_edit, 1, 3)
        self.ais_label = QtWidgets.QLabel("Analogue inputs", self)
        grid_arduino.addWidget(self.ais_label, 2, 0)
        self.ais_edit = QtWidgets.QLineEdit('5', self)
        self.ais_edit.setFixedWidth(60)
        self.ais_edit.setDisabled(True)
        grid_arduino.addWidget(self.ais_edit, 2, 1)
        self.query_label = QtWidgets.QLabel("Query period (s)", self)
        grid_arduino.addWidget(self.query_label, 2, 2)
        self.query_edit = QtWidgets.QLineEdit('0.25', self)
        self.query_edit.setFixedWidth(60)
        self.query_edit.setDisabled(True)
        grid_arduino.addWidget(self.query_edit, 2, 3)
        self.arduino_group_box.setLayout(grid_arduino)
        vbox_sensor_col.addWidget(self.arduino_group_box)
        vbox_sensor_col.addStretch(-1)
        hbox_top.addLayout(vbox_sensor_col, 3)
        vbox_total.addLayout(hbox_top, 4)

        hbox_bottom = QtWidgets.QHBoxLayout()
        vbox_bottom_left = QtWidgets.QVBoxLayout()
        self.source_group_box = QtWidgets.QGroupBox('I-V Measure')
        hbox_source = QtWidgets.QHBoxLayout()

        grid_source = QtWidgets.QGridLayout()
        self.start_label = QtWidgets.QLabel("Start (V)", self)
        grid_source.addWidget(self.start_label, 0, 0)
        self.start_edit = QtWidgets.QLineEdit('-0.01', self)
        self.start_edit.setFixedWidth(80)
        self.start_edit.textChanged.connect(self.update_steps)
        grid_source.addWidget(self.start_edit, 0, 1)
        self.end_label = QtWidgets.QLabel("End (V)", self)
        grid_source.addWidget(self.end_label, 0, 2)
        self.end_edit = QtWidgets.QLineEdit('0.7', self)
        self.end_edit.setFixedWidth(80)
        self.end_edit.textChanged.connect(self.update_steps)
        grid_source.addWidget(self.end_edit, 0, 3)
        self.step_label = QtWidgets.QLabel("Step (V)", self)
        grid_source.addWidget(self.step_label, 0, 4)
        self.step_edit = QtWidgets.QLineEdit('0.005', self)
        self.step_edit.setFixedWidth(80)
        self.step_edit.setDisabled(True)
        grid_source.addWidget(self.step_edit, 0, 5)
        self.nstep_label = QtWidgets.QLabel("# Steps", self)
        grid_source.addWidget(self.nstep_label, 0, 6)
        self.nstep_edit = QtWidgets.QLineEdit('142', self)
        self.nstep_edit.setFixedWidth(80)
        self.nstep_edit.textChanged.connect(self.update_steps)
        grid_source.addWidget(self.nstep_edit, 0, 7)

        self.ilimit_label = QtWidgets.QLabel("I Limit (A)", self)
        grid_source.addWidget(self.ilimit_label, 1, 0)
        self.ilimit_edit = QtWidgets.QLineEdit('0.5', self)
        self.ilimit_edit.setFixedWidth(80)
        grid_source.addWidget(self.ilimit_edit, 1, 1)
        self.delay_label = QtWidgets.QLabel("Delay (s)", self)
        grid_source.addWidget(self.delay_label, 1, 2)
        self.delay_edit = QtWidgets.QLineEdit('0.025', self)
        self.delay_edit.setFixedWidth(80)
        grid_source.addWidget(self.delay_edit, 1, 3)
        self.reps_label = QtWidgets.QLabel("Repetitions", self)
        grid_source.addWidget(self.reps_label, 1, 4)
        self.reps_edit = QtWidgets.QLineEdit('5', self)
        self.reps_edit.setFixedWidth(80)
        grid_source.addWidget(self.reps_edit, 1, 5)
        self.rep_delay_label = QtWidgets.QLabel("Rep. Delay (s)", self)
        grid_source.addWidget(self.rep_delay_label, 1, 6)
        self.rep_delay_edit = QtWidgets.QLineEdit('2.0', self)
        self.rep_delay_edit.setFixedWidth(80)
        grid_source.addWidget(self.rep_delay_edit, 1, 7)
        self.naverage_label = QtWidgets.QLabel("# Averages", self)
        grid_source.addWidget(self.naverage_label, 1, 8)
        self.naverage_edit = QtWidgets.QLineEdit('5', self)  # adjust to update with NSteps
        self.naverage_edit.setFixedWidth(80)
        grid_source.addWidget(self.naverage_edit, 1, 9)
        hbox_source.addLayout(grid_source)
        hbox_source.addStretch(-1)

        vbox_source_ctrl = QtWidgets.QVBoxLayout()
        vbox_source_ctrl.addStretch(-1)
        start_icon = QtGui.QIcon()
        start_icon.addPixmap(QtGui.QPixmap(os.path.join(paths['icons'], 'iv_off.png')),
                             QtGui.QIcon.Normal, QtGui.QIcon.Off)
        start_icon.addPixmap(QtGui.QPixmap(os.path.join(paths['icons'], 'iv_on.png')),
                             QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.start_button = QtWidgets.QPushButton(QtGui.QIcon(start_icon), '')
        self.start_button.setIconSize(QtCore.QSize(48, 48))
        self.start_button.setCheckable(True)
        self.start_button.clicked.connect(self.start)
        self.start_button.setToolTip('Start Measurement')
        vbox_source_ctrl.addWidget(self.start_button)
        vbox_source_ctrl.addStretch(-1)
        hbox_source.addLayout(vbox_source_ctrl)
        self.source_group_box.setLayout(hbox_source)
        vbox_bottom_left.addWidget(self.source_group_box)

        hbox_port_meas_folder = QtWidgets.QHBoxLayout()
        vbox_port_meas_folder = QtWidgets.QVBoxLayout()
        hbox_port_meas = QtWidgets.QHBoxLayout()
        self.ports_group_box = QtWidgets.QGroupBox('Ports')
        hbox_ports = QtWidgets.QHBoxLayout()
        self.sensor_label = QtWidgets.QLabel("Arduino", self)
        hbox_ports.addWidget(self.sensor_label)
        self.sensor_cb = QtWidgets.QComboBox()
        self.sensor_cb.setFixedWidth(120)
        self.sensor_cb.addItem('dummy')
        for port in ports.get_serial_ports():
            self.sensor_cb.addItem(port)
        self.sensor_cb.currentTextChanged.connect(self.sensor_port_changed)
        hbox_ports.addWidget(self.sensor_cb)
        self.source_label = QtWidgets.QLabel("Keithley", self)
        hbox_ports.addWidget(self.source_label)
        self.source_cb = QtWidgets.QComboBox()
        self.source_cb.setFixedWidth(120)
        self.source_cb.addItem('dummy')
        self.source_cb.addItem('GPIB::24')
        hbox_ports.addWidget(self.source_cb)
        hbox_ports.addStretch(-1)
        self.refresh_button = QtWidgets.QPushButton(
            QtGui.QIcon(os.path.join(paths['icons'], 'refresh.png')), '')
        # self.refresh_button.setIconSize(QtCore.QSize(20, 20))
        self.refresh_button.clicked.connect(self.update_ports)
        self.refresh_button.setToolTip('Update Ports')
        hbox_ports.addWidget(self.refresh_button)
        self.ports_group_box.setLayout(hbox_ports)
        hbox_port_meas.addWidget(self.ports_group_box)

        self.readout_group_box = QtWidgets.QGroupBox('I-V Readout')
        hbox_readout = QtWidgets.QHBoxLayout()
        self.read_volt_label = QtWidgets.QLabel("Voltage (mV)", self)
        hbox_readout.addWidget(self.read_volt_label)
        self.read_volt_edit = QtWidgets.QLineEdit('-1', self)
        self.read_volt_edit.setFixedWidth(80)
        self.read_volt_edit.setDisabled(True)
        hbox_readout.addWidget(self.read_volt_edit)
        self.read_curr_label = QtWidgets.QLabel("Current (mA)", self)
        hbox_readout.addWidget(self.read_curr_label)
        self.read_curr_edit = QtWidgets.QLineEdit('-1', self)
        self.read_curr_edit.setFixedWidth(80)
        self.read_curr_edit.setDisabled(True)
        hbox_readout.addWidget(self.read_curr_edit)
        hbox_readout.addStretch(-1)
        self.readout_group_box.setLayout(hbox_readout)
        hbox_port_meas.addWidget(self.readout_group_box)
        vbox_port_meas_folder.addLayout(hbox_port_meas)

        self.save_group_box = QtWidgets.QGroupBox('Save')
        vbox_measure = QtWidgets.QVBoxLayout()
        hbox_folder = QtWidgets.QHBoxLayout()
        self.folder_button = QtWidgets.QPushButton(
            QtGui.QIcon(os.path.join(paths['icons'], 'folder.png')), '')
        self.folder_button.clicked.connect(self.folder_dialog)
        self.folder_button.setToolTip('Choose folder')
        hbox_folder.addWidget(self.folder_button)
        self.folder_edit = QtWidgets.QLineEdit(self.directory, self)
        self.folder_edit.setMinimumWidth(180)
        self.folder_edit.setDisabled(True)
        hbox_folder.addWidget(self.folder_edit)
        self.clipboard_button = QtWidgets.QPushButton(
            QtGui.QIcon(os.path.join(paths['icons'], 'clipboard.png')), '')
        self.clipboard_button.clicked.connect(lambda: self.clipboard('iv'))
        self.clipboard_button.setToolTip('Save plot to clipboard')
        hbox_folder.addWidget(self.clipboard_button)
        vbox_measure.addLayout(hbox_folder)
        self.save_group_box.setLayout(vbox_measure)
        vbox_port_meas_folder.addWidget(self.save_group_box)
        hbox_port_meas_folder.addLayout(vbox_port_meas_folder)
        hbox_port_meas_folder.addStretch(-1)

        self.logo_label = QtWidgets.QLabel(self)
        logo_pixmap = QtGui.QPixmap(os.path.join(paths['icons'], 'lambda.png'))
        self.logo_label.setPixmap(logo_pixmap)
        hbox_port_meas_folder.addWidget(self.logo_label)
        hbox_port_meas_folder.addStretch(-1)
        vbox_bottom_left.addLayout(hbox_port_meas_folder)
        vbox_bottom_left.addStretch(-1)
        hbox_bottom.addLayout(vbox_bottom_left, 5)

        self.log_group_box = QtWidgets.QGroupBox('Log')
        grid_log = QtWidgets.QGridLayout()
        self.log_edit = QtWidgets.QTextEdit("Ready to measure...\n", self)
        grid_log.addWidget(self.log_edit, 0, 0)
        self.log_group_box.setLayout(grid_log)
        hbox_bottom.addWidget(self.log_group_box, 3)
        vbox_total.addLayout(hbox_bottom, 2)
        self.setLayout(vbox_total)

        self.data_sensor = np.zeros((int(self.ais_edit.text()), int(self.nstep_edit.text())))
        self.plot_temperature = False
        self.plot_power = False

        self.sensor_mes = None
        self.start_sensor()

        self.iv_mes = keithley.Keithley(gpib_port='dummy')
        self.iv_register(self.iv_mes)
        self.iv_mes.update.emit(-1)

    def sensor_register(self, mes):
        self.sensor_mes = mes
        self.sensor_mes.update.connect(self.update_sensor)
        self.sensor_mes.to_log.connect(self.logger)

    @QtCore.pyqtSlot()
    def update_sensor(self):
        if not self.sensor_mes:
            return
        tval, d1val, d2val, d3val, d4val = self.sensor_mes.get_sensor_latest()
        self.temperature_edit.setText("%.2f" % tval)
        self.diode1_edit.setText("%02d" % d1val)
        self.diode2_edit.setText("%02d" % d2val)
        self.diode3_edit.setText("%02d" % d3val)
        self.diode4_edit.setText("%02d" % d4val)
        # Could enable plotting permanently as long as port is not dummy
        if self.plot_temperature and not self.sensor_mes.port == 'dummy':
            self.sensor_mes.line_plot(self.temp_data_line, channel='temp')
        if self.plot_power and not self.sensor_mes.port == 'dummy':
            self.sensor_mes.line_plot(self.power_data_line1, channel='power1')
            self.sensor_mes.line_plot(self.power_data_line2, channel='power2')
            self.sensor_mes.line_plot(self.power_data_line3, channel='power3')
            self.sensor_mes.line_plot(self.power_data_line4, channel='power4')

    def start_sensor(self):
        if self.sensor_mes:
            self.sensor_mes.stop()
        self.sensor_mes = sensor.ArduinoSensor(port=str(self.sensor_cb.currentText()),
                                               baud=int(self.baud_edit.text()),
                                               n_data_points=int(self.datapoints_edit.text()),
                                               data_num_bytes=int(self.databytes_edit.text()),
                                               n_ai=int(self.ais_edit.text()),
                                               timeout=float(self.timeout_edit.text()),
                                               query_period=float(self.query_edit.text()))
        self.sensor_register(self.sensor_mes)
        self.sensor_mes.start()

    def stop_sensor(self):
        if self.sensor_mes:
            self.sensor_mes.stop()
            self.sensor_mes = None

    def sensor_port_changed(self):
        if self.block_sensor is False:  # if combobox update is in progress, sensor_port_changed is not triggered
            self.start_sensor()

    def update_ports(self):
        self.stop_sensor()
        self.block_sensor = True
        self.sensor_cb.clear()
        self.sensor_cb.addItem('dummy')
        for port in ports.get_serial_ports():
            self.sensor_cb.addItem(port)
        self.block_sensor = False
        self.start_sensor()

    def plot_temp(self):
        if self.plot_power:
            self.plot_power = False
            self.power_button.setChecked(False)
            self.power_data_line1.setData([], [])
            self.power_data_line2.setData([], [])
            self.power_data_line3.setData([], [])
            self.power_data_line4.setData([], [])
        if not self.plot_temperature:
            self.plot_temperature = True
            self.sensor_graph.setLabel('left', 'Temperature (C)')
        else:
            self.plot_temperature = False
            self.temp_data_line.setData([], [])
            self.sensor_graph.setLabel('left', '')

    def plot_pow(self):
        if self.plot_temperature:
            self.plot_temperature = False
            self.temp_button.setChecked(False)
            self.temp_data_line.setData([], [])
        if not self.plot_power:
            self.plot_power = True
            self.sensor_graph.setLabel('left', 'Irradiation (W/m2)')
        else:
            self.plot_power = False
            self.power_data_line1.setData([], [])
            self.power_data_line2.setData([], [])
            self.power_data_line3.setData([], [])
            self.power_data_line4.setData([], [])
            self.sensor_graph.setLabel('left', '')

    def folder_dialog(self):
        self.directory = str(QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory', paths['last_save']))
        self.folder_edit.setText(self.directory)

    def iv_register(self, mes):
        self.iv_mes = mes
        self.iv_mes.update.connect(self.update_iv)
        self.iv_mes.save.connect(self.save)
        self.iv_mes.to_log.connect(self.logger)

    def start(self):
        if not self.start_button.isChecked():
            self.stop()
            return
            # self.logger('<span style=\" color:#ff0000;\" >Experiment running. Stop current experiment first.</span>')
            # self.start_button.setChecked(True)
            # return
        if self.check_iv_parameters() is False:
            return
        if self.iv_mes:
            self.iv_mes.close()
        self.iv_mes = keithley.Keithley(gpib_port=str(self.source_cb.currentText()),
                                        n_data_points=int(self.nstep_edit.text()),
                                        averages=int(self.naverage_edit.text()),
                                        repetitions=int(self.reps_edit.text()),
                                        repetition_delay=float(self.rep_delay_edit.text()),
                                        delay=float(self.delay_edit.text()),
                                        min_voltage=float(self.start_edit.text()),
                                        max_voltage=float(self.end_edit.text()),
                                        compliance_current=float(self.ilimit_edit.text()))
        self.iv_register(self.iv_mes)
        self.data_sensor = np.zeros((int(self.ais_edit.text()), int(self.nstep_edit.text())))
        self.iv_mes.read_keithley_start()

    @QtCore.pyqtSlot(int)
    def update_iv(self, datapoint):
        if not self.iv_mes:
            return
        if datapoint != -1:
            sensor_latest = self.sensor_mes.get_sensor_latest()
            for ai, val in enumerate(sensor_latest):
                self.data_sensor[ai, datapoint] = val
            self.read_volt_edit.setText("%0.1f" % (1e3*self.iv_mes.voltages_set[datapoint]))
            self.read_curr_edit.setText("%0.2f" % (1e3*self.iv_mes.currents[datapoint]))
        self.iv_mes.line_plot(self.iv_data_line)

    def stop(self):  # TODO: implement iv scan pause
        if self.iv_mes:
            self.iv_mes.close()
        self.start_button.setChecked(False)

    def clipboard(self, plot):
        if plot == 'iv':
            pixmap = QtWidgets.QWidget.grab(self.iv_graph)
        elif plot == 'sensor':
            pixmap = QtWidgets.QWidget.grab(self.sensor_graph)
        else:
            return
        QtWidgets.QApplication.clipboard().setPixmap(pixmap)

    @QtCore.pyqtSlot(int)
    def save(self, repetition):
        self.data_iv = self.iv_mes.get_keithley_data()
        self.data_iv['Temperature (C)'] = self.data_sensor[0]
        self.data_iv['Power 1 (W/m2)'] = self.data_sensor[1]
        self.data_iv['Power 2 (W/m2)'] = self.data_sensor[2]
        self.data_iv['Power 3 (W/m2)'] = self.data_sensor[3]
        self.data_iv['Power 4 (W/m2)'] = self.data_sensor[4]
        self.data_iv.to_csv(os.path.join(self.directory, 'IV_Curve_%s.csv' % str(repetition)))
        if repetition == (self.iv_mes.repetitions - 1):
            self.start_button.setChecked(False)

    @QtCore.pyqtSlot(str)
    def logger(self, string):
        self.log_edit.append(string)
        self.log_edit.moveCursor(QtGui.QTextCursor.End)

    @QtCore.pyqtSlot()
    def update_steps(self):
        try:  # capture empty cells, typos etc during data entry
            steps = (float(self.end_edit.text()) - float(self.start_edit.text())) / float(self.nstep_edit.text())
            self.step_edit.setText("%.3f" % steps)
        except (ZeroDivisionError, ValueError):
            pass

    def check_iv_parameters(self):
        try:
            int(self.nstep_edit.text())
            int(self.naverage_edit.text())
            int(self.reps_edit.text())
            float(self.rep_delay_edit.text())
            float(self.delay_edit.text())
            float(self.start_edit.text())
            float(self.end_edit.text())
            float(self.ilimit_edit.text())
        except (ZeroDivisionError, ValueError):
            self.warning('Some parameters are not in the right format. Please check before starting measurement.')
            return False
        if any([float(self.end_edit.text()) > 0.75,
                float(self.start_edit.text()) < -0.15,
                float(self.start_edit.text()) > float(self.end_edit.text()),
                float(self.delay_edit.text()) < 0.01,
                float(self.rep_delay_edit.text()) < 0.5,
                float(self.ilimit_edit.text()) > 0.5,
                float(self.ilimit_edit.text()) <= 0.,
                int(self.naverage_edit.text()) < 1,
                int(self.reps_edit.text()) < 1
                ]):
            self.warning('Parameters are out of bounds. Please check before starting the measurement. Keep positive '
                         'though, at least you didn\'t barbeque the sample :)')
            return False
        return True

    def warning(self, string):
        QtWidgets.QMessageBox.warning(self, 'Warning', string, QtWidgets.QMessageBox.Ok)
