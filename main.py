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
    
    var_config = cargar_variables_desde_archivo(ARCHIVO_EXTRAIDO_DEL_PLC) # archivo con datos en formato ASCII
    manager = OPCUAVariableManager(plc, opcua, var_config)

    opcua.start()

    try:
        while True:
            if not plc.connected:
                logging.warning("PLC no conectado. Intentando reconectar...")
                plc.try_reconnect(retry_delay=RECONNECT_INTERVAL)
                time.sleep(RECONNECT_INTERVAL)
                continue  # no intentes leer si aún no conecta

            try:
                manager.update_variables()
                logging.info("[Valores actualizados]")
            except Exception as e:
                logging.error(f"[main] Error al actualizar variables: {e}")
                plc.disconnect()
                logging.info(f"Esperando {RECONNECT_INTERVAL} segundos antes de reconectar...")
                time.sleep(RECONNECT_INTERVAL)

            time.sleep(1) # modificar en caso se quiera aumentar el tiempo de muestreo
                
    except KeyboardInterrupt:
        logging.info("Detenido por usuario")
    
    finally:
        plc.disconnect()
        opcua.stop()

if __name__ == "__main__":
    main()
