
# Integration test towards external modbus server
#
# This test checks that the modbus gateway can connect to an external modbus server and parse the data correctly
#

import pytest

import pymodbus.constants

import src.modbus_gateway.core as core
import src.modbus_gateway.utils as utils

@pytest.mark.integration
def test_integration_external():
    # Create modbus gateway

    gateway = core.ModbusGateway(
        "docencia.i4techlab.upc.edu",
        20000,
        40,
        pymodbus.constants.Endian.Big,
        pymodbus.constants.Endian.Little
    )

    # Configure tags

    gateway.configure_tags(
        [
            {
                "name": "var1",
                "address": 0,
                "memory_bank": utils.MemoryBank.HOLDING,
                "datatype": "float32",
            },
            {
                "name": "var2",
                "address": 1,
                "memory_bank": utils.MemoryBank.HOLDING,
                "datatype": "float32",
            }
        ]
    )

    # Read tags

    results = gateway.read_tags()

    # Check results

    assert len(results) == 2

    assert results[0].name == "var1"
    assert results[0].address == 0
    assert results[0].datatype == "float32"
    assert results[0].value == 1.0