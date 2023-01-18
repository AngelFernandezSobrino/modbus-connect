import pytest

import pymodbus.register_read_message
import pymodbus.bit_read_message
import pymodbus.constants

import modbus_connect.processors as processors
import modbus_connect.tags as tags
from modbus_connect.tags import Tag, MemoryTypes, DataTypes


def test_process_holding_registers():
    batch = tags.Batch([
        Tag(
            "var1", 0, MemoryTypes.HOLDING_REGISTERS, DataTypes.INT32
        ),
        Tag(
            "var2", 2, MemoryTypes.HOLDING_REGISTERS, DataTypes.INT32
        ),
    ])

    batch_results = (
        pymodbus.register_read_message.ReadHoldingRegistersResponse(
            [0, 4, 0, 8]
        )
    )

    results = process_batch(
        batch,
        batch_results,
        pymodbus.constants.Endian.Big,
        pymodbus.constants.Endian.Big,
    )

    # Check the results

    assert len(results) == len(batch)
    assert results[0].tag.name == batch[0].name
    assert results[0].tag.address == batch[0].address
    assert results[0].tag.memorytype == batch[0].memorytype
    assert results[0].tag.datatype == batch[0].datatype
    assert (
        results[0].value
        == batch_results.registers[0] * 65536 + batch_results.registers[1]
    )


def test_process_coils_registers():
    batch = tags.Batch([
        Tag("var1", 0, MemoryTypes.COILS, DataTypes.BOOL),
        Tag("var2", 1, MemoryTypes.COILS, DataTypes.BOOL),
    ])

    batch_results = pymodbus.bit_read_message.ReadCoilsResponse([True, False])

    results = process_batch(
        batch,
        batch_results,
        pymodbus.constants.Endian.Big,
        pymodbus.constants.Endian.Big,
    )

    assert len(results) == len(batch)
    assert results[0].tag.name == batch[0].name
    assert results[0].tag.address == batch[0].address
    assert results[0].tag.memorytype == batch[0].memorytype
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
