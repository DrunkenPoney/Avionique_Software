from src.consumer import Consumer
from src.controller import Controller
from src.file_reader import FileReader
from src.ui.replay_widget import ReplayWidget


class ReplayController(Controller):

    def __init__(self, replay_widget: ReplayWidget, filename: str):
        super().__init__()
        self.data_widget = replay_widget
        self.producer = FileReader(filename)
        self.consumer = Consumer(self.producer, self.sampling_frequency)
        self.consumer.update()
        self.update_plots()
