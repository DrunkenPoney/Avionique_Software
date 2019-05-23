import struct

from src.rocket_packet.rocket_packet import RocketPacket
from src.rocket_packet.rocket_packet_parser import RocketPacketParser


class RocketPacketParser2019(RocketPacketParser):

    def __init__(self):
        super().__init__(2019, "<dddccdfIfHHHfffHHHHHH", 76)

    def parse(self, data: bytes):
        # TODO: support all fields
        data_list = struct.unpack(self.format, data)
        return self.from_list(data_list)

    def get_field_names(self):
        return ["time_stamp", "latitude", "longitude", "ns_indicator", "ew_indicator", "utc_time", "altitude",
                "pressure", "temperature", "acceleration_x_uncomp", "acceleration_y_uncomp", "acceleration_z_uncomp",
                "acceleration_x", "acceleration_y", "acceleration_z", "magnetometer_x", "magnetometer_y",
                "magnetometer_z", "angular_speed_x", "angular_speed_y", "angular_speed_z"]

    def to_list(self, packet: RocketPacket) -> list:
        return [packet.time_stamp, packet.latitude, packet.longitude, b'N', b'W', packet.UTCtime, packet.altitude,
                packet.pressure, packet.temperature, 0, 0, 0, packet.acceleration_x, packet.acceleration_y,
                packet.acceleration_z, packet.magnetometer_x, packet.magnetometer_y, packet.magnetometer_z,
                packet.angular_speed_x, packet.angular_speed_y, packet.angular_speed_z]

    def from_list(self, data: list) -> RocketPacket:
        rocket_packet = RocketPacket()

        rocket_packet.time_stamp = data[0]
        rocket_packet.latitude = data[1]
        rocket_packet.longitude = data[2]

        rocket_packet.NSIndicator = data[3]
        rocket_packet.EWIndicator = data[4]
        rocket_packet.UTCtime = data[5]

        rocket_packet.altitude = data[6]
        rocket_packet.pressure = data[7]
        rocket_packet.temperature = data[8]

        rocket_packet.acceleration_x = data[12]
        rocket_packet.acceleration_y = data[13]
        rocket_packet.acceleration_z = data[14]

        rocket_packet.magnetometer_x = data[15]
        rocket_packet.magnetometer_y = data[16]
        rocket_packet.magnetometer_z = data[17]

        rocket_packet.angular_speed_x = data[18]
        rocket_packet.angular_speed_y = data[19]
        rocket_packet.angular_speed_z = data[20]

        return rocket_packet
