import time
import logging
from config import *
from plc_client import PLCClient
from opcua_server import OPCUAServer

RECONNECT_INTERVAL = 5  # segundos

logging.basicConfig(level=logging.INFO)
logging.getLogger("opcua.server").setLevel(logging.WARNING)

def main():
    # Inicializar PLC y servidor OPC UA
    plc = PLCClient(ip=PLC_IP, rack=PLC_RACK, slot=PLC_SLOT)
    opcua = OPCUAServer()
    
    # Crear variables en el servidor OPC UA
    opcua.add_variable("I0_0", False)
    opcua.add_variable("Q1_1", False)
    opcua.add_variable("MD208", 0.0)
    opcua.add_variable("Product_Name", "")
    opcua.add_variable("Product_Value", 0)
    opcua.add_variable("Product_Status", False)

    opcua.start()

    try:
        while True:
            try:
                if not plc.connected:
                    logging.info("PLC no conectado. Intentando reconectar...")
                    plc.try_reconnect(retry_delay=RECONNECT_INTERVAL)

                # Leer del PLC
                i0_0 = plc.read_bit_in(0, 0)
                q1_1 = plc.read_bit_out(1, 1)
                md208 = plc.read_real_mrk(208)
                name = plc.read_string_db(104, 0)
                value = plc.read_int_db(104, 256)
                status = plc.read_bit_db(104, 258, 0)

                # Publicar en OPC UA
                opcua.set_value("I0_0", i0_0)
                opcua.set_value("Q1_1", q1_1)
                opcua.set_value("MD208", md208)
                opcua.set_value("Product_Name", name)
                opcua.set_value("Product_Value", value)
                opcua.set_value("Product_Status", status)

                logging.info(f"[Valores actualizados] I0.0={i0_0}, Q1.1={q1_1}, MD208={md208}, Name={name}, Value={value}, Status={status}")
            
            except RuntimeError as e:
                logging.error(f"Error de conexión con PLC: {e}")
                plc.disconnect() # asegurate de cerrar la sesion malograda
                logging.info(f"Esperando {RECONNECT_INTERVAL} segundos antes de reconectar...")
                time.sleep(RECONNECT_INTERVAL)

            time.sleep(1) # ciclo de lectura
            

    except KeyboardInterrupt:
        logging.info("Detenido por usuario")
    
    finally:
        plc.disconnect()
        opcua.stop()

if __name__ == "__main__":
    main()
