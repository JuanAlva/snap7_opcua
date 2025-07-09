# opcua_server.py

from opcua import Server, ua
import logging
from config import OPCUA_SERVER_URL

class OPCUAServer:
    def __init__(self, endpoint=OPCUA_SERVER_URL, uri="http://example.org/plc"):
        self.server = Server()
        self.server.set_endpoint(endpoint)
        self.idx = self.server.register_namespace(uri)
        self.variables = {}
        self.plc_node = self.server.nodes.objects.add_object(self.idx, "PLC")

    def add_variable(self, name, initial_value):
        var = self.plc_node.add_variable(self.idx, name, initial_value)
        var.set_writable()
        access = ua.AccessLevel.CurrentRead | ua.AccessLevel.CurrentWrite
        var.set_attribute(ua.AttributeIds.AccessLevel, ua.DataValue(access))
        var.set_attribute(ua.AttributeIds.UserAccessLevel, ua.DataValue(access))
        self.variables[name] = var
        return var

    def set_value(self, name, value):
        if name in self.variables:
            self.variables[name].set_value(value)
        else:
            logging.warning(f"Variable OPC UA '{name}' no encontrada")

    def start(self):
        self.server.start()
        logging.info("Servidor OPC UA iniciado")

    def stop(self):
        self.server.stop()
        logging.info("Servidor OPC UA detenido")
