import pymodbus.register_read_message

import src.modbus_gateway.processors as processors
import src.modbus_gateway.utils as utils

# Test that process_holding_registers returns the correct values for a batch of 2 variables
# 
# The batch is composed of 2 variables, one of type int16 and the other of type int32
# 
# The batch results are composed of 2 registers, one of value 1 and the other of value 2
# 
# The byte order is big endian and the word order is big endian
# 
# The expected result is a list of 2 ModbusResult objects, one with the name of the int16 variable, the address of the int16 variable, the datatype of the int16 variable and the value of the int16 variable, and the other with the name of the int32 variable, the address of the int32 variable, the datatype of the int32 variable and the value of the int32 variable
# 
# The test passes if the result is equal to the expected result
# 
# The test fails if the result is not equal to the expected result
# 
# The test fails if an exception is raised

def test_process_holding_registers():

    batches: utils.ModbusRegistersBatched = [
        [
            {
                "name": "var1",
                "address": 0,
                "memory_bank": utils.MemoryBank.HOLDING,
                "datatype": "int16",
            },
            {
                "name": "var2",
                "address": 1,
                "datatype": "int32",
            }
        ]
    ]

    batches_results = pymodbus.register_read_message.ReadHoldingRegistersResponse(values=[1, 0, 2])

    # 

