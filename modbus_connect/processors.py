from typing import List, Protocol

import pymodbus.payload
import pymodbus.register_read_message
import pymodbus.bit_read_message
import pymodbus.constants

import modbus_connect.tags as tags
from modbus_connect.tags import MemoryTypes, DataTypes


class RegisterResponse(Protocol):
    def getBit(self, address: int) -> bool:
        ...

    @property
    def registers(self) -> list[int]:
        ...


def process_batch(
    batch: tags.Batch,
    batch_results: RegisterResponse,
    byte_order: pymodbus.constants.Endian,
    word_order: pymodbus.constants.Endian,
) -> tags.Results:
    values: tags.Results = []

    # Check the memory bank of the first register in the batch to determine the processing function between word like or bit like, for each register in the batch, process the register and append the result to the list of results
    if batch[0].memorytype == tags.MemoryTypes.HOLDING_REGISTERS:
        process_registers_batch(
            batch, batch_results, byte_order, word_order, values
        )
    elif (
        batch[0].memorytype == tags.MemoryTypes.COILS
        or batch[0].memorytype == tags.MemoryTypes.DISCRETE_INPUTS
    ):
        process_bits_batch(batch, batch_results, values)

    return values


def process_bits_batch(
    batch: tags.Batch, batch_results: RegisterResponse, values: tags.Results
):
    for tag in batch:
        if (
            tag.memorytype == tags.MemoryTypes.COILS
            or tag.memorytype == tags.MemoryTypes.DISCRETE_INPUTS
        ):
            values.append(
                process_bitlike_register(
                    tag,
                    batch_results.getBit(tag.address - batch[0].address),
                )
            )


def process_registers_batch(
    batch: tags.Batch,
    batch_results: RegisterResponse,
    byte_order,
    word_order,
    values: tags.Results,
):
    for tag in batch:
        if (
            tag.memorytype == tags.MemoryTypes.HOLDING_REGISTERS
            or tag.memorytype == tags.MemoryTypes.INPUT_REGISTERS
        ):
            values.append(
                tags.Result(
                    tag,
                    process_wordlike_register(
                        tag,
                        batch_results.registers[
                            tag.address
                            - batch[0].address : (
                                tag.address - batch[0].address
                            )
                            + tag.length
                        ],
                        byte_order,
                        word_order,
                    ),
                )
            )


def process_wordlike_register(
    tag: tags.Tag,
    registers_list: list[int],
    byte_order: pymodbus.constants.Endian,
    word_order: pymodbus.constants.Endian,
) -> any:
    if tag.datatype == DataTypes.INT16:
        return registers_list[0]

    elif tag.datatype == DataTypes.INT32:
        return pymodbus.payload.BinaryPayloadDecoder.fromRegisters(
            registers_list,
            byte_order,
            wordorder=word_order,
        ).decode_32bit_int()

    elif tag.datatype == DataTypes.FLOAT32:
        return pymodbus.payload.BinaryPayloadDecoder.fromRegisters(
            registers_list,
            byte_order,
            wordorder=word_order,
        ).decode_32bit_float()

    else:
        raise ValueError("Invalid datatype: " + tag.datatype)


def process_bitlike_register(
    tag: tags.Tag,
    register: any,
):
    value = None

    if tag.datatype == DataTypes.BOOL:
        value = tags.Result(tag, bool(register))

    else:
        raise ValueError("Invalid datatype: " + tag["datatype"])

    return value
