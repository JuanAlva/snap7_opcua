import time
import logging
from config import *
from plc_client import PLCClient
from opcua_server import OPCUAServer
from variable_manager import OPCUAVariableManager
from variable_loader import cargar_variables_desde_archivo

RECONNECT_INTERVAL = 5  # segundos

logging.basicConfig(level=logging.INFO)
logging.getLogger("opcua.server").setLevel(logging.WARNING)

def main():
    # Inicializar PLC y servidor OPC UA
    plc = PLCClient(ip=PLC_IP, rack=PLC_RACK, slot=PLC_SLOT)
    opcua = OPCUAServer()
    
    var_config = cargar_variables_desde_archivo("prueba") # archivo con datos en formato ASCII
    manager = OPCUAVariableManager(plc, opcua, var_config)

    opcua.start()

    try:
        while True:
            try:
                if not plc.connected:
                    logging.info("PLC no conectado. Intentando reconectar...")
                    plc.try_reconnect(retry_delay=RECONNECT_INTERVAL)

                manager.update_variables()
                logging.info(f"[Valores actualizados]")
            
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
