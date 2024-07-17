date_inv = [{
    "name": "Growatt Sozlash",
    "serial_number": "either-12315-673-as",
    "slave": 1,
    "connect": {
        "method": "rtu",
        "port": "/dev/tty.usbserial-10",
        "baudrate": 9600,
        "parity": "N",
        "stopbits": 1,
        "bytesize": 8,
        "timeout": 1
    },
    "registers": {
        "e-today": {
            "function": 4,
            "address": 53,
            "count": 2,
            "coefficient": "0.1",
            "unit": "kWH"
        },
        "e-total": {
            "function": 4,
            "address": 55,
            "count": 2,
            "coefficient": "0.1",
            "unit": "kWH"
        },
        "H-total": {
            "function": 4,
            "address": 57,
            "count": 2,
            "coefficient": "0.5",
            "unit": "s"
        },
        "Current-power": {
            "function": 4,
            "address": 1,
            "count": 2,
            "coefficient": "0.1",
            "unit": "W"
        }
    }
}, {
    "name": "Growatt Tpp",
    "serial_number": "either-12315-673-as",
    "slave": 2,
    "connect": {
        "method": "rtu",
        "port": "/dev/tty.usbserial-10",
        "baudrate": 9600,
        "parity": "N",
        "stopbits": 1,
        "bytesize": 8,
        "timeout": 1
    },
    "registers": {
        "e-today": {
            "function": 4,
            "address": 53,
            "count": 2,
            "coefficient": "0.1",
            "unit": "kWH"
        },
        "e-total": {
            "function": 4,
            "address": 55,
            "count": 2,
            "coefficient": "0.1",
            "unit": "kWH"
        },
        "H-total": {
            "function": 4,
            "address": 57,
            "count": 2,
            "coefficient": "0.5",
            "unit": "s"
        },
        "Current-power": {
            "function": 4,
            "address": 1,
            "count": 2,
            "coefficient": "0.1",
            "unit": "W"
        }
    }
}]

date_inv_out = [

]
