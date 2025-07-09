import logging

class OPCUAVariableManager:
    def __init__(self, plc_client, opcua_server, config_list):
        self.plc = plc_client
        self.opcua = opcua_server
        self.variables = config_list  # Lista de diccionarios con la config

        self._create_variables()

    def _create_variables(self):
        for var in self.variables:
            # Inicializa según tipo
            default_value = False if var["type"] == "BOOL" else 0
            self.opcua.add_variable(var["desc"], default_value)

    def update_variables(self):
        for var in self.variables:
            try:
                value = self._read_from_plc(var)
                self.opcua.set_value(var["desc"], value)
            except Exception as e:
                logging.error(f"Error leyendo {var['desc']} del PLC: {e}")

    def _read_from_plc(self, var):
        area = var["area"]
        byte_index = var["byte"]
        bit_index = var.get("bit")  # solo para BOOL

        if area == "E":  # Entradas
            if var["type"] == "BOOL":
                return self.plc.read_bit_in(byte_index, bit_index)
            elif var["type"] == "WORD":
                return self.plc.read_int_in(byte_index)

        elif area == "A":  # Salidas
            if var["type"] == "BOOL":
                return self.plc.read_bit_out(byte_index, bit_index)
            elif var["type"] == "WORD":
                return self.plc.read_int_out(byte_index)

        elif area == "M":  # Marcas
            if var["type"] == "BOOL":
                return self.plc.read_bit_mrk(byte_index, bit_index)
            elif var["type"] == "WORD":
                return self.plc.read_int_mrk(byte_index)

        raise ValueError(f"Tipo de área no reconocida: {area}")
