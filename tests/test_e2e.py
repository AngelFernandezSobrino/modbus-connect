import logging

from modbus_connect import client
import modbus_connect.connect as connect
from modbus_connect.tags import Tag, MemoryTypes, DataTypes


def test_integration_external():
    # Arrange

    connector = connect.ModbusConnector(
        client.ModbusConfig("docencia.i4techlab.upc.edu", 20000, 1, 1),
        tags_dict=[
            Tag("var1", 0, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
            Tag("var2", 2, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        ],
    )

    connector.connect()

    # Act

    results = connector.read_tags()

    # Assert

    assert len(results) == 2
    assert results[0].tag.name == "var1"
    assert results[0].tag.address == 0
    assert results[0].tag.datatype == DataTypes.FLOAT32
    assert results[0].value != 0
    assert results[0].value > -10 and results[0].value < 10
