from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, mkPen, mkBrush, TextItem

from src.ui.utils import set_minimum_expanding_size_policy


class AltitudeGraph(PlotWidget):

    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)

        self.setMinimumSize(QtCore.QSize(400, 150))
        set_minimum_expanding_size_policy(self)
        self.setObjectName("altitudeGraph")

        self.plotItem.setTitle("Altitude")
        self.plotItem.setLabel("bottom", "Temps", "Sec")
        self.plotItem.setLabel("left", "Altitude (ft)")

        self.altitude_curve = self.plot([0], [0], pen=mkPen(color='k', width=3))

        self.current_altitude = 0
        self.current_altitude_text = TextItem("", color='k')
        self.current_altitude_point = self.plotItem.scatterPlot([], [], pxMode=True, size=8, brush=mkBrush(color='r'))
        self.addItem(self.current_altitude_text)

        self.simulation_curve = None

        self.apogee = 0
        self.draw_apogee_plot = True
        self.apogee_text = TextItem("", anchor=(0.5, 1), color='b')
        self.apogee_point = self.plotItem.scatterPlot([], [], pxMode=True, size=9, brush=mkBrush(color='b'))
        self.addItem(self.apogee_text)

    def paintEvent(self, ev):
        if self.draw_apogee_plot:
            self.apogee_text.setText("{}ft".format(int(self.apogee)))

        self.current_altitude_text.setText("{}ft".format(self.current_altitude))

        super(AltitudeGraph, self).paintEvent(ev)

    def draw(self, values: list):
        nb_points = len(values)

        if nb_points > 0:
            self.current_altitude = int(values[-1])

            self.altitude_curve.setData(values)
            self.current_altitude_point.setData([nb_points - 1], [self.current_altitude])
            self.current_altitude_text.setPos(nb_points - 1, self.current_altitude)

    def set_target_altitude(self, altitude):
        self.plotItem.addLine(y=altitude, pen=mkPen(color=(15, 236, 20), width=3, style=QtCore.Qt.DashDotLine))

    def show_simulation(self, time: list, altitude: list):
        if self.simulation_curve is None:
            self.simulation_curve = self.plot(time, altitude, pen=mkPen(color='b', width=3))
        else:
            self.simulation_curve.setData(time, altitude)

    def draw_apogee(self, values: list):
        if len(values) == 2:
            self.apogee = values[0]
            apogee_index = values[1]

            if not self.draw_apogee_plot:
                self.apogee_text.setColor(color='b')
                self.apogee_point = self.plotItem.scatterPlot([apogee_index], [self.apogee], pxMode=True, size=9, brush=mkBrush(color='b'))
                self.addItem(self.apogee_point)

                self.apogee_text.setPos(apogee_index, self.apogee)

                self.draw_apogee_plot = True
        else:
            if self.draw_apogee_plot:
                self.apogee_text.setColor(color=(0, 0, 0, 0))
                self.apogee_text.setPos(10, self.apogee)
                self.removeItem(self.apogee_point)

                self.draw_apogee_plot = False
