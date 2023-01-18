from typing import List
from dataclasses import dataclass, field

import logging

import pymodbus
import pymodbus.register_read_message
import pymodbus.client.tcp
import pymodbus.payload
import pymodbus.constants

import modbus_connect.tags as tags
import modbus_connect.processors as processors
import modbus_connect.client as client

logger = logging.getLogger()


class ModbusConnector:
    def __init__(
        self,
        device_config: client.ModbusConfig,
        tags: tags.Tags | None = None,
        tags_dict: List[tags.Tag] | None = None,
        batch_size: int = 60,
        byteorder: pymodbus.constants.Endian = pymodbus.constants.Endian.Big,
        wordorder: pymodbus.constants.Endian = pymodbus.constants.Endian.Little,
    ):
        self.batch_size = batch_size
        self.byte_order = byteorder
        self.word_order = wordorder
        self.device_config = device_config

        self.tags = tags

        if tags_dict is not None:
            self.set_tags_by_dict(tags_dict)

        self.client = client.ModbusClient(device_config)

    def connect(self):
        self.client.connect()
        return True

    @property
    def connected(self) -> bool:
        return self.client.client.is_socket_open()

    def set_tags(self, tags: tags.Tags):
        self.tags = tags

    def set_tags_by_dict(self, tags_dict: dict[str, tags.Tag]):
        self.tags = tags.Tags(tags_dict, self.batch_size)

    # Get variables values from modbus server
    # It gets the values in batches of 60 variables, using the address from the tags dictionary, and returns a dictionary with tha varibles names as keys and the server values
    def read_tags(self) -> tags.Results:
        values: tags.Results = tags.Results([])

        # For each batch of tags, read the values from the modbus server and process them
        for batch in self.tags.batches:
            if len(batch) == 0:
                continue

            try:
                values += processors.process_batch(
                    batch,
                    self.client.get_registers(batch[0].memorytype, batch[0].address, batch.memory_length),
                    self.byte_order,
                    self.word_order,
                )
            except Exception as e:
                logger.error(e)
                continue

        return values

    @property
    def tags_ready(self) -> bool:
        return self.tags.ready
