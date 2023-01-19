# Integration test towards external modbus server
#
# This test checks that the modbus gateway can connect to an external modbus server and parse the data correctly
#

import time
import pytest

import pymodbus.constants

import modbus_connect.connect as connect
import modbus_connect.tags as tags
from modbus_connect.tags import Tag, MemoryTypes, DataTypes

import tests.mock_modbus


def test_integration_external():
    # Arrange

    # Create modbus server mock

    thread = tests.mock_modbus.run_mock_thread()

    # Create modbus gateway

    gateway = connect.ModbusConnector("localhost", 5020)

    try:
        while not gateway.connected:
            print("Trying to connect...")
            time.sleep(1)
            gateway.connect()

    except Exception as e:
        print(e)

    # Configure tags
    print(gateway.connected)
    tags_list = [
        Tag("var1", 0, MemoryTypes.HOLDING_REGISTERS, DataTypes.INT32),
        Tag("var2", 2, MemoryTypes.HOLDING_REGISTERS, DataTypes.INT32),
    ]

    gateway.set_tags(tags_list)

    # Act

    results = None

    # Read tags
    try:
        results = gateway.read_tags()
    except Exception as e:
        print(e)
    # Assert

    # Check results

    assert len(results) == 2

    assert results[0].tag.name == "var1"
    assert results[0].tag.address == 0
    assert results[0].tag.datatype == DataTypes.INT32
    assert results[0].value == 4

    # Cleanup

    # No cleanup needed
