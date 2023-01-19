from typing import List, NewType
from dataclasses import dataclass
from enum import Enum


class MemoryTypes(Enum):
    HOLDING_REGISTERS = "holding_registers"
    INPUT_REGISTERS = "input_registers"
    DISCRETE_INPUTS = "discrete_inputs"
    COILS = "coils"

    __lt__ = lambda self, other: self.value < other.value
    __eq__ = lambda self, other: self.value == other.value
    __gt__ = lambda self, other: self.value > other.value


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

    @property
    def length(self) -> int:
        if self == DataTypes.BOOL:
            return 1
        elif self == DataTypes.INT16:
            return 1
        elif self == DataTypes.UINT16:
            return 1
        elif self == DataTypes.INT32:
            return 2
        elif self == DataTypes.UINT32:
            return 2
        elif self == DataTypes.FLOAT32:
            return 2
        elif self == DataTypes.INT64:
            return 4
        elif self == DataTypes.UINT64:
            return 4
        elif self == DataTypes.FLOAT64:
            return 4
        else:
            raise ValueError("Datatype not supported")


@dataclass
class Tag:
    name: str
    address: int
    memorytype: MemoryTypes
    datatype: DataTypes

    # Create a lenght property to be able to know the lenght of the register by its datatype
    @property
    def length(self) -> int:
        return self.datatype.length


@dataclass
class Result:
    tag: Tag
    value: any = None


Results = NewType("Results", List[Result])


class Tags:
    def __init__(self, tags: List[Tag], batch_size):
        self.tags = tags
        self.batch_size = batch_size

        # Tags are stored sorted by address and memory bank
        self.tags.sort(key=lambda x: x.address)
        self.tags.sort(key=lambda x: x.memorytype)

        self.batches: List[Batch] = []
        self.create_batches()

    # Batches must be consecutive in memory and have the same memory bank
    # TODO: Allow the creation of batches which are not consecutive by an allowed non taged memory space

    def ready(self) -> bool:
        return len(self.batches) > 0

    def create_batches(self):
        # Check context for bad configurations
        if self.batch_size < 2:
            raise ValueError(
                "Is not possible to make batches with a size less than 2"
            )

        # Create batches
        self.batches.append(Batch((self.tags[0],)))
        for i in range(1, len(self.tags)):
            if (
                self.tags[i].address
                != self.tags[i - 1].address + self.tags[i - 1].length
                or self.tags[i].memorytype != self.tags[i - 1].memorytype
                or len(self.batches[-1]) >= self.batch_size
            ):
                self.batches.append(Batch((self.tags[i],)))

            else:
                self.batches[-1].append(self.tags[i])


class Batch(List[Tag]):
    # Get the length of the batch in modbus memory space
    @property
    def memory_length(self) -> int:
        return sum([tag.length for tag in self])
