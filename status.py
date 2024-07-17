from pymodbus.client.serial import ModbusSerialClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from decimal import Decimal
import time
from typing import NamedTuple, Dict


class Connect(NamedTuple):
    method: str
    port: str
    baudrate: int
    parity: str
    stopbits: int
    bytesize: int
    timeout: int


class ModBusDataRead(NamedTuple):
    slave: int
    function: int
    address: int
    count: int
    coefficient: str
    unit: str


def decode_registers_to_ascii(registers):
    decoder = BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.BIG)
    decoded_string = ''
    for _ in range(len(registers)):
        word = decoder.decode_16bit_uint()
        high_byte = (word >> 8) & 0xFF
        low_byte = word & 0xFF
        decoded_string += chr(high_byte) + chr(low_byte)
    return decoded_string.strip()


def read_serial_number(connect):
    connect = ModbusClient(**connect)
    try:
        start_address = 23
        count = 5
        serial_registers = connect.read_holding_registers(address=start_address, count=count, unit=1, slave=2)
        if not serial_registers.isError():
            serial_number = decode_registers_to_ascii(serial_registers.registers)
            connect.close()
            return {'serial_number': serial_number}
        else:
            return 'Не удалось прочитать серийный номер'
    except Exception as e:
        return e


class Device:
    def __init__(self, connect: dict, sn, read_dict: Dict[str, ModBusDataRead]):
        self.connect = ModbusClient(**connect)
        self.registers_dict = read_dict
        self.decoders = BinaryPayloadDecoder.fromRegisters
        self.sn = sn

    def decode_registers(self, registers, count):
        res = self.decoders(registers, byteorder=Endian.BIG, wordorder=Endian.BIG)
        decode_bit = {1: res.decode_16bit_uint, 2: res.decode_32bit_uint, 4: res.decode_64bit_uint}
        return decode_bit[count]

    def registers_functions(self, func: int):
        res = {3: self.connect.read_holding_registers, 4: self.connect.read_input_registers}
        return res[func]

    def read_registers(self, name: str):
        try:
            register = self.registers_dict.get(name, False)
            if register is False:
                return 'Данный метод (name), отсутствует!'
            register_function = self.registers_functions(register.function)
            data = register_function(address=register.address, count=register.count, slave=register.slave)
            decode = self.decode_registers(data.registers, register.count)
            return {'data': str(decode() * Decimal(register.coefficient)), 'unit': register.unit}
        except Exception as e:
            return str(e)

    def read_all_registers(self):
        result = {name: self.read_registers(name) for name in self.registers_dict.keys()}
        return result, sn

    def send_one_register_data(self, name, server_ip):
        pass

    def send_all_register_data(self, server_ip):
        pass


connect_example = {'method': 'rtu', 'port': '/dev/tty.usbserial-10',
                   'baudrate': 9600, 'parity': 'N', 'stopbits': 1,
                   'bytesize': 8, 'timeout': 1}
sn = read_serial_number(connect_example)
reg = {
    "e-today": ModBusDataRead(**{
        "slave": 2,
        "function": 4,
        "address": 53,
        "count": 2,
        "coefficient": "0.1",
        "unit": "kWH"
    }),
    "e-total": ModBusDataRead(**{
        "slave": 2,
        "function": 4,
        "address": 55,
        "count": 2,
        "coefficient": "0.1",
        "unit": "kWH"
    }),
    "h-total": ModBusDataRead(**{
        "slave": 2,
        "function": 4,
        "address": 57,
        "count": 2,
        "coefficient": "0.5",
        "unit": "s"
    })
}

growwat = Device(connect=connect_example, read_dict=reg, sn=sn)

while True:
    print(growwat.read_all_registers())
    time.sleep(0.1)
