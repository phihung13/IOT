def temp_serializer(record) -> dict:
    return {
        'id' : str(record["_id"]),
        'device_name' : record["device_name"],
        'time': record["time"],
        'temp' : record["temp"],
    }

def temps_serializer(records) -> list:
    return [temp_serializer(record) for record in records]