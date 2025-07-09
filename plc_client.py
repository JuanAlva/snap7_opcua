import snap7
from snap7.util import get_bool, get_int, get_real
from snap7.type import Area
import logging
import time

class PLCClient:
    def __init__(self, ip='192.168.0.1', rack=0, slot=1): # valores por defecto
        self.client = snap7.client.Client()
        self.ip = ip
        self.rack = rack
        self.slot = slot
        self.connected = False
        self.connect()

    # -------------------- Conexión --------------------
    def connect(self):
        try:
            self.client.connect(self.ip, self.rack, self.slot)
            self.connected = self.client.get_connected()
            if self.connected:
                logging.info("Conectado al PLC")
            else:
                raise RuntimeError("Conexion fallida: estado desconectado")
        except Exception as e:
            self.connected = False
            raise RuntimeError(f"Error de conexión al PLC: {e}")

    def disconnect(self):
        if self.connected:
            self.client.disconnect()
            self.connected = False
            logging.info("Desconectado del PLC")

    def try_reconnect(self, retry_delay=5, max_attempts=None):
        attempts = 0
        while not self.connected:
            try:
                logging.info("Intentando reconectar al PLC...")
                self.connect()
                if self.connected:
                    logging.info("Reconexión exitosa al PLC")
                    break
            except Exception as e:
                logging.error(f"Error en reconexión: {e}")
            attempts += 1
            if max_attempts and attempts >= max_attempts:
                logging.error("Máximo número de reintentos alcanzado")
                break
            time.sleep(retry_delay)

    # -------------------- Lecturas genéricas --------------------
    def _chk(self):
        if not self.connected:
            raise RuntimeError("PLC no conectado")

    def read_area(self, area, byte_index, size):
        self._chk()
        return self.client.read_area(area, 0, byte_index, size)  # 0 = DB num cuando es área PE/PA/MK

    def read_db(self, db_number, start, size):
        self._chk()
        return self.client.db_read(db_number, start, size)

    # -------------------- Lecturas primitivas --------------------
    # Área (PE = Inputs, PA = Outputs, MK = Merkers)
    def read_bit(self, area, byte_index, bit_index):
        data = self.read_area(area, byte_index, 1)
        return get_bool(data, 0, bit_index)

    def read_int(self, area, byte_index):
        data = self.read_area(area, byte_index, 2)
        return get_int(data, 0)

    def read_real(self, area, byte_index):
        data = self.read_area(area, byte_index, 4)
        return get_real(data, 0)

    # DB
    def read_bit_db(self, db, offset, bit_index):
        data = self.read_db(db, offset, 1)
        return get_bool(data, 0, bit_index)

    def read_int_db(self, db, offset):
        data = self.read_db(db, offset, 2)
        return get_int(data, 0)

    def read_real_db(self, db, offset):
        data = self.read_db(db, offset, 4)
        return get_real(data, 0)

    def read_string_db(self, db, offset, max_len=255):
        data = self.read_db(db, offset, max_len)
        actual_len = data[1]            # longitud real
        return data[2:2 + actual_len].decode("utf-8")

    # -------------------- Atajos semánticos --------------------
    # Entradas (Input = PE)
    def read_bit_in(self, byte_index, bit_index):
        return self.read_bit(Area.PE, byte_index, bit_index)

    def read_int_in(self, byte_index):
        return self.read_int(Area.PE, byte_index)

    def read_real_in(self, byte_index):
        return self.read_real(Area.PE, byte_index)

    # Salidas (Output = PA)
    def read_bit_out(self, byte_index, bit_index):
        return self.read_bit(Area.PA, byte_index, bit_index)

    def read_int_out(self, byte_index):
        return self.read_int(Area.PA, byte_index)

    def read_real_out(self, byte_index):
        return self.read_real(Area.PA, byte_index)

    # Marcas (Memory = MK)
    def read_bit_mrk(self, byte_index, bit_index):
        return self.read_bit(Area.MK, byte_index, bit_index)

    def read_int_mrk(self, byte_index):
        return self.read_int(Area.MK, byte_index)

    def read_real_mrk(self, byte_index):
        return self.read_real(Area.MK, byte_index)
