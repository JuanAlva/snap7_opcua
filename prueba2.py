def conectar_plc():
    while True:
        try:
            if not plc.get_connected():
                print("Intentando conectar con el PLC...")
                plc.connect(IP, RACK, SLOT)
                print("Conectado al PLC")
            return
        except Exception as e:
            print("Error de conexión:", e)
            time.sleep(5)  # espera antes de reintentar
