def sonic_serializer(record) -> dict:
    return {
        'id' : str(record["_id"]),
        'device_name' : record["device_name"],
        'time': record["time"],
        'sonic' : record["sonic"],
    }

def sonics_serializer(records) -> list:
    return [sonic_serializer(record) for record in records]