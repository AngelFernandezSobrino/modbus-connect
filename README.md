# Modbus Connect package for Python

<a href="https://angelfernandezsobrino.github.io/modbus-connect/reports/tests/3.11.html" alt="Tests">
    <img src="https://angelfernandezsobrino.github.io/modbus-connect/badges/tests/3.11.svg">
</a>
<a href="https://angelfernandezsobrino.github.io/modbus-connect/reports/coverage/3.11/index.html" alt="Tests">
    <img src="https://angelfernandezsobrino.github.io/modbus-connect/badges/coverage/3.11.svg">
</a>


Modbus Connect is a Python package that provides a configurable Modbus TCP data adquisition library from Modbus TCP devices. It is designed to be used as a library for a data acquisition application, managing the connection to the devices and the data exchange with them. The data is returned in a format that can be easily used for sending to a database or MQTT broker.

The Modbus data table can be supplied as a csv file or as a Python dictionary. A dictionary is used to configure the Modbus Gateway. The dictionary can be created manually or by using the importer module from a csv file.

It is based on the [PyModbus](https://github.com/riptideio/pymodbus) for the Modbus TCP communication.

The [modbus-mqtt-digital-twin]() package provides a data acquisition application that uses the Modbus Gateway library. (Under development)


## Installation

The package can be installed from PyPI:

```bash
pip install modbus
```

## Usage

For a complete example of the usage of the package, check the examples folder.

Here is a simple example of the usage of the package:

```python
from modbus_gateway import ModbusGateway

# Create a dictionary with the configuration of the Modbus Gateway

config = [
    {
        "name": "var1",
        "address": 0,
        "memory_bank": utils.MemoryBanks.HOLDING_REGISTERS,
        "datatype": "float32",
    },
    {
        "name": "var2",
        "address": 2,
        "memory_bank": utils.MemoryBanks.HOLDING_REGISTERS,
        "datatype": "float32",
    },
]

gateway = ModbusGateway(
    host=<host>,
    port=<port>,
    tags_list=config,
)

# Read the values from the modbus server

values = gateway.read_tags()
print(values)
```

This behaviour can be easly used for continuous data adquisition using rocktry or any other scheduler and fastly deploied using docker.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Authors

-   **Ángel Fernández Sobrino** - [AngelFernandezSobrino](https://github.com/AngelFernandezSobrino)