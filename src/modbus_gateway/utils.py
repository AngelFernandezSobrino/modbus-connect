import typing
from typing import List, NewType

from dataclasses import dataclass, field
from typing import List, TypedDict
from enum import Enum

# --------------------- TYPES ---------------------


class MemoryBanks(Enum):
    HOLDING_REGISTERS = "holding_registers"
    INPUT_REGISTERS = "input_registers"
    DISCRETE_INPUTS = "discrete_inputs"
    COILS = "coils"

class DataTypes(Enum):
    BOOL = "bool"
    INT16 = "int16"
    UINT16 = "uint16"
    INT32 = "int32"
    UINT32 = "uint32"
    FLOAT32 = "float32"
    INT64 = "int64"
    UINT64 = "uint64"
    FLOAT64 = "float64"

@dataclass
class ModbusRegister:
    name: str
    address: int
    memorybank: MemoryBanks
    datatype: str

    # Create a lenght property to be able to know the lenght of the register by its datatype
    @property
    def length(self) -> int:
        if self.datatype == "bool":
            return 1
        elif self.datatype == "int16":
            return 1
        elif self.datatype == "uint16":
            return 1
        elif self.datatype == "int32":
            return 2
        elif self.datatype == "uint32":
            return 2
        elif self.datatype == "float32":
            return 2
        elif self.datatype == "int64":
            return 4
        elif self.datatype == "uint64":
            return 4
        elif self.datatype == "float64":
            return 4
        else:
            raise ValueError("Datatype not supported")


ModbusRegisters = NewType("ModbusRegisters", List[ModbusRegister])

ModbusRegistersBatched = NewType("ModbusRegistersBatched", List[List[ModbusRegister]])


@dataclass
class ModbusRegistersGroups:
    holding_registers: ModbusRegisters = field(default_factory=list)
    input_registers: ModbusRegisters = field(default_factory=list)
    discrete_inputs: ModbusRegisters = field(default_factory=list)
    coils: ModbusRegisters = field(default_factory=list)

ModbusRegistersGroupsV2 = NewType("ModbusRegistersGroupsV2", dict[MemoryBanks, ModbusRegistersGroups])

@dataclass
class ModbusRegistersGroupsBatched:
    holding_registers: ModbusRegistersBatched = field(default_factory=list)
    input_registers: ModbusRegistersBatched = field(default_factory=list)
    discrete_inputs: ModbusRegistersBatched = field(default_factory=list)
    coils: ModbusRegistersBatched = field(default_factory=list)


@dataclass
class ModbusResult:
    register: ModbusRegister
    value: any = None


ModbusResults = NewType("ModbusResults", List[ModbusResult])


@dataclass
class ModbusResultsGrups:
    holding_registers: ModbusResults = field(default_factory=list)
    input_registers: ModbusResults = field(default_factory=list)
    discrete_inputs: ModbusResults = field(default_factory=list)
    coils: ModbusResults = field(default_factory=list)


# --------------------- FUNCTIONS ---------------------


# From a list of {'name': 'variable_name', 'address': number} classes, return a list which contains lists of dictionaries which contain the dictionaries
# from the original list which have consecutive address numbers, with a maximum size of size.


@dataclass
class ObjectWithAddress():
    address: int
    length: int


def make_batch_consecutive_sized(
    list: List[ObjectWithAddress],
    size: int,
) -> List[List]:
    # Check if size is greater than 2 to be able to make batches
    if size < 2:
        raise ValueError("Size must be greater than 2")
    parts: List[List] = []

    if len(list) == 0:
        return []

    # Create a for loop that will iterate over modbus_addresss_list, looking for consecutive addresss and adding them to parts list, without considering the first element
    parts.append([list[0]])
    for i in range(1, len(list)):
        if list[i].address == list[i - 1].address + list[i - 1].length:
            # If batch_counter is equal to size plus one, the batch is full, so we create a new list
            if len(parts[-1]) < size:
                parts[-1].append(list[i])
            else:
                parts.append([list[i]])

        else:
            parts.append([list[i]])

    return parts
