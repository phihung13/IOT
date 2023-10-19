def record_serializer(record) -> dict:
    return {
        'id' : str(record["_id"]),
        'device_name' : record["device_name"],
        'time': record["time"],
        'tem' : record["tem"],
        'humi' : record["humi"],
        'led1' : record["led1"],
        'led2' : record["led2"],
    }


def records_serializer(records) -> list:
    return [record_serializer(record) for record in records]