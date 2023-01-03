from typing import List
from dataclasses import dataclass, field

import logging

import pymodbus
import pymodbus.register_read_message
import pymodbus.client.tcp
import pymodbus.payload
import pymodbus.constants

import src.modbus_gateway.utils as utils
import src.modbus_gateway.processors as processors


logger = logging.getLogger()


class ModbusGateway:
    def __init__(
        self,
        host: str,
        port: int,
        timeout: int = 3,
        tags_list: List[utils.ModbusRegister] = [],
        batch_size=60,
        byteorder: pymodbus.constants.Endian = pymodbus.constants.Endian.Big,
        wordorder: pymodbus.constants.Endian = pymodbus.constants.Endian.Little,
    ):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.batch_size = batch_size
        self.tags_list = tags_list
        self.byte_order = byteorder
        self.word_order = wordorder

        # Create modbus server connections using pymodbus library, using the host and port parameters, using the ModbusTcpClient class¡
        self.client = pymodbus.client.tcp.ModbusTcpClient(
            self.host, self.port, timeout=self.timeout
        )
        self.tags_requests = utils.ModbusRegistersGroupsBatched()

        if self.tags_list != []:
            self.configure_tags()

    def __del__(self):
        self.client.close()

    def connect(self):
        self.client.connect()

    def set_tags_list(self, tags_list: List[utils.ModbusRegister]):
        self.tags_list = tags_list
        self.tags_requests = utils.ModbusRegistersGroupsBatched()

    def configure_tags(self):
        # Temporal storage of tags, where the memory bank is the key of the dictionary
        tags_groups: utils.ModbusRegistersGroups = utils.ModbusRegistersGroups()

        for tag in self.tags_list:
            bank = getattr(tags_groups, tag.memorybank.value)
            bank.append(tag)
            setattr(tags_groups, tag.memorybank.value, bank)

        # For each tags_request, sort the list of dictionaries by address and the make batches of consecutive addresses with a maximum size of self.batch_size
        for memory_bank, tags in tags_groups.__dict__.items():
            tags.sort(key=lambda x: x.address)
            setattr(
                self.tags_requests,
                memory_bank,
                utils.make_batch_consecutive_sized(tags, self.batch_size),
            )

    # Get variables values from modbus server
    # It gets the values in batches of 60 variables, using the address from the tags dictionary, and returns a dictionary with tha varibles names as keys and the server values
    def read_tags(self) -> utils.ModbusResults:
        values: utils.ModbusResults = utils.ModbusResults([])

        for group in dataclass.fields(self.tags_requests):
            if memorybank == utils.MemoryBanks.HOLDING_REGISTERS:
                batches_results: pymodbus.register_read_message.ReadHoldingRegistersResponse = (
                    []
                )
                for batch in batches:
                    try:
                        batch_results = self.client.read_holding_registers(
                            batch[0].address, count=len(batch), slave=1
                        )
                        if batch_results.isError():
                            raise Exception("Modbus error: " + str(batch_results))
                    except Exception as e:
                        raise Exception(
                            "Error reading from modbus server from address "
                            + str(batch[0].address)
                            + " to address "
                            + str(batch[-1].address)
                        )
                    batches_results.append(batch_results)

                values.holding_registers = processors.process_holding_registers(
                    batches, batches_results, self.byte_order, self.word_order
                )

            elif memorybank == utils.MemoryBanks.INPUT_REGISTERS:
                # TODO: Implement input registers read
                raise NotImplementedError("Input registers not implemented")

            elif memorybank == utils.MemoryBanks.DISCRETE_INPUTS:
                # TODO: Implement discrete inputs read
                raise NotImplementedError("Discrete inputs not implemented")

            elif memorybank == utils.MemoryBanks.COILS:
                # TODO: Implement coils read
                raise NotImplementedError("Coils not implemented")

        return values

    def tags_ready(self) -> bool:
        return len(self.tags) > 0


if __name__ == "__main__":
    # Create a ModbusGateway object, using the host and port parameters, and the tags_list parameter, which is a list of dictionaries with the variable names and memory addresses
    gateway = ModbusGateway(
        host="docencia.i4techlab.upc.edu",
        port=20000,
        tags_list=[
            {
                "name": "var1",
                "address": 0,
                "memory_bank": utils.MemoryBanks.HOLDING_REGISTERS,
                "datatype": "float32",
            },
            {
                "name": "var2",
                "address": 1,
                "memory_bank": utils.MemoryBanks.HOLDING_REGISTERS,
                "datatype": "float32",
            },
        ],
    )

    # Read the values from the modbus server
    values = gateway.read_tags()
    print(values)
    logger.info(values)
