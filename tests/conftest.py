from typing import List
import pytest

from modbus_connect.tags import Tag, MemoryTypes, DataTypes

import tests.mock_modbus


@pytest.fixture
def mock_modbus_server() -> int:
    port = tests.mock_modbus.get_free_port()
    thread = tests.mock_modbus.run_mock_thread(port)
    return port


@pytest.fixture
def tags_list() -> List[Tag]:
    return [
        Tag("var1", 0, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var2", 2, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var3", 4, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var4", 6, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var5", 8, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var6", 10, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var7", 12, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var8", 14, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var9", 16, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var10", 18, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var11", 20, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var12", 22, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var13", 24, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var14", 26, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var15", 28, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var16", 30, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var17", 32, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var18", 34, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var19", 36, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var20", 38, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var21", 40, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var22", 42, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
        Tag("var23", 44, MemoryTypes.HOLDING_REGISTERS, DataTypes.FLOAT32),
    ]


@pytest.fixture
def tags_list_mock() -> List[Tag]:
    return [
        Tag("var1", 0, MemoryTypes.HOLDING_REGISTERS, DataTypes.INT32),
        Tag("var2", 2, MemoryTypes.HOLDING_REGISTERS, DataTypes.INT32),
    ]
