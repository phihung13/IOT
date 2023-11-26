def lcd_serializer(record) -> dict:
    return {
        'id' : str(record["_id"]),
        'device_name' : record["device_name"],
        'time': record["time"],
        'lcd' : record["lcd"],
    }

def lcds_serializer(records) -> list:
    return [lcd_serializer(record) for record in records]