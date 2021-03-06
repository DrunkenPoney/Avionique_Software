import abc
import threading
from typing import List

from src.rocket_packet.rocket_packet import RocketPacket


class DataProducer:
    __metaclass__ = abc.ABCMeta

    def __init__(self, lock: threading.RLock):
        self.available_rocket_packets = []
        self.lock = lock
        self.is_running = False
        self.thread = None

    @abc.abstractmethod
    def start(self):
        """Start acquisition thread"""
        pass

    def stop(self):
        self.is_running = False
        self.thread.join()

    def get_available_rocket_packets(self) -> List[RocketPacket]:
        self.lock.acquire()
        packet_list = list(self.available_rocket_packets)
        self.lock.release()

        return packet_list

    def add_rocket_packet(self, rocket_packet: RocketPacket):
        self.lock.acquire()
        self.available_rocket_packets.append(rocket_packet)
        self.lock.release()

    @abc.abstractmethod
    def clear_rocket_packets(self):
        pass

    @abc.abstractmethod
    def run(self):
        """Acquisition thread function"""
        pass
