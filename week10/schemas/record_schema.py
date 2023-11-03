def record_serializer(record) -> dict:
    return {
        'id' : str(record["_id"]),
        'device_name' : record["device_name"],
        'time': record["time"],
        'temp' : record["temp"],
        'humi' : record["humi"],
        'led1' : record["led1"],
        'led2' : record["led2"],
    }

def temp_serializer(record) -> dict:
    return {
        'id' : str(record["_id"]),
        'device_name' : record["device_name"],
        'time': record["time"],
        'temp' : record["temp"],
    }

def humi_serializer(record) -> dict:
    return {
        'id' : str(record["_id"]),
        'device_name' : record["device_name"],
        'time': record["time"],
        'humi' : record["humi"],

    }

def led1_serializer(record) -> dict:
    return {
        'id' : str(record["_id"]),
        'device_name' : record["device_name"],
        'time': record["time"],
        'led1' : record["led1"],
    }

def led2_serializer(record) -> dict:
    return {
        'id' : str(record["_id"]),
        'device_name' : record["device_name"],
        'time': record["time"],
        'led2' : record["led2"],
    }

def records_serializer(records) -> list:
    return [record_serializer(record) for record in records]

def temps_serializer(records) -> list:
    return [temp_serializer(record) for record in records]

def humis_serializer(records) -> list:
    return [humi_serializer(record) for record in records]

def led1s_serializer(records) -> list:
    return [led1_serializer(record) for record in records]

def led2s_serializer(records) -> list:
    return [led2_serializer(record) for record in records]
