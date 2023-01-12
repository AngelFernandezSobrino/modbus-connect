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
pip install modbus-connect
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

### Framework

This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging. To install the dependencies, run:

```bash
poetry install
```
Add `-without dev` to the command to install only build and production dependencies.

To format the code usign black, use:

```bash
poetry run black ./modbus_connect/* ./tests/*
```

To run the tests, use:

```bash
poetry run pytest tests/
```

To get the reports of the tests, that would be shown on release, use:

```bash
poetry run pytest --junitxml=reports/tests/${{ matrix.python-version }}.xml --html=reports/tests/${{ matrix.python-version }}.html --cov-report xml:reports/coverage/${{ matrix.python-version }}.xml --cov-report html:reports/coverage/${{ matrix.python-version }} --cov=modbus_connect tests/
```

Reports are generated in the reports folder.

Pre-commit hooks are used to ensure that the code is properly formated and tested before commiting. To install the pre-commit hooks, run:

```bash
poetry run pre-commit install
```
To avoid commits without formating or failing tests. To void 

Coverage and reports can also be triggered, check [lint-test action](./.github/workflows/lint-test.yml) for more details about the commands to use.




## Authors

-   **Ángel Fernández Sobrino** - [AngelFernandezSobrino](https://github.com/AngelFernandezSobrino)