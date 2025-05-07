

def search_inventory(query, inventory_data):
    """
    Searches the inventory data for items that match the query. The search is case-insensitive.
    """
    query = query.lower()  # Convert the search query to lowercase for case-insensitive comparison
    
    # Return a list of items where any field in the item contains the query string
    return [
        item for item in inventory_data  # Loop through each item in the inventory data
        if any(query in str(field).lower() for field in item)  # Check if the query exists in any field (case-insensitive)
    ]
