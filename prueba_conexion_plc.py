import time
import snap7
from snap7.util import *
from snap7.type import Area

IP = '192.168.146.157'
RACK = 0
SLOT = 2


plc = snap7.client.Client()
plc.connect(IP, RACK, SLOT)

def read_bit(area, byte_index, bit_index):
    data = plc.read_area(area, 0, byte_index, 1)  # leer 1 byte desde el área especificada
    return get_bool(data, 0, bit_index)

def read_int(area, byte_index):
    data = plc.read_area(area, 0, byte_index, 2) 
    return get_int(data, 0)

def read_real(area, byte_index):
    data = plc.read_area(area, 0, byte_index, 4) 
    return get_real(data, 0)

def read_bit_db(db, offset, bit_index):
    data = plc.db_read(db, offset, 1)   
    return get_bool(data, 0, bit_index)

def read_int_db(db, offset):
    data = plc.db_read(db, offset, 2)   
    return get_int(data, 0)

def read_real_db(db, offset):
    data = plc.db_read(db, offset, 4)   
    return get_real(data, 0)

def read_string_db(db, offset):
    data = plc.db_read(db, offset, 255)
    actual_len = data[1]
    return data[2:2 + actual_len].decode('utf-8')

def read_bit_in(byte_index, bit_index):
    return read_bit(Area.PE, byte_index, bit_index)

def read_int_in(byte_index):
    return read_int(Area.PE, byte_index)

def read_real_in(byte_index):
    return read_real(Area.PE, byte_index)

def read_bit_out(byte_index, bit_index):
    return read_bit(Area.PA, byte_index, bit_index)

def read_int_out(byte_index):
    return read_int(Area.PA, byte_index)

def read_real_out(byte_index):
    return read_real(Area.PA, byte_index)

def read_bit_mr(byte_index, bit_index):
    return read_bit(Area.MK, byte_index, bit_index)

def read_int_mr(byte_index):
    return read_int(Area.MK, byte_index)

def read_real_mr(byte_index):
    return read_real(Area.MK, byte_index)

"""# Leer una entrada (ej. I0.0)
entrada00 = read_bit_in(0, 0)
print(f"I0.0: {entrada00}")

# Leer una entrada (ej. I0.1)
entrada01 = read_bit_in(0, 1)
print(f"I0.1: {entrada01}")

entradaAnalogica = read_int_in(64)
print(f"IW64: {entradaAnalogica}")

# Leer una salida (ej. Q1.1)
salida = read_bit_out(1, 1)
print(f"Q1.1: {salida}")

# Leer una marca (ej. M10.5)
marca = read_bit_mr(10, 5)
print(f"M10.5: {marca}")

marcaEntero = read_int_mr(8)
print(f"MW8: {marcaEntero}")

marcaReal = read_real_mr(208)
print(f"MD208: {marcaReal}")

estadoDB = read_bit_db(104, 258, 0)
print(f"estado: {estadoDB}")

valorDB = read_int_db(104, 256)
print(f"valor: {valorDB}")

realDB = read_real_db(104, 255)
print(f"valorReal: {realDB}")

nombreDB = read_string_db(104, 0)
print(f"nombre: {nombreDB}")
"""

marca51_4 = read_bit_mr(51, 4)
print(f"nombre: {marca51_4}")

marcaWord2 = read_int_mr(2)
print(f"nombre: {marcaWord2}")

time.sleep(50)

plc.disconnect()