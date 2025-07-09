import csv

def cargar_variables_desde_archivo(path):
    variables = []
    with open(path, encoding='latin-1') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 4:
                continue  # omitir líneas incompletas

            name = row[0].strip().replace('"', '')
            direccion_raw = row[1].strip().replace('"', '')
            tipo = row[2].strip().replace('"', '').upper()
            descripcion = row[3].strip().replace('"', '')

            # Separar área y posición limpiando espacios intermedios
            partes = direccion_raw.strip().split()
            if len(partes) != 2:
                continue  # omitir si el formato no es válido

            area = partes[0][0]  # E, A, M, W, etc.
            pos = partes[1]

            try:
                if '.' in pos:
                    byte_str, bit_str = pos.split('.')
                    byte = int(byte_str)
                    bit = int(bit_str)
                else:
                    byte = int(pos)
                    bit = None  # aplica para WORD o tipo completo
            except ValueError:
                continue  # saltar si no es un número válido

            variables.append({
                "name": name,
                "area": area,
                "byte": byte,
                "bit": bit,
                "type": tipo,
                "desc": descripcion
            })

    return variables
