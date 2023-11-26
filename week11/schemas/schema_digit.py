def digit_serializer(record) -> dict:
    return {
        'id' : str(record["_id"]),
        'device_name' : record["device_name"],
        'time': record["time"],
        'digit' : record["digit"],
    }

def digits_serializer(records) -> list:
    return [digit_serializer(record) for record in records]