# Test gateway core methods

# Import gateway module

import modbus_connect.tags as tags


# Test memory types enum order


def test_memory_types_enum_order():
    assert tags.MemoryTypes.COILS < tags.MemoryTypes.DISCRETE_INPUTS
    assert (
        tags.MemoryTypes.DISCRETE_INPUTS < tags.MemoryTypes.HOLDING_REGISTERS
    )
    assert (
        tags.MemoryTypes.HOLDING_REGISTERS < tags.MemoryTypes.INPUT_REGISTERS
    )


# Test data types enum data length


def test_data_types_enum_data_length():
    assert tags.DataTypes.BOOL.length == 1
    assert tags.DataTypes.INT16.length == 1
    assert tags.DataTypes.UINT16.length == 1
    assert tags.DataTypes.INT32.length == 2
    assert tags.DataTypes.UINT32.length == 2
    assert tags.DataTypes.FLOAT32.length == 2
    assert tags.DataTypes.INT64.length == 4


# Test tag class returns correct length


def test_tag_class_returns_correct_length():
    tag = tags.Tag(
        "test_tag", 0, tags.MemoryTypes.HOLDING_REGISTERS, tags.DataTypes.INT32
    )

    assert tag.length == 2


# Test tag class creates correct batches


def test_tag_class_batches():
    # Arrange
    tags_list = [
        tags.Tag(
            "test_tag1",
            0,
            tags.MemoryTypes.HOLDING_REGISTERS,
            tags.DataTypes.INT32,
        ),
        tags.Tag(
            "test_tag2",
            2,
            tags.MemoryTypes.HOLDING_REGISTERS,
            tags.DataTypes.INT32,
        ),
        tags.Tag(
            "test_tag3",
            4,
            tags.MemoryTypes.HOLDING_REGISTERS,
            tags.DataTypes.INT16,
        ),
        tags.Tag(
            "test_tag4",
            5,
            tags.MemoryTypes.HOLDING_REGISTERS,
            tags.DataTypes.INT32,
        ),
        tags.Tag(
            "test_tag5",
            7,
            tags.MemoryTypes.HOLDING_REGISTERS,
            tags.DataTypes.INT32,
        ),
        tags.Tag(
            "test_tag6",
            9,
            tags.MemoryTypes.HOLDING_REGISTERS,
            tags.DataTypes.INT16,
        ),
        tags.Tag(
            "test_tag7",
            10,
            tags.MemoryTypes.HOLDING_REGISTERS,
            tags.DataTypes.INT16,
        ),
        tags.Tag(
            "test_tag8",
            11,
            tags.MemoryTypes.HOLDING_REGISTERS,
            tags.DataTypes.INT32,
        ),
        tags.Tag(
            "test_tag9",
            100,
            tags.MemoryTypes.HOLDING_REGISTERS,
            tags.DataTypes.INT32,
        ),
        tags.Tag(
            "test_tag10",
            102,
            tags.MemoryTypes.HOLDING_REGISTERS,
            tags.DataTypes.INT32,
        ),
        tags.Tag(
            "test_tag11",
            104,
            tags.MemoryTypes.HOLDING_REGISTERS,
            tags.DataTypes.INT32,
        ),
        tags.Tag(
            "test_tag12",
            106,
            tags.MemoryTypes.HOLDING_REGISTERS,
            tags.DataTypes.INT32,
        ),
    ]

    # Act
    tags_object = tags.Tags(tags_list, 5)

    # Assert
    assert len(tags_object.batches) == 3
    assert len(tags_object.batches[0]) == 5
    assert isinstance(tags_object.batches[0], tags.Batch)


# Test Batch class returns correct modbus address length for batch


def test_batch_class_returns_correct_modbus_address_length_for_batch():
    # Arrange
    tags_list = [
        tags.Tag(
            "test_tag1",
            0,
            tags.MemoryTypes.HOLDING_REGISTERS,
            tags.DataTypes.INT32,
        ),
        tags.Tag(
            "test_tag2",
            2,
            tags.MemoryTypes.HOLDING_REGISTERS,
            tags.DataTypes.INT32,
        ),
        tags.Tag(
            "test_tag3",
            4,
            tags.MemoryTypes.HOLDING_REGISTERS,
            tags.DataTypes.INT16,
        ),
        tags.Tag(
            "test_tag4",
            5,
            tags.MemoryTypes.HOLDING_REGISTERS,
            tags.DataTypes.INT32,
        ),
    ]

    batch = tags.Batch(tags_list)

    # Act
    result = batch.memory_length

    # Assert
    assert result == 7
