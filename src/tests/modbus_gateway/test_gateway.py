# Test gateway core methods

# Import gateway module

import src.modbus_gateway.core as core
import pymodbus.constants
import src.modbus_gateway.utils as utils
from src.modbus_gateway.utils import MemoryBanks, ModbusRegister, DataTypes


# Test that ModbusGateway constructor sets the correct values for the attributes


def test_modbus_gateway_constructor():
    # Create gateway

    gateway = core.ModbusGateway("localhost", 502)

    # Check attributes

    assert gateway.host == "localhost"
    assert gateway.port == 502
    assert gateway.timeout == 3
    assert gateway.batch_size == 60
    assert gateway.tags_list == []
    assert gateway.byte_order == pymodbus.constants.Endian.Big
    assert gateway.word_order == pymodbus.constants.Endian.Little
    assert gateway.client is not None


def test_modbus_gateway_set_tags_list():
    # Create gateway

    gateway = core.ModbusGateway("localhost", 502)

    # Set tags list

    gateway.set_tags_list(
        [
            ModbusRegister(
                "var1", 0, MemoryBanks.HOLDING_REGISTERS, "float32"
            )
        ]
    )

    # Check tags list

    assert len(gateway.tags_list) == 1
    assert gateway.tags_list[0].name == "var1"
    assert gateway.tags_list[0].address == 0
    assert gateway.tags_list[0].memorybank == MemoryBanks.HOLDING_REGISTERS
    assert gateway.tags_list[0].datatype == "float32"


def test_modbus_gateway_configure_tags():
    # Create gateway

    gateway = core.ModbusGateway("localhost", 502)

    # Set tags list

    gateway.set_tags_list(
        [
            ModbusRegister(
                "var1", 0, MemoryBanks.HOLDING_REGISTERS, DataTypes.FLOAT32
            ),
            ModbusRegister(
                "var2", 2, MemoryBanks.HOLDING_REGISTERS, DataTypes.FLOAT32
            ),
            ModbusRegister(
                "var3", 0, MemoryBanks.COILS, DataTypes.BOOL
            ),
            ModbusRegister(
                "var4", 1, MemoryBanks.COILS, DataTypes.BOOL
            )
        ]
    )

    # Configure tags

    gateway.configure_tags()

    # Check tags configuration

    assert len(gateway.tags_requests) == 2
    assert len(gateway.tags_requests[0]) == 2
    assert len(gateway.tags_requests[1]) == 2
    assert gateway.tags_requests[1][0].name == "var1"
    assert gateway.tags_requests[1][1].name == "var2"
    assert gateway.tags_requests[0][0].name == "var3"
    assert gateway.tags_requests[0][1].name == "var4"