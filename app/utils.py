import json
import time
from uuid import getnode
from collections.abc import Iterator

from app import constants
from app.exceptions import InvalidSystemClockException, GetHardwareIdFailedException


class ExtendedEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Iterator):
            return list(o)
        return json.JSONEncoder.default(self, o)


class Snowflake:
    """
    id format
    timestamp  | machine_id| sequence
    41        | 10        | 12
    """

    def __init__(self):
        self.machine_id_bits = 10
        self.sequence_bits = 12
        self.max_machine_id = -1 ^ (-1 << self.machine_id_bits)
        self.machine_id_shift = self.sequence_bits
        self.timestamp_left_shift = self.sequence_bits + self.machine_id_bits
        self.twepoch = constants.TWEPOCH
        self.machine_id = self.get_machine_id()
        self.sequence_max = 2 ** 12  # 4096
        self.last_timestamp = -1
        self.sequence = 0

    @staticmethod
    def get_system_millisecond():
        """获取系统微妙数"""
        return int(round(time.time() * 1000))

    def till_next_millis(self, last_timestamp):
        """获取下一个微妙数"""
        timestamp = self.get_system_millisecond()
        while timestamp <= last_timestamp:
            timestamp = self.get_system_millisecond()
        return timestamp

    def get_machine_id(self):
        """获取机器id"""
        mac_id = getnode()
        machine_id = mac_id & self.max_machine_id
        if machine_id > self.max_machine_id or machine_id < 0:
            raise GetHardwareIdFailedException(
                'MachineId must be less than max_machine_id'
            )
        return machine_id

    def generate_id(self):
        """生成id"""
        timestamp = self.get_system_millisecond()
        if timestamp < self.last_timestamp:
            raise InvalidSystemClockException(
                f'Clock moved backwards. Refusing to generate id for {self.last_timestamp - timestamp} milliseconds'
            )
        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) % self.sequence_max
            if self.sequence == 0:
                timestamp = self.till_next_millis(self.last_timestamp)
        else:
            self.sequence = 0
        self.last_timestamp = timestamp
        _id = (
            ((timestamp - self.twepoch) << self.timestamp_left_shift)
            | (self.machine_id << self.machine_id_shift)
            | self.sequence
        )
        return _id
