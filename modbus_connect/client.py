from dataclasses import dataclass

import logging
import time

import pymodbus
import pymodbus.register_read_message
import pymodbus.client.tcp
import pymodbus.payload
import pymodbus.constants

import modbus_connect.tags as tags
import modbus_connect.processors as processors

logger = logging.getLogger()


@dataclass
class ModbusConfig:
    host: str
    port: int
    slave: int = 1
    request_timeout: int = 3
    reconnect_timeout: int = 3
    retryes: int = 3


class ModbusClient:
    def __init__(
        self,
        modbus_config: ModbusConfig,
    ):
        self.modbus_config = modbus_config

        self.client = pymodbus.client.tcp.ModbusTcpClient(
            self.modbus_config.host,
            self.modbus_config.port,
            timeout=self.modbus_config.request_timeout,
        )

    def reset(self):
        self.client.close()
        self.client = pymodbus.client.tcp.ModbusTcpClient(
            self.modbus_config.host,
            self.modbus_config.port,
            timeout=self.modbus_config.request_timeout,
        )

    def connect(self):
        retry_counter = 0
        start = time.time()
        self.client.connect()
        while not self.client.is_socket_open():
            if time.time() - start > self.modbus_config.reconnect_timeout:
                if retry_counter > self.modbus_config.retryes:
                    raise Exception(
                        "Could not connect to modbus server after "
                        + str(self.modbus_config.reconnect_timeout)
                        + " seconds"
                    )
                else:
                    retry_counter += 1
                    start = time.time()
                    self.reset()
                    self.client.connect()
            time.sleep(0.5)

    @property
    def connected(self) -> bool:
        return self.client.is_socket_open()

    def __del__(self):
        self.client.close()

    def get_registers(
        self, memory_type: tags.MemoryTypes, address: int, memory_length: int
    ) -> processors.RegisterResponse:
        if (
            memory_type != tags.MemoryTypes.HOLDING_REGISTERS
            and memory_type != tags.MemoryTypes.INPUT_REGISTERS
            and memory_type != tags.MemoryTypes.DISCRETE_INPUTS
            and memory_type != tags.MemoryTypes.COILS
        ):
            raise Exception("Non supported memory bank")

        return self.__read_registers(memory_type, address, memory_length)

    def __read_registers(
        self,
        memory_type: tags.MemoryTypes,
        address: int,
        memory_length: int,
    ) -> processors.RegisterResponse:
        try:
            if memory_type == tags.MemoryTypes.HOLDING_REGISTERS:
                results = self.client.read_holding_registers(
                    address,
                    count=memory_length,
                    slave=self.modbus_config.slave,
                )
            elif memory_type == tags.MemoryTypes.INPUT_REGISTERS:
                results = self.client.read_input_registers(
                    address,
                    count=memory_length,
                    slave=self.modbus_config.slave,
                )
            elif memory_type == tags.MemoryTypes.DISCRETE_INPUTS:
                results = self.client.read_discrete_inputs(
                    address,
                    count=memory_length,
                    slave=self.modbus_config.slave,
                )
            elif memory_type == tags.MemoryTypes.COILS:
                results = self.client.read_coils(
                    address,
                    count=memory_length,
                    slave=self.modbus_config.slave,
                )

            if results.isError():
                raise Exception("Modbus error: " + str(results))

            return results

        except Exception as e:
            raise Exception(
                "Error reading from modbus server from address "
                + str(address)
                + " and length "
                + str(memory_length)
            )
