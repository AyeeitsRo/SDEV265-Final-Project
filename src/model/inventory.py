


def search_inventory(query, inventory_data):
    query = query.lower()
    return [
        item for item in inventory_data
        if any(query in str(field).lower() for field in item)
    ]
