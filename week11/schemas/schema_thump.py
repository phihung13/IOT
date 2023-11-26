def thump_serializer(record) -> dict:
    return {
        'id' : str(record["_id"]),
        'device_name' : record["device_name"],
        'time': record["time"],
        'thump' : record["thump"],
    }

def thumps_serializer(records) -> list:
    return [thump_serializer(record) for record in records]