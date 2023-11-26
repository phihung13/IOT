def ledstick_serializer(record) -> dict:
    return {
        'id' : str(record["_id"]),
        'device_name' : record["device_name"],
        'time': record["time"],
        'ledstick' : record["ledstick"],
    }

def ledsticks_serializer(records) -> list:
    return [ledstick_serializer(record) for record in records]