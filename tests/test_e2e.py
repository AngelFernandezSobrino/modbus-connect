# Integration test towards external modbus server
#
# This test checks that the modbus gateway can connect to an external modbus server and parse the data correctly
#

import time
import pytest

import pymodbus.constants

import src.modbus_connect.core as core
import src.modbus_connect.utils as utils
from src.modbus_connect.utils import ModbusRegister, MemoryBanks, DataTypes

import tests.mock_modbus


def test_integration_external():

    # Arrange

    # Create modbus server mock

    thread = tests.mock_modbus.run_mock_thread()

    # Create modbus gateway

    gateway = core.ModbusGateway("localhost", 5020)

    try:
        while not gateway.client.is_socket_open():
            print("Trying to connect...")
            time.sleep(1)
            gateway.connect()

    except Exception as e:
        print(e)

    # Configure tags
    print(gateway.client.is_socket_open())
    tags_list = [
        ModbusRegister("var1", 0, MemoryBanks.HOLDING_REGISTERS, DataTypes.INT32),
        ModbusRegister("var2", 2, MemoryBanks.HOLDING_REGISTERS, DataTypes.INT32),
    ]

    gateway.set_tags_list(tags_list)

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
