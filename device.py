from pymodbus.client.serial import ModbusSerialClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian


def read_inverter_data(con, address, count, slave):
    # данная функция читает данные с инв
    result = con.read_input_registers(address=address, count=count, unit=1, slave=slave)
    print(result)
    if not result.isError():
        return result.registers
    else:
        print(f"Failed to read registers from address {address}")
        return None


def decode_registers(registers):
    print(registers)
    # данная функция расшифровывает данные с инв
    res = BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.BIG)
    print(res)
    return res


# Configure the Modbus client
client = ModbusClient(
    method='rtu',
    port='/dev/tty.usbserial-210',  # Adjust this to your USB port
    baudrate=9600,
    parity='N',
    stopbits=1,
    bytesize=8,
    timeout=1
)

# Connect to the Modbus server (Growatt inverter)
connection = client.connect()
if connection:
    print("Connected to Growatt inverter")

    try:
        registers = read_inverter_data(client, 91, 4, 1)
        current = read_inverter_data(client, 53, 2, 1)

        if registers:
            decoder = decode_registers(registers)
            decode = decode_registers(current)
            # Example: Decode some typical inverter data
            # Adjust decoding according to your specific register map
            total_energy = decoder.decode_32bit_uint()  # Assuming total energy is a 32-bit unsigned integer
            temp1 = decoder.decode_16bit_uint()  # Assuming daily energy is a 16-bit unsigned integer
            temp2 = decoder.decode_16bit_uint()  # Assuming current power is a 16-bit unsigned integer
            current = decode.decode_32bit_uint()  # Assuming current power is a 16-bit unsigned integer

            print(f"Total Energy: {total_energy / 10} kWh")
            print(f"Temperature: {temp1 / 10} kWh")
            print(f"Temp2: {temp2 / 10} W")
            print(f"Current: {current / 10}  Wh")

    finally:
        # Close the client connection
        client.close()
else:
    print("Failed to connect to Growatt inverter")
