import requests
import time
from modbus_app import Device, ModBusDataRead, read_serial_number
from pymodbus.client.serial import ModbusSerialClient as ModbusClient
from ip import get_local_ip

# ip = '127.0.0.1:8080'
ip = get_local_ip() + ':8080'

# Получение токена
url = f"http://{ip}/inverter"
response = requests.get(url)
date = response.json()
inv_list = list()

connect = ModbusClient(**date[0]['connect'])
for inv in date:
    serial_number = read_serial_number(connect, inv['slave'])
    date_reg = {k: ModBusDataRead(**v) for k, v in inv['registers'].items()}
    inv_list.append(Device(connect=connect,serial_number=serial_number, slave=inv['slave'], read_dict=date_reg))


url_date_send = f"http://{ip}/date"

while True:
    for i in inv_list:
        print(i.send_all_register_data(url_date_send))

    time.sleep(3)
