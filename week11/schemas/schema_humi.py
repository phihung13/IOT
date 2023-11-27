def humi_serializer(record) -> dict:
    return {
        'id' : str(record["_id"]),
        'device_name' : record["device_name"],
        'time': record["time"],
        'humi' : record["humi"],
    }

def humis_serializer(records) -> list:
    return [humi_serializer(record) for record in records]