def led2_serializer(record) -> dict:
    return {
        'id' : str(record["_id"]),
        'device_name' : record["device_name"],
        'time': record["time"],
        'led2' : record["led2"],
    }

def led2s_serializer(records) -> list:
    return [led2_serializer(record) for record in records]