PLC_IP = "192.168.146.157"                  # IP del plc
PLC_RACK = 0                                # ubicacion del plc en el rack, generalmente es 0
PLC_SLOT = 2                                # espacio del plc, para s7 300: slot 2, y para s7 1200: slot 1

ARCHIVO_EXTRAIDO_DEL_PLC = 'prueba'         # nombre del archivo exportado del plc con variables en formato ASCII

OPCUA_SERVER_URL = "opc.tcp://0.0.0.0:4840" # "opc.tcp://192.168.146.67:4840" o "opc.tcp://localhost:4840"
                                            # camibar el puerto en caso tener distintos servidores OPCUA en una misma computadora