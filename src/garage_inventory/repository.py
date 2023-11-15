from abc import ABC, abstractmethod
from typing import List

from src.garage_inventory.entity import Item


class BaseRepository(ABC):
    @abstractmethod
    def get_item(self, item_id: int) -> Item | None:
        ...

    @abstractmethod
    def get_items(self) -> List[Item]:
        ...

    @abstractmethod
    def create_item(self, item: Item) -> Item | None:
        ...

    @abstractmethod
    def update_item(self, item: Item) -> Item | None:
        ...

    @abstractmethod
    def delete_item(self, item_id: int) -> bool:
        ...


class ListRepository(BaseRepository):
    items = {}

    def get_item(self, item_id: int) -> Item | None:
        if item_id not in self.items:
            return None
        return self.items[item_id]

    def get_items(self) -> List[Item]:
        return list(self.items.values())

    def create_item(self, item: Item) -> Item:
        item.id = self._get_max_id() + 1
        self.items[item.id] = item
        return item

    def update_item(self, item: Item) -> Item | None:
        if item.id not in self.items.keys():
            return None
        self.items[item.id] = item
        return item

    def delete_item(self, item_id: int) -> bool:
        if item_id in self.items:
            self.items.pop(item_id)
            return True
        return False

    def _get_max_id(self) -> int:
        if len(self.items) == 0:
            return 0
        return max(self.items.keys())
