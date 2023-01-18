
import pymodbus.client.tcp
from modbus_connect import tags

import tests.mock_modbus

# Import gateway module

import modbus_connect.client as client


# Test Client class creates the correct client


def test_client_class_creates_correct_client():
    # Arrange

    device_config = client.ModbusConfig("localhost", 502, 1, 1)

    # Act

    modbus_client = client.ModbusClient(device_config)

    # Assert

    assert modbus_client.client is not None
    assert isinstance(modbus_client.client, pymodbus.client.tcp.ModbusTcpClient)

# Test Client class resets the client

def test_client_class_resets_client():
    # Arrange

    device_config = client.ModbusConfig("localhost", 502, 1, 1)

    modbus_client = client.ModbusClient(device_config)

    old_client = modbus_client.client

    # Act

    modbus_client.reset()

    # Assert

    assert modbus_client.client is not None
    assert modbus_client.client != old_client


# Test Client class connects to the client

def test_client_class_connects_to_client():

    # Arrange

    port = 10502

    device_config = client.ModbusConfig("localhost", port, 1, 1)

    modbus_client = client.ModbusClient(device_config)

    thread = tests.mock_modbus.run_mock_thread(port)

    # Act

    modbus_client.connect()

    # Assert

    assert modbus_client.client is not None
    assert modbus_client.client.connected


# Test client read registers from mock server

def test_client_read_registers_from_mock_server():

    # Arrange

    port = 10502

    device_config = client.ModbusConfig("localhost", port, 1, 1)

    modbus_client = client.ModbusClient(device_config)

    thread = tests.mock_modbus.run_mock_thread(port)

    modbus_client.connect()

    # Act

    result = modbus_client.get_registers(tags.MemoryTypes.HOLDING_REGISTERS, 0, 2)

    # Assert

    assert result is not None
    assert result.registers == [4, 0]


