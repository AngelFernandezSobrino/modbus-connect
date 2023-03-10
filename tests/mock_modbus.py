import logging
import asyncio
import time

from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusSlaveContext,
)
from pymodbus.device import ModbusDeviceIdentification
import pymodbus.server.async_io
from pymodbus.version import version


_logger = logging.getLogger()


def setup_server(port):
    datablock = ModbusSequentialDataBlock.create()
    datablock.setValues(0, [0, 4, 0, 8])
    context = ModbusSlaveContext(
        di=datablock, co=datablock, hr=datablock, ir=datablock, unit=1
    )
    single = True

    setup = {
        "port": port,
        "comm": "tcp",
        "framer": "socket",
        "context": ModbusServerContext(slaves=context, single=single),
        "identity": ModbusDeviceIdentification(
            info_name={
                "VendorName": "Pymodbus",
                "ProductCode": "PM",
                "VendorUrl": "https://github.com/riptideio/pymodbus/",
                "ProductName": "Pymodbus Server",
                "ModelName": "Pymodbus Server",
                "MajorMinorRevision": version.short(),
            }
        ),
    }
    return setup


def run_async_server(setup):
    address = ("", setup["port"]) if setup["port"] else None
    server = pymodbus.server.async_io.ModbusTcpServer(
        context=setup["context"],  # Data storage
        identity=setup["identity"],  # server identify
        # TBD host=
        # TBD port=
        address=address,  # listen address
        # custom_functions=[],  # allow custom handling
        # framer=setup['framer'],  # The framer strategy to use
        # handler=None,  # handler for each session
        # allow_reuse_address=True,  # allow the reuse of an address
        # ignore_missing_slaves=True,  # ignore request to a missing slave
        # broadcast_enable=False,  # treat unit_id 0 as broadcast address,
        # timeout=1,  # waiting time for request to complete
        # TBD strict=True,  # use strict timing, t1.5 for Modbus RTU
        # defer_start=False,  # Only define server do not activate
    )

    return server


def start_mock_server(port):
    asyncio.set_event_loop(asyncio.new_event_loop())
    setup = setup_server(port)
    server = run_async_server(setup)

    loop = server.loop
    loop.set_debug(True)
    loop.set_exception_handler(lambda loop, context: _logger.error(context))
    loop.create_task(server.serve_forever())
    loop.run_forever()


def run_mock_thread(port):
    import threading
    import time

    thread = threading.Thread(target=start_mock_server, args=(port,))
    thread.daemon = True
    thread.start()
    return thread


def get_free_port():
    import socket

    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port
