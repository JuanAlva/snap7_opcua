import csv

def conv_ASCII_to_CSV():
    # Abrimos el archivo original
    with open("prueba", newline='', encoding='latin-1') as archivo_entrada:
        lector = csv.reader(archivo_entrada)

        # Abrimos un nuevo archivo para guardar la tabla
        with open("tabla_salida.csv", mode="w", newline='', encoding='utf-8') as archivo_salida:
            escritor = csv.writer(archivo_salida)

            # Escribir encabezados
            #escritor.writerow(["Simbolo", "Direccion", "Tipo", "Descripcion"])

            # Escribir cada fila limpiando los campos
            for fila in lector:
                fila_limpia = [campo.strip() for campo in fila]
                escritor.writerow(fila_limpia)

    print("✅ Archivo 'tabla_salida.csv' creado correctamente.")