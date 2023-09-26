from .schemas import FavoriteItem

def get_favorite_items(data: list, limit: int = 1, offset: int = 0):
    return data[offset:offset + limit]

def get_favorite_item(item_id: int, data: list):
    for item in data:
        if item["id"] == item_id:
            return FavoriteItem(**item)
    return None

def add_favorite_item(item: FavoriteItem, data: list):
    # Проверяем, есть ли уже элемент с таким же id в списке
    for existing_item in data:
        if existing_item["id"] == item.id:
            return None
    # Если элемент с таким id не найден, то добавляем новый элемент
    data.append(item.dict())
    return item

def update_favorite_item(item_id: int, updated_item: FavoriteItem, data: list):
    for idx, item in enumerate(data):
        if item["id"] == item_id:
            data[idx] = updated_item.dict()
            return updated_item
    return None

def delete_favorite_item(item_id: int, data: list):
    for item in data:
        if item["id"] == item_id:
            deleted_item = data.pop(data.index(item))
            return FavoriteItem(**deleted_item)
    return None
