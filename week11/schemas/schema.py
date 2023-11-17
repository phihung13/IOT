def record_serializer(record) -> dict:
    return {
        'id' : str(record["_id"]),
        'device_name' : record["device_name"],
        'time': record["time"],
        "data": record["data"],
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

def ultra_serializer(record) -> dict:
    return {
        'id' : str(record["_id"]),
        'device_name' : record["device_name"],
        'time': record["time"],
        'ultra' : record["ultra"],
    }

def rotary_serializer(record) -> dict:
    return {
        'id' : str(record["_id"]),
        'device_name' : record["device_name"],
        'time': record["time"],
        'rotary' : record["rotary"],
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

def ultras_serializer(records) -> list:
    return [ultra_serializer(record) for record in records]

def rotarys_serializer(records) -> list:
    return [rotary_serializer(record) for record in records]

def all_records(records) -> list:
    result_list = []
    for document in records:
        # Chuyển đổi ObjectId thành str trước khi chuyển đổi sang JSON
        document["_id"] = str(document["_id"])
        result_list.append(document)
    return result_list
