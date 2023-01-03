from typing import List

import pymodbus.payload
import pymodbus.register_read_message
import pymodbus.constants

import src.modbus_gateway.utils as utils


def process_holding_registers(
    batches: utils.ModbusRegistersBatched,
    batches_results: List[pymodbus.register_read_message.ReadHoldingRegistersResponse],
    byte_order,
    word_order,
) -> utils.ModbusResults:
    values: utils.ModbusResults = []
    for batch_index, batch in enumerate(batches):
        register_counter = batches[0]["address"]
        for tag in batches:
            # Process the result depending on the datatype, increase the register counter depending on the datatype as well

            values.append(process_holding_register(tag, batches_results[batch_index].registers[register_counter] , byte_order, word_order))

            if tag["datatype"] == "int16":
                values.append(
                    utils.ModbusResult(
                        tag, batches_results[batch_index].registers[register_counter]
                    )
                )
                register_counter += 1
            elif tag["datatype"] == "int32":
                values.append(
                    utils.ModbusResult(
                        tag,
                        pymodbus.payload.BinaryPayloadDecoder.fromRegisters(
                            batches_results[batch_index].registers[
                                register_counter : register_counter + 2
                            ],
                            byte_order,
                            wordorder=word_order,
                        ).decode_32bit_int(),
                    )
                )

                register_counter += 2
            elif tag["datatype"] == "float32":
                values.append(
                    utils.ModbusResult(
                        tag,
                        pymodbus.payload.BinaryPayloadDecoder.fromRegisters(
                            batches_results[batch_index].registers[
                                register_counter : register_counter + 2
                            ],
                            byte_order,
                            wordorder=word_order,
                        ).decode_32bit_float(),
                    )
                )
                register_counter += 2
            else:
                raise ValueError("Invalid datatype: " + tag["datatype"])


def process_holding_register(
    tag: utils.ModbusRegister,
    registers_list: list[int],
    byte_order: pymodbus.constants.Endian,
    word_order: pymodbus.constants.Endian,
):
    value = None

    if tag["datatype"] == "int16":
        value = utils.ModbusResult(tag, registers_list[0])

    elif tag["datatype"] == "int32":
        value = utils.ModbusResult(
            tag,
            pymodbus.payload.BinaryPayloadDecoder.fromRegisters(
                registers_list,
                byte_order,
                wordorder=word_order,
            ).decode_32bit_int(),
        )

    elif tag["datatype"] == "float32":
        values = utils.ModbusResult(
            tag,
            pymodbus.payload.BinaryPayloadDecoder.fromRegisters(
                registers_list,
                byte_order,
                wordorder=word_order,
            ).decode_32bit_float(),
        )

    else:
        raise ValueError("Invalid datatype: " + tag["datatype"])

    return value
