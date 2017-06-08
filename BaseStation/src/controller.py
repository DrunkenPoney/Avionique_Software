from threading import Thread
from src.serial_reader import SerialReader
from src.FileReader import FileReader
from src.consumer import Consumer
from src.ui.real_time_widget import RealTimeWidget
from src.ui.replay_widget import ReplayWidget


class Controller:
    def __init__(self):
        self.data_widget = None
        self.filename = ""
        self.is_running = False
        self.producer = None
        self.consumer = None
        self.target_altitude = 10000
        self.thread = Thread(self.drawing_thread)

    def set_filename(self, filename):
        assert isinstance(filename, str)
        self.filename = filename

    def drawing_thread(self):
        while self.is_running:
            self.consumer.update()
            if self.consumer.has_new_data:
                self.draw_plots()
                self.consumer.has_new_data = False

    def draw_plots(self):
        # TODO: draw plots and update
        self.data_widget.draw_altitude(self.consumer["altitude"], self.target_altitude)

    def init_real_time_mode(self, real_time_widget):
        assert isinstance(real_time_widget, RealTimeWidget)
        self.data_widget = real_time_widget
        self.producer = SerialReader()

    def init_replay_mode(self, replay_widget):
        assert isinstance(replay_widget, ReplayWidget)
        self.data_widget = replay_widget
        self.producer = FileReader(self.filename)
        self.consumer = Consumer(self.producer)
        self.consumer.update()
        self.draw_plots()

    def start_thread(self):
        self.consumer = Consumer(self.producer)
        self.producer.start()
        self.is_running = True
        self.thread.start()

    def stop_thread(self):
        self.is_running = False
        self.thread.join()
        self.producer.stop()

    # TODO: add ui event processing methods here
