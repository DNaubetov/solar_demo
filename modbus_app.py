import datetime

from pymodbus.client.serial import ModbusSerialClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from decimal import Decimal
import time
import requests

from typing import NamedTuple, Dict

"""    
        self.model = model
        self.serial_number = serial_number
        self.status = status
        self.current_power = current_power
        self.e_today = e_today
        self.e_total = e_total
        self.h_total = h_total
        self.temperature = temperature
"""


class Connect(NamedTuple):
    method: str
    port: str
    baudrate: int
    parity: str
    stopbits: int
    bytesize: int
    timeout: int


class ModBusDataRead(NamedTuple):
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


def read_serial_number(connect, slave):
    try:
        start_address = 23
        count = 5
        serial_registers = connect.read_holding_registers(address=start_address, count=count, unit=1, slave=slave)
        if not serial_registers.isError():
            serial_number = decode_registers_to_ascii(serial_registers.registers)
            connect.close()
            return {'serial_number': serial_number}
        else:
            return 'Не удалось прочитать серийный номер'
    except Exception as e:
        return e


class Device:
    def __init__(self, connect: ModbusClient, slave, serial_number, read_dict: Dict[str, ModBusDataRead]):
        self.connect = connect
        self.registers_dict = read_dict
        self.slave = slave
        self.serial_number = serial_number
        self.decoders = BinaryPayloadDecoder.fromRegisters

    def __decode_registers(self, registers, count):
        # данная функция расшифровывает данные с инв
        res = self.decoders(registers, byteorder=Endian.BIG, wordorder=Endian.BIG)
        decode_bit = {1: res.decode_16bit_uint, 2: res.decode_32bit_uint, 4: res.decode_64bit_uint}
        return decode_bit[count]

    def __registers_functions(self, func: int):
        """
        Функция принимает число (номер функции modbus) и возвращает функцию modbus
        """
        res = {3: self.connect.read_holding_registers, 4: self.connect.read_input_registers}
        return res[func]

    def read_registers(self, name: str):
        """
        Функция читает регистры и переводит их в 10 данные
        Пример: Нужно прочитать e-total, отправляем название (e-total) и получаем данные 30 и тп
        """
        try:
            register = self.registers_dict.get(name, False)  # выбираем что нужно прочитать по названию.
            if register is False:
                return 'Данный метод (name), отсутствует!'
            register_function = self.__registers_functions(register.function)  # выбираем функцию чтения (3 или 4).
            data = register_function(address=register.address, count=register.count,
                                     slave=self.slave)  # читаем данные
            decode = self.__decode_registers(data.registers, register.count)  # переводим данные с 16 на 10
            return {'date': str(decode() * Decimal(register.coefficient)), 'unit': register.unit}
        except Exception as e:
            return e

    def read_all_registers(self):
        """ Функция читает все регистры класса и возвращает словарь"""
        return {name: self.read_registers(name) for name in self.registers_dict.keys()}

    def send_one_register_data(self, name, server_ip):
        """ Функция отправляет на сервер один из параметров"""
        pass

    def send_all_register_data(self, server_ip):
        """ Функция отправляет на сервер все данные регистров"""
        date = {'serial_number': self.serial_number['serial_number'],
                "create_date": datetime.datetime.now().isoformat(),
                "inverter_registers_date": self.read_all_registers()
                }
        secure_response = requests.post(server_ip, json=date)
        print(date)
        return secure_response, secure_response.json()
        # return date

# # reg = {
# #     "e-today": ModBusDataRead(**{
# #         "slave": 2,
# #         "function": 4,
# #         "address": 53,
# #         "count": 2,
# #         "coefficient": "0.1",
# #         "unit": "kWH"
# #     }),
# #     "e-total": ModBusDataRead(**{
# #         "slave": 2,
# #         "function": 4,
# #         "address": 55,
# #         "count": 2,
# #         "coefficient": "0.1",
# #         "unit": "kWH"
# #     }),
# #     "h-total": ModBusDataRead(**{
# #         "slave": 2,
# #         "function": 4,
# #         "address": 57,
# #         "count": 2,
# #         "coefficient": "0.5",
# #         "unit": "s"
# #     })
# # }
#
#
# connect_example = {'method': 'rtu', 'port': '/dev/tty.usbserial-210',
#                    'baudrate': 9600, 'parity': 'N', 'stopbits': 1,
#                    'bytesize': 8, 'timeout': 1}
#
# if __name__ == '__main__':
#     growatt = Device(connect=connect_example, read_dict=reg)
#     while True:
#         print(growatt.read_all_registers())
#         time.sleep(5)
