from PyQt4 import QtGui, QtCore
from .flight_dataUI import Ui_Dialog
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import time
import matplotlib.animation as Animation
import numpy as np
#from .data_processing import DataProcessing
from ..communication.serialReader import SerialReader as SR
from ..rocket_data import rocket_packet

class LoopThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.fd = FlightData()
        self.checkThread = True
        self.signal = QtCore.SIGNAL("signal")
    def run(self):
        while True:
            self.emit(self.signal,"Hi from Thread")
            time.sleep(1)
            # As long as thread is on
            print("Still on baby")

    def stop(self):
        """Thread is supposed to end there"""
        self.connect(self.fd, self.fd.signal, self.terminate)

class FlightData(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.signal = QtCore.SIGNAL("signal")

        self.figs = {}  # Empty Dictionnary
        self.canvas = {}  # Empty Dictionnary
        self.axs = {}  # Empty Dictionnary

        plot_names = ['speed', 'height', 'map', 'angle']
        for pn in plot_names:
            fig = Figure()  # Give the variable fig the function Figure()
            self.canvas[pn] = FigureCanvas(fig)  # Creates the key pn and assiociates it with FigureCanvas
            ax = fig.add_subplot(1, 1, 1)  # Creates a plot

            self.figs[pn] = fig  # Each string of plot_names are a Figure()
            self.axs[pn] = ax  # Each string of plot_names are a plot defined by ax"""
        self.data_list = []
        self.data_list1 = []
        self.data_list2 = []
        self.data_list3 = []
        self.end_flag = False
        self.speedLayout.addWidget(self.canvas['speed'])  # Creates the canvas for speed
        self.heightLayout.addWidget(self.canvas['height'])  # Creates the canvas for height
        self.mapLayout.addWidget(self.canvas['map'])  # Creates the canvas for map
        self.angleLayout.addWidget(self.canvas['angle'])  # Creates the canvas for angle
        self.init_widgets()  # Once the Dialog exist, automatically initiate self.
        #self.ani = Animation.FuncAnimation(self.figs["speed"], self.generate_random_list, interval = 1000)


    def init_widgets(self)
        self.analyseButton.clicked.connect(self.open_analysedata)
        self.stopButton.clicked.connect(self.stop_plotting)
        self.startButton.clicked.connect(self.start_plotting)
        #self.showlcd([10, 2, 14])


    def open_analysedata(self):
        self.done(2)  # Closes and deletes Dialog Window and return the integer 2 to main_window.py which will
        #              connect to and open analysis.py

    def stop_plotting(self):
        self.end_flag = True
        self.ani._stop()
        self.data_thread.quit()
        self.emit(self.signal, "Hi from main")

    def start_plotting(self):
        self.ani = Animation.FuncAnimation(self.figs["speed"], self.generate_random_list, interval= 1000)
        self.data_thread = LoopThread()
        self.data_thread.start()
        self.connect(self.data_thread, self.data_thread.signal, self.draw_plots)

    def draw_plots(self):
        self.draw_plot("speed", self.data_list)
        self.draw_plot("height", self.data_list1)
        self.draw_plot("map", self.data_list2)
        self.draw_plot("angle", self.data_list3)

    def draw_plot(self, target, data):
        self.axs[target].plot(data, '-*')  # Will plot with one of the 4 plot_names and any given data in a list
        self.canvas[target].draw()

    def generate_random_list(self, i):
        self.axs["height"].clear()
        self.axs["speed"].clear()
        self.axs["map"].clear()
        self.axs["angle"].clear()

        self.data_list.append(random.randrange(0, 100))
        j = self.data_list[len(self.data_list)-1]
        self.data_list1.append(j+random.randrange(-10, 10))
        self.data_list2.append(j*random.randrange(0, 5))
        self.data_list3.append(j/random.randrange(1, 10))

    def generate_cosinus(self, i):
        cos = np.cos
        yar = []
        yar1 = []
        yar2 = []
        yar3 = []
        for pn in ['speed', 'height', 'map', 'angle']:
            self.axs[pn].clear()

        for j in range(i):
            yar.append((cos((i*500/1000)*np.pi)))

        for obj in yar:
            yar1.append(obj/4)
            yar2.append(obj*20)
            yar3.append(obj/10)

        self.draw_plot("height", yar)
        self.draw_plot("speed", yar1)
        self.draw_plot("map", self.yar2)
        self.draw_plot("angle", yar3)

    def showlcd(self, data):
        speed = data[len(data)-1]
        text = str(speed)
        self.speedLCD.display(text)
