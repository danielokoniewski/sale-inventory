from typing import List

from fastapi import APIRouter, Path, HTTPException, status

from .entity import Item, NewItem
from .repository import BaseRepository
from .usecases import ItemUseCase

_repo: BaseRepository


def set_repository(repository: BaseRepository):
    global _repo
    _repo = repository


router = APIRouter()


@router.get("/items", response_model=List[Item])
async def read_items():
    return ItemUseCase(repo=_repo).get_all_items()


@router.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: NewItem):
    new_item = ItemUseCase(repo=_repo).add_item(item=item)
    return new_item


# Read item
@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int = Path(..., title="The ID of the item to read")):
    """
    returns the item with id item_id
    :param item_id:
    :return:
    """
    item = ItemUseCase(repo=_repo).get_item(item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# Update item
@router.put("/items/{item_id}", response_model=Item, status_code=status.HTTP_202_ACCEPTED)
async def update_item(item_id: int, item: Item):
    if item.id != item_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="item ids does not match")

    new_item = ItemUseCase(repo=_repo).update_item(item=item)

    if new_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return new_item


# Delete item
@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    if not ItemUseCase(repo=_repo).delete_item(item_id=item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
