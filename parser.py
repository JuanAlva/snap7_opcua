def decode_product_data(db):
    product_name = db[2:256].decode('UTF-8').strip('\x00')
    product_value = int.from_bytes(db[256:258], byteorder='big')
    product_status = bool(db[258])
    return product_name, product_value, product_status
