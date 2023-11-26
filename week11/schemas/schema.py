def record_serializer(record) -> dict:
    return {
        'id' : str(record["_id"]),
        'device_name' : record["device_name"],
        'time': record["time"],
        "data": record["data"],
    }

def records_serializer(records) -> list:
    return [record_serializer(record) for record in records]


def all_records(records) -> list:
    result_list = []
    for document in records:
        # Chuyển đổi ObjectId thành str trước khi chuyển đổi sang JSON
        document["_id"] = str(document["_id"])
        result_list.append(document)
    return result_list
