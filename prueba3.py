import time
import snap7

IP = '192.168.146.151'
RACK = 0
SLOT = 1
DB_NUMBER = 104
START_ADDRESS = 0
SIZE = 259

plc = snap7.client.Client()
plc.connect(IP, RACK, SLOT)

# try:
#     db = plc.db_read(DB_NUMBER, START_ADDRESS, SIZE)
#     print("Lectura DB OK:", db)
# except Exception as e:
#     print("Error al leer DB:", e)
# finally:
#     plc.disconnect()


db = plc.db_read(DB_NUMBER, START_ADDRESS, SIZE)

product_name = db[2:256].decode('UTF-8').strip('\x00')
print(f'PRODUCT NAME: {product_name}')

product_value = int.from_bytes(db[256:258], byteorder='big')
print(f'PRODUCT VALUE: {product_value}')

product_status = bool(db[258])
print(product_status)

time.sleep(15)