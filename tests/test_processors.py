import pytest

import pymodbus.register_read_message
import pymodbus.bit_read_message
import pymodbus.constants

import modbus_connect.processors as processors
import modbus_connect.utils as utils
from modbus_connect.utils import ModbusRegister, MemoryBanks, DataTypes


def test_process_holding_registers():
    batch = [
        ModbusRegister("var1", 0, MemoryBanks.HOLDING_REGISTERS, DataTypes.INT32),
        ModbusRegister("var2", 2, MemoryBanks.HOLDING_REGISTERS, DataTypes.INT32),
    ]

    batch_results = pymodbus.register_read_message.ReadHoldingRegistersResponse(
        [0, 4, 0, 8]
    )

    results = process_batch(batch, batch_results, pymodbus.constants.Endian.Big, pymodbus.constants.Endian.Big)

    # Check the results

    assert len(results) == len(batch)
    assert results[0].tag.name == batch[0].name
    assert results[0].tag.address == batch[0].address
    assert results[0].tag.memorybank == batch[0].memorybank
    assert results[0].tag.datatype == batch[0].datatype
    assert (
        results[0].value
        == batch_results.registers[0] * 65536
        + batch_results.registers[1]
    )


def test_process_coils_registers():
    batch = [
        ModbusRegister("var1", 0, MemoryBanks.COILS, DataTypes.BOOL),
        ModbusRegister("var2", 1, MemoryBanks.COILS, DataTypes.BOOL),
    ]

    batch_results = pymodbus.bit_read_message.ReadCoilsResponse([True, False])
    
    results = process_batch(batch, batch_results, pymodbus.constants.Endian.Big, pymodbus.constants.Endian.Big)

    assert len(results) == len(batch)
    assert results[0].tag.name == batch[0].name
    assert results[0].tag.address == batch[0].address
    assert results[0].tag.memorybank == batch[0].memorybank
    assert results[0].tag.datatype == batch[0].datatype
    assert results[0].value == batch_results.bits[0]


def process_batch(batch, batch_results, byte_order, word_order):
    # Process the batch

    return processors.process_batch(
        batch,
        batch_results,
        byte_order,
        word_order,
    )
