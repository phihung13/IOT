def led1_serializer(record) -> dict:
    return {
        'id' : str(record["_id"]),
        'device_name' : record["device_name"],
        'time': record["time"],
        'led1' : record["led1"],
    }

def led1s_serializer(records) -> list:
    return [led1_serializer(record) for record in records]