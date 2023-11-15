from typing import List

from .entity import Item, NewItem
from .repository import BaseRepository


class BaseUseCase:
    """
    makes sure each use case has a repository
    """
    repo: BaseRepository

    def __init__(self, repo: BaseRepository) -> None:
        self.repo = repo


class ItemUseCase(BaseUseCase):
    """
    item related use cases
    """

    def add_item(self, item: NewItem) -> Item | None:
        new_item = Item(
            id=0,
            name=item.name,
            description=item.description,
            owner=item.owner,
            expiration_date=item.expiration_date,
            shipping=item.shipping,
            price=item.price
        )
        return self.repo.create_item(new_item)

    def update_item(self, item: Item) -> Item | None:
        return self.repo.update_item(item)

    def delete_item(self, item_id: int) -> bool:
        return self.repo.delete_item(item_id)

    def get_item(self, item_id: int) -> Item | None:
        return self.repo.get_item(item_id)

    def get_all_items(self) -> List[Item]:
        return self.repo.get_items()
