import datetime
from enum import Enum
from typing import Dict

from pydantic import BaseModel, field_validator


Name_Inverter = str
Serial_Number = str
Registers_Name = str


class FunctionEnum(int, Enum):
    read_holding_registers = 3
    read_input_registers = 4


class CountEnum(int, Enum):
    bit16 = 1
    bit32 = 2
    bit64 = 4


class Connect(BaseModel):
    method: str
    port: str
    baudrate: int
    parity: str
    stopbits: int
    bytesize: int
    timeout: int

    @field_validator('baudrate')
    @classmethod
    def validate_baudrate(cls, values: int) -> int:
        if values not in [1200, 2400, 4800, 9600, 19200, 38400]:
            raise ValueError('Скорость может быть только: 1200, 2400, 4800, 9600, 19200, 38400')
        return values


class InverterDateInput(BaseModel):
    function: FunctionEnum
    address: int
    count: CountEnum
    coefficient: str
    unit: str | None


class Inverter(BaseModel):
    name: Name_Inverter
    serial_number: Serial_Number
    connect: Connect
    slave: int
    create_date: datetime.datetime = datetime.datetime.now()
    registers: Dict[Registers_Name, InverterDateInput]


class InverterDate(BaseModel):
    date: str
    unit: str | None


class InverterDataOutput(BaseModel):
    serial_number: Serial_Number
    create_date: datetime.datetime = datetime.datetime.now()
    inverter_registers_date: Dict[Registers_Name, InverterDate]
