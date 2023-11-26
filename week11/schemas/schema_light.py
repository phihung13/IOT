def light_serializer(record) -> dict:
    return {
        'id' : str(record["_id"]),
        'device_name' : record["device_name"],
        'time': record["time"],
        'light' : record["light"],
    }

def lights_serializer(records) -> list:
    return [light_serializer(record) for record in records]