import pytest

import modbus_connect.connect as connect
import pymodbus.constants
import modbus_connect.tags as tags
import modbus_connect.client as client
from modbus_connect.tags import MemoryTypes, DataTypes, Tag


def test_constructor(tags_list):
    # Arrange

    device_config = client.ModbusConfig("localhost", 0, 1, 1)

    # Act

    connector = connect.ModbusConnector(device_config, tags_list)

    # Check attributes

    assert connector.device_config == device_config
    assert connector.byte_order == pymodbus.constants.Endian.Big
    assert connector.word_order == pymodbus.constants.Endian.Little
    assert connector.client is not None


def test_connection(mock_modbus_server):
    # Arrange

    connector = connect.ModbusConnector(
        client.ModbusConfig("localhost", mock_modbus_server, 1, 1)
    )

    # Act

    result = connector.connect()

    # Assert
    assert result == True
    assert connector.client is not None
    assert connector.connected == True
    assert (
        connector.client.client.socket.getpeername()[1] == mock_modbus_server
    )


@pytest.mark.parametrize("batch_size", [5, 10, 60])
def test_tags_loading(tags_list, batch_size):
    # Arrange

    connector = connect.ModbusConnector(
        client.ModbusConfig("localhost", 0, 1, 1)
    )

    # Act

    connector.set_tags(tags.Tags(tags_list, batch_size))

    # Assert

    assert len(connector.tags.tags) == len(tags_list)
    for batch in connector.tags.batches:
        assert len(batch) <= batch_size
    assert connector.tags.ready


@pytest.mark.parametrize("batch_size", [5, 10, 60])
def test_tags_loading_by_dict(tags_list, batch_size):
    # Arrange

    connector = connect.ModbusConnector(
        client.ModbusConfig("localhost", 0, 1, 1), batch_size=batch_size
    )

    # Act

    connector.set_tags_by_dict(tags_list)

    # Assert

    assert len(connector.tags.tags) == len(tags_list)
    for batch in connector.tags.batches:
        assert len(batch) <= batch_size
    assert connector.tags.ready


@pytest.mark.parametrize("batch_size", [5, 10, 60])
def test_read_tags(mock_modbus_server, tags_list_mock, batch_size):
    # Arrange

    connector = connect.ModbusConnector(
        client.ModbusConfig("localhost", mock_modbus_server, 1, 1),
        batch_size=batch_size,
        tags_dict=tags_list_mock
    )

    connector.connect()

    # Act

    result = connector.read_tags()

    # Assert

    assert len(result) == len(tags_list_mock)
    assert result[0].tag.name == "var1"
    assert result[0].tag.address == 0
    assert result[0].tag.datatype == DataTypes.INT32
    assert result[0].value == 4
