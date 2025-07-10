from variable_loader import cargar_variables_desde_archivo  # cambia 'tu_archivo' por el nombre del .py que tiene la función
from config import ARCHIVO_EXTRAIDO_DEL_PLC

variables = cargar_variables_desde_archivo(ARCHIVO_EXTRAIDO_DEL_PLC)

# Mostrar la tabla generada
for var in variables:
    print(f"{var['name']:10} | Area: {var['area']} | Byte: {var['byte']:3} | Bit: {str(var['bit']):>4} | Tipo: {var['type']:6} | {var['desc']}")